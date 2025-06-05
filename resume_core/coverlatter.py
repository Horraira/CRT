import json
from typing import Dict, Any
from openai import OpenAI
import yaml

class CoverLetterGenerator:
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize the CoverLetterGenerator with configuration.
        
        Args:
            config_path: Path to the YAML configuration file
        """
        self.config = self._load_config(config_path)
        self.client = OpenAI(api_key=self.config.get("OPENAI_API_KEY"))

    @staticmethod
    def _load_config(config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file.
        
        Args:
            config_path: Path to the YAML configuration file
            
        Returns:
            dict: Loaded configuration
        """
        try:
            with open(config_path) as f:
                return yaml.safe_load(f)
        except Exception as e:
            raise RuntimeError(f"Failed to load config: {e}")

    def generate_resume(self, user_profile: Dict[str, Any], job_description: str) -> str:
        """Generate a tailored resume based on user profile and job description.
        
        Args:
            user_profile: Parsed user profile from CV
            job_description: Job description text
            
        Returns:
            str: Generated resume in markdown format
        """
        prompt = f"""
You are a professional resume writer.

Using the following USER PROFILE and JOB DESCRIPTION, create a customized, ATS-friendly resume that aligns with the job role.

USER PROFILE:
{json.dumps(user_profile, indent=2)}

JOB DESCRIPTION:
{job_description}

Output only the resume in text/markdown format. Focus on highlighting the most relevant experiences and skills for this specific job.
"""
        return self._get_ai_response(prompt)

    def _format_contact_info(self, user_profile: Dict[str, Any]) -> str:
        """Format the sender's contact information for the cover letter.
        
        Args:
            user_profile: Parsed user profile from CV
            
        Returns:
            str: Formatted contact information with date
        """
        if not user_profile:
            return ""
            
        # Helper function to safely get and clean string values
        def clean_value(value):
            if value is None:
                return ''
            if not isinstance(value, str):
                value = str(value)
            return value.strip()
            
        # Extract contact information with fallbacks, handling None values
        name = clean_value(user_profile.get('full_name'))
        email = clean_value(user_profile.get('email'))
        phone = clean_value(user_profile.get('phone'))
        
        # Format the date
        from datetime import datetime
        date_str = datetime.now().strftime("%B %d, %Y")
        
        # Build the contact block with name, email, phone, and date
        contact_lines = []
        if name or email or phone:
            if name:
                contact_lines.append(name)
            if email:
                contact_lines.append(email)
            if phone:
                contact_lines.append(phone)
            contact_lines.append('')  # Empty line before date
        
        contact_lines.append(date_str)
        
        return '\n'.join(contact_lines)

    def generate_cover_letter(self, user_profile: Dict[str, Any], job_description: str, 
                           position: str = 'the position', company: str = 'your company') -> str:
        """Generate a personalized cover letter based on user profile and job description.
        
        Args:
            user_profile: Parsed user profile from CV
            job_description: Job description text
            position: The position being applied for
            company: The company name
            
        Returns:
            str: Generated cover letter with contact information
        """
        # Format the contact information
        contact_info = self._format_contact_info(user_profile)
        
        prompt = f"""
Create a professional cover letter following this EXACT format:

{contact_info}

Hiring Manager
{company}
[Location or "Remote"]

Subject: Application for {position} Position

Dear Hiring Manager,

[First paragraph: Express interest in the position and company. Keep it concise and engaging.]

[Second paragraph: Highlight your most relevant experience and skills that match the job requirements.]

[Third paragraph: Showcase specific achievements or projects that demonstrate your qualifications.]

[Fourth paragraph: Express enthusiasm for the opportunity and request an interview. Mention your availability for a call or meeting.]

Sincerely,

{user_profile.get('full_name', 'Your Name')}
{user_profile.get('email', 'your.email@example.com')}
{user_profile.get('phone', '')}

IMPORTANT INSTRUCTIONS:
1. DO NOT include any section headers, labels, or placeholders like [Your Name]
2. Use the exact contact information provided above
3. Keep the tone professional but conversational
4. Focus on how your skills and experience match the job requirements
5. Keep paragraphs concise (3-5 sentences each)
6. Use proper business letter formatting with single spacing between paragraphs
7. Do not include any additional information or sections

JOB DESCRIPTION:
{job_description}

USER PROFILE:
{json.dumps(user_profile, indent=2)}

Now generate the cover letter following the exact format and instructions above. Do not include any placeholders or section headers in the final output.
"""
        return self._get_ai_response(prompt)

    def _get_ai_response(self, prompt: str) -> str:
        """Get response from OpenAI's API.
        
        Args:
            prompt: The prompt to send to the AI
            
        Returns:
            str: The AI's response
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that creates professional documents."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"Failed to generate content: {e}")

# Example usage
if __name__ == "__main__":
    # Example user profile (would come from cvparser.py in real usage)
    example_profile = {
        "full_name": "John Doe",
        "email": "john.doe@example.com",
        "employment": [
            {
                "company": "Tech Corp",
                "position": "Senior Developer",
                "start_date": "2020-01-01",
                "responsibilities": "Led a team of developers, implemented new features, and optimized performance."
            }
        ],
        "education": [
            {
                "degree": "BSc in Computer Science",
                "institution": "University of Technology",
                "end_date": "2019"
            }
        ],
        "technical_skills": ["Python", "JavaScript", "Docker", "AWS"],
        "soft_skills": ["Leadership", "Teamwork", "Problem-solving"]
    }

    example_job_description = """
We are looking for a Senior Developer with experience in Python and cloud technologies.
The ideal candidate has leadership experience and a strong background in software development.
Responsibilities include leading a team, designing system architecture, and implementing new features.
"""

    try:
        generator = CoverLetterGenerator()
        
        print("Generating resume...")
        resume = generator.generate_resume(example_profile, example_job_description)
        print("\n=== GENERATED RESUME ===")
        print(resume)
        
        print("\nGenerating cover letter...")
        cover_letter = generator.generate_cover_letter(example_profile, example_job_description)
        print("\n=== GENERATED COVER LETTER ===")
        print(cover_letter)
        
    except Exception as e:
        print(f"An error occurred: {e}")