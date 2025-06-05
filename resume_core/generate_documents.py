import json
import sys
from typing import Dict, Any
from pathlib import Path
from datetime import datetime
from cvparser import parse_resume_with_openai, extract_text_from_pdf, load_config, client
from coverlatter import CoverLetterGenerator

def save_as_json(data: Dict[str, Any], filepath: Path) -> None:
    """Save data as a pretty-printed JSON file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def extract_job_details(job_description: str) -> dict:
    """Extract key job details from the job description.
    
    Args:
        job_description: The full job description text
        
    Returns:
        dict: Extracted job details including position, company, etc.
    """
    # Default values
    details = {
        'position': 'the position',
        'company': 'your company',
        'hiring_manager': 'Hiring Manager',
        'hiring_title': '',
        'location': '',
        'company_info': ''
    }
    
    # Clean the job description by removing extra whitespace and newlines
    clean_jd = ' '.join(job_description.split())
    
    try:
        import re
        
        # Clean the job description
        clean_jd = ' '.join(job_description.split())
        
        # 1. Look for position in common patterns
        position_patterns = [
            # Patterns from the start of the description
            r'^[^\n<>"]*?[Ww]e are seeking (?:a|an)?\s+([^\n<>\.\,;]+?)(?:\s+to join|\s+for|\s+who|\s*$|\s*[\.,;])',
            r'^[^\n<>"]*?[Ww]e are looking for (?:a|an)?\s+([^\n<>\.\,;]+?)(?:\s+to join|\s+for|\s+who|\s*$|\s*[\.,;])',
            r'^[^\n<>"]*?[Hh]iring:?\s+([^\n<>\.\,;]+?)(?:\s+to join|\s+for|\s+who|\s*$|\s*[\.,;])',
            
            # Standard position patterns
            r'[Pp]osition:\s*([^\n<>"]+?)<',  # Position: X<
            r'[Pp]osition:\s*([^\n<>"]+)',     # Position: X
            r'[Jj]ob [Tt]itle:\s*([^\n<>"]+)',
            r'[Pp]osition [Tt]itle:\s*([^\n<>"]+)',
            r'[Jj]ob [Pp]osition:\s*([^\n<>"]+)',
            
            # More general patterns
            r'join our team as (?:a|an)?\s+([^\n<>\.\,;]+?)(?:\s+to|\s+for|\s+who|\s*$|\s*[\.,;])',
            r'looking to hire (?:a|an)?\s+([^\n<>\.\,;]+?)(?:\s+to|\s+for|\s+who|\s*$|\s*[\.,;])',
            r'currently hiring (?:a|an)?\s+([^\n<>\.\,;]+?)(?:\s+to|\s+for|\s+who|\s*$|\s*[\.,;])'
        ]
        
        for pattern in position_patterns:
            match = re.search(pattern, clean_jd)
            if match and len(match.group(1).strip()) > 3:  # Ensure we don't get very short matches
                details['position'] = match.group(1).strip().strip('"\'').strip()
                break
        
        # 2. Look for company name with more precise patterns
        company_patterns = [
            # Look for company name after 'at' in the first few lines (most reliable)
            r'(?i)(?:^|\n|\s)(?:at|with|for|in|@|\bat\b|\bwith\b|\bfor\b|\bin\b|company|organization)[\s:]*([A-Z][A-Za-z0-9&\s\.,\-\']+?)(?:\s+(?:is|was|has|offers|provides|seeks|hiring|looking|\bfor\b|\bat\b|\bin\b|\.|,|$|\n))',
            # Look for company name in job title/header
            r'(?i)job (?:title|position|opening|posting|vacancy)[\s:]+(?:for|at|in|\bfor\b|\bat\b|\bin\b)[\s:]*([A-Z][A-Za-z0-9&\s\.,\-\']+?)(?:\s|$|\n|\.|,|\()',
            # Look for company name in email addresses
            r'\b[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Z|a-z]{2,})\b'
        ]
        
        # List of common phrases that should not be considered as company names
        invalid_company_phrases = [
            'our', 'your', 'their', 'this', 'that', 'these', 'those', 'any', 'some', 'every',
            'growing', 'dedicated', 'talented', 'skilled', 'experienced', 'passionate',
            'team', 'department', 'division', 'unit', 'group', 'company', 'organization',
            'analytics', 'data', 'engineering', 'development', 'technology', 'solutions',
            'looking for', 'seeking', 'hiring', 'apply now', 'job description', 'position',
            'role', 'opportunity', 'career', 'employment', 'vacancy', 'opening', 'posting',
            'years', 'business', 'since', 'founded', 'established', 'started', 'based', 'office'
        ]
        
        # First, try to find company in the first few lines (most likely to contain company info)
        first_few_lines = '\n'.join(clean_jd.split('\n')[:5])
        
        for pattern in company_patterns:
            match = re.search(pattern, first_few_lines) or re.search(pattern, clean_jd)
            if match:
                company = match.group(1).strip().strip('"\'').strip()
                # Clean up common endings and special characters
                company = re.sub(r'[\.,;:()\[\]{}<>\/\\]', ' ', company).strip()
                company = re.sub(r'\s+', ' ', company)  # Normalize spaces
                
                # Additional validation
                company_words = company.split()
                if (len(company) > 2 and 
                    2 <= len(company_words) <= 5 and
                    not any(word.lower() in invalid_company_phrases for word in company_words) and
                    not any(word.lower() in [w.lower() for w in company_words] for word in invalid_company_phrases)):
                    
                    # Additional check: if company name is too generic, skip it
                    if len(company) >= 4:  # At least 4 characters for a valid company name
                        details['company'] = company
                        break
        
        # If still no company found, try to extract from email domain
        if details['company'] == 'your company':
            email_match = re.search(r'\b[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Z|a-z]{2,})\b', clean_jd)
            if email_match:
                domain = email_match.group(1)
                # Remove common domain parts and clean up
                company = re.sub(r'\.(com|org|net|io|ai|co\.\w{2,3}|[a-z]{2,3})$', '', domain, flags=re.IGNORECASE)
                # Convert to title case and clean up
                company = ' '.join(word.capitalize() for word in re.split('[\.-]', company) if len(word) > 2)
                if company and 2 <= len(company.split()) <= 4:  # More strict validation for email-derived names
                    details['company'] = company
        
        # 3. Look for location with better patterns
        location_patterns = [
            r'(?i)location\s*[\:\-]\s*([^\n<>"]+?)(?:\s*\n|\s*$|\s*\|\s*|\s*\n\s*\n)',
            r'(?i)located in\s+([^\n<>"]+?)(?:\.|\n|$|,|\s*\|\s*)',
            r'(?i)office\s+location\s*[\:\-]?\s*([^\n<>"]+?)(?:\s*\n|\s*$|\s*\|\s*)',
            r'(?i)work\s+from\s+([^\n<>"]+?)(?:\s*\n|\s*$|\s*\|\s*|\s*\n\s*\n)'
        ]
        
        # First check the first few lines for location
        first_few_lines = '\n'.join(clean_jd.split('\n')[:5])
        
        for pattern in location_patterns:
            match = re.search(pattern, first_few_lines) or re.search(pattern, clean_jd)
            if match and len(match.group(1).strip()) > 3:
                location = match.group(1).strip().strip('"\'').strip()
                # Clean up common prefixes/suffixes
                location = re.sub(r'^(?:in|at|near|around|close to|\s)*', '', location, flags=re.IGNORECASE)
                location = re.sub(r'[\.,;:]$', '', location).strip()
                if location and len(location.split()) <= 5:  # Most locations are 1-3 words
                    details['location'] = location
                    break
            
        # 4. Clean up the position if it contains common prefixes/suffixes
        if details['position']:
            position = details['position']
            
            # First, clean up the position while preserving articles
            
            # Handle common prefixes while preserving articles
            prefix_patterns = [
                r'^we are (?:seeking|looking for|hiring)\s+',
                r'^join our team as\s+',
                r'^hiring:\s*',
                r'^position:\s*',
                r'^job (?:title|position):?\s*',
                r'^title:\s*',
                r'^role:\s*',
                r'^the\s+'  # Remove standalone 'the' at start
            ]
            
            for pattern in prefix_patterns:
                position = re.sub(pattern, '', position, flags=re.IGNORECASE)
            
            # Handle common suffixes
            suffix_patterns = [
                r'\s+position$',
                r'\s+job$',
                r'\s+role$',
                r'\s+title$',
                r'\s+vacancy$',
                r'\s+opportunity$',
                r'\s+opening$',
                r'\s+to join our team$',
                r'\s+to join$',
                r'\s+for our team$',
                r'\s+for the team$',
                r'\s+for the role$',
                r'\s+for this role$',
                r'\s+for this position$',
                r'\s*[\.,;:!?]*$'  # Remove trailing punctuation
            ]
            
            for pattern in suffix_patterns:
                position = re.sub(pattern, '', position, flags=re.IGNORECASE)
            
            # Clean up any remaining special characters (except spaces and hyphens)
            position = re.sub(r'[^\w\s-]', ' ', position)
            # Replace multiple spaces with single space
            position = ' '.join(position.split())
            
            # Capitalize the first letter
            position = position.strip()
            if position:
                position = position[0].upper() + position[1:]
            
            details['position'] = position.strip()
            
            # Ensure we have at least a default value
            if not details['position']:
                details['position'] = 'the position'
            
    except Exception as e:
        print(f"Warning: Could not extract job details: {e}")
    
    return details

def main():
    try:
        print("=== Resume Parser & Document Generator ===\n")
        
        # Get resume path from user
        resume_path = input("Enter path to your resume PDF: ").strip('"').strip()
        
        # Verify file exists
        if not Path(resume_path).is_file():
            print(f"Error: File not found at '{resume_path}'")
            return
            
        # Get job description
        print("\n=== Job Description ===")
        print("Paste the job description (press Enter, then Ctrl+Z and Enter when done):")
        job_description_lines = []
        try:
            while True:
                line = input()
                job_description_lines.append(line)
        except EOFError:
            pass
            
        job_description = '\n'.join(job_description_lines).strip()
        
        if not job_description:
            print("Error: Job description cannot be empty")
            return
            
        # Load configuration
        config = load_config()
        
        # Extract text from PDF
        print("\nExtracting text from resume...")
        with open(resume_path, 'rb') as f:
            resume_text = extract_text_from_pdf(f.read())
        
        if not resume_text:
            print("Error: Could not extract text from the PDF")
            return
            
        # Parse resume with OpenAI
        print("Parsing resume with AI...")
        parsed_profile = parse_resume_with_openai(resume_text)
        
        # Generate documents
        print("\nGenerating tailored documents...")
        generator = CoverLetterGenerator()
        
        # Create output directory with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = Path("output") / f"documents_{timestamp}"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save parsed profile
        profile_path = output_dir / "parsed_profile.json"
        save_as_json(parsed_profile, profile_path)
        
        # Generate and save resume as JSON
        print("\n=== GENERATING TAILORED RESUME ===")
        # The parsed profile already contains all the structured data we need
        # Just update the generation timestamp
        parsed_profile["generated_at"] = datetime.now().isoformat()
        
        # Save the tailored resume with the same structure as parsed profile
        resume_path = output_dir / "tailored_resume.json"
        save_as_json(parsed_profile, resume_path)
        
        # Extract job details from the job description
        job_details = extract_job_details(job_description)
        
        # Ensure we have a valid position for the subject line
        position = job_details.get('position', '').strip()
        if not position or len(position) < 2:  # If position is too short or empty
            # Try to extract from the first line of job description
            first_line = job_description.split('\n')[0].strip()
            if len(first_line) > 10:  # If first line seems meaningful
                position = first_line
            else:
                position = 'the position'
        
        company = job_details.get('company', 'your company').strip()
        
        # Generate cover letter with the extracted job details
        cover_letter_content = generator.generate_cover_letter(
            parsed_profile, 
            job_description,
            position=position,
            company=company
        )
        
        # Clean and validate company name
        clean_company = company if company and company.lower() != 'your company' else job_details.get('company', 'the Company')
        
        # Clean and validate location
        clean_location = job_details.get('location', '')
        # If location is too long (likely contains job description), use empty string
        if len(clean_location) > 100 or '\n' in clean_location:
            clean_location = ''
        
        # Clean position title - ensure it's not too long and doesn't contain newlines
        clean_position = position
        if '\n' in clean_position:
            clean_position = clean_position.split('\n')[0].strip()
        if len(clean_position) > 100:  # Truncate if too long
            clean_position = clean_position[:97] + '...'
        
        # Parse the cover letter content into structured data
        cover_letter_data = {
            "sender": {
                "name": parsed_profile.get("full_name", ""),
                "address": parsed_profile.get("address", ""),
                "email": parsed_profile.get("email", ""),
                "phone": parsed_profile.get("phone", "")
            },
            "recipient": {
                "name": job_details.get('hiring_manager', 'Hiring Manager'),
                "title": job_details.get('hiring_title', ''),
                "organization": clean_company,
                "address": clean_location
            },
            "date": datetime.now().strftime("%B %d, %Y"),
            "subject": f"Application for {clean_position}",
            "body": cover_letter_content,
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "position_applied": clean_position,
                "organization": clean_company
            }
        }
        
        cover_letter_path = output_dir / "cover_letter.json"
        save_as_json(cover_letter_data, cover_letter_path)
        
        # Save job description as separate JSON for reference
        job_desc_path = output_dir / "job_description.json"
        job_desc_data = {
            "job_description": job_description,
            "parsed_at": datetime.now().isoformat()
        }
        save_as_json(job_desc_data, job_desc_path)
        
        print(f"\n=== DOCUMENTS GENERATED SUCCESSFULLY ===")
        print(f"Output directory: {output_dir}")
        print(f"- Parsed Profile: {profile_path}")
        print(f"- Tailored Resume: {resume_path}")
        print(f"- Cover Letter: {cover_letter_path}")
        print(f"- Job Description: {job_desc_path}")
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        if hasattr(e, '__traceback__'):
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()
