from typing import Dict, Optional, List, Any
import os
from agno.agent import Agent, RunResponse
from agno.models.groq import Groq
import PyPDF2
from io import StringIO
import re
import docx

class MockModel:
    """A mock model for testing without API keys."""
    
    def __init__(self, id="mock"):
        self.id = id
        self.functions = []
    
    def response_stream(self, messages):
        """Mock response stream that returns a sample analysis."""
        # This is a simplified mock response for testing purposes
        mock_response = f"""
Fit Score: 80%

Matched Skills:
- Python programming
- JavaScript
- React
- AWS experience
- Cloud platforms
- Database knowledge
- Problem-solving skills
- Cross-functional collaboration
- Code reviews

Missing or Weak Skills:
- Only 4 years experience vs. required 5+ years
- No explicit mention of Django or Flask
- Limited DevOps experience
- No mention of microservices architecture
- No explicit mention of CI/CD pipelines

Improvement Suggestions:
- Highlight Python and JavaScript experience more prominently
- Add specific Django or Flask projects or experience
- Quantify your cloud platform experience more clearly
- Emphasize your mentoring experience with concrete examples
- Add specific examples of complex problem-solving

Resume Red Flags:
- Resume lacks specificity in some technical skills
- Experience section could use more metrics and achievements
- Missing information about specific cloud services experience
- Portfolio or GitHub projects could be highlighted better

ATS Optimization Tips:
- Add more keywords from the job description
- Use standard section headings for better parsing
- Ensure technical skills section aligns with job requirements
- Add a skills summary at the top matched to this position
- Consider using a more ATS-friendly format
"""
        
        # Simulate streaming response by yielding chunks
        words = mock_response.split()
        current_chunk = ""
        
        for word in words:
            current_chunk += word + " "
            if len(current_chunk) > 30:  # Arbitrary chunk size
                yield RunResponse(role="assistant", content=current_chunk)
                current_chunk = ""
        
        if current_chunk:
            yield RunResponse(role="assistant", content=current_chunk)
    
    def response(self, messages):
        """Mock response method that returns a single response."""
        mock_response = """
Fit Score: 80%

Matched Skills:
- Python programming
- JavaScript
- React
- AWS experience
- Cloud platforms
- Database knowledge
- Problem-solving skills
- Cross-functional collaboration
- Code reviews

Missing or Weak Skills:
- Only 4 years experience vs. required 5+ years
- No explicit mention of Django or Flask
- Limited DevOps experience
- No mention of microservices architecture
- No explicit mention of CI/CD pipelines

Improvement Suggestions:
- Highlight Python and JavaScript experience more prominently
- Add specific Django or Flask projects or experience
- Quantify your cloud platform experience more clearly
- Emphasize your mentoring experience with concrete examples
- Add specific examples of complex problem-solving

Resume Red Flags:
- Resume lacks specificity in some technical skills
- Experience section could use more metrics and achievements
- Missing information about specific cloud services experience
- Portfolio or GitHub projects could be highlighted better

ATS Optimization Tips:
- Add more keywords from the job description
- Use standard section headings for better parsing
- Ensure technical skills section aligns with job requirements
- Add a skills summary at the top matched to this position
- Consider using a more ATS-friendly format
"""
        return RunResponse(role="assistant", content=mock_response)
    
    def get_functions(self):
        """Return empty functions list for compatibility."""
        return self.functions
    
    def invoke(self, messages):
        """Mock invoke method."""
        return self.response(messages).content
    
    def invoke_stream(self, messages):
        """Mock invoke_stream method."""
        for chunk in self.response_stream(messages):
            yield chunk.content

class ResumeAIAgent:
    def __init__(self, model=None, use_mock=False, api_key=None):
        """
        Initialize the Resume AI Agent.
        
        Args:
            model: The LLM model to use (defaults to Groq)
            use_mock: Whether to use a mock model (for testing without API keys)
            api_key: Groq API key (if provided, overrides environment variable)
        """
        # Hardcoded API key
        DEFAULT_API_KEY = "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"
        
        if use_mock:
            self.agent = Agent(model=MockModel(), markdown=True)
        else:
            # Set API key - prioritize parameter, then hardcoded key
            os.environ["GROQ_API_KEY"] = api_key or DEFAULT_API_KEY
            self.agent = Agent(model=model or Groq(id="llama-3.3-70b-versatile"), markdown=True)
        
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text content from a PDF file with enhanced handling."""
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                
                # Get metadata if available
                metadata = {}
                if reader.metadata:
                    metadata = reader.metadata
                    
                # Process each page
                for page_num, page in enumerate(reader.pages):
                    page_text = page.extract_text()
                    if page_text.strip():
                        text += page_text + "\n\n"  # Add double newline between pages
                    else:
                        print(f"Warning: Page {page_num+1} appears to be empty or contains only images.")
                
                # If no text was extracted, try to use OCR (placeholder for future improvement)
                if not text.strip():
                    print("Warning: No text extracted from PDF. The file might be scanned or image-based.")
                    text = "⚠️ Note: This PDF appears to be image-based and text couldn't be extracted."
                
            print(f"Successfully extracted {len(text.split())} words from PDF")
            return text
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""
    
    def extract_text_from_docx(self, docx_path: str) -> str:
        """Extract text content from a DOCX file."""
        try:
            doc = docx.Document(docx_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            print(f"Error extracting text from DOCX: {e}")
            return ""
    
    def read_text_file(self, file_path: str) -> str:
        """Read text from a plain text file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Error reading text file: {e}")
            return ""
    
    def extract_resume_content(self, file_path: str) -> str:
        """Extract content from a resume file (PDF preferred)."""
        if file_path.lower().endswith('.pdf'):
            return self.extract_text_from_pdf(file_path)
        elif file_path.lower().endswith('.docx'):
            print("Note: PDF format is preferred for resumes. Processing DOCX file...")
            return self.extract_text_from_docx(file_path)
        else:
            print(f"Unsupported file format: {file_path}")
            print("Please provide a PDF resume for best results.")
            return ""
    
    def analyze_resume(self, resume_path: str, job_description: str, stream: bool = False) -> Dict:
        """
        Analyze a resume against a job description.
        
        Args:
            resume_path: Path to the resume file
            job_description: The job description text
            stream: Whether to stream the response
            
        Returns:
            Analysis results including fit score, matched skills, missing skills,
            improvement suggestions, red flags, and ATS optimization tips
        """
        resume_text = self.extract_resume_content(resume_path)
        if not resume_text:
            return {"error": "Could not extract text from resume"}
        
        prompt = f"""
        I need you to analyze a resume against a job description. Provide the following:
        
        1. Fit Score (0-100%) - How well does this resume match the job description? THIS IS VERY IMPORTANT - PLEASE START YOUR RESPONSE WITH A CLEAR PERCENTAGE NUMBER.
        2. Matched Skills - List all skills in the resume that match those in the job description.
        3. Missing or Weak Skills - What important skills are missing or underrepresented?
        4. Improvement Suggestions - How can the candidate tailor their resume for this job?
        5. Resume Red Flags (if any) - Point out vague language, outdated info, or formatting issues.
        6. ATS Optimization Tips - Is this resume suitable for automated screening systems?
        
        Resume:
        ```
        {resume_text}
        ```
        
        Job Description:
        ```
        {job_description}
        ```
        
        Provide a detailed analysis under each of the 6 categories above. Start with a clear Fit Score percentage.
        """
        
        if stream:
            response = self.agent.run(prompt, stream=True)
            print("Resume Analysis Results:")
            full_response = ""
            for chunk in response:
                chunk_text = chunk.content
                print(chunk_text, end='', flush=True)
                full_response += chunk_text
            print("\n")
            parsed_result = self.parse_analysis_response(full_response)
            # Print fit score prominently if found
            if parsed_result.get("fit_score"):
                print(f"\n===== MATCH PERCENTAGE: {parsed_result['fit_score']}% =====\n")
            return {"status": "Analysis streamed to console", "full_response": full_response}
        else:
            # For non-streaming mode, we need to collect all chunks
            response = self.agent.run(prompt, stream=False)
            if isinstance(response, RunResponse):
                result = response.content
            else:
                # If it's already an iterable of chunks
                result = ""
                for chunk in response:
                    result += chunk.content
            parsed_result = self.parse_analysis_response(result)
            # Print fit score prominently if found
            if parsed_result.get("fit_score"):
                print(f"\n===== MATCH PERCENTAGE: {parsed_result['fit_score']}% =====\n")
            return parsed_result
    
    def parse_analysis_response(self, response: str) -> Dict:
        """Parse the LLM response into a structured format."""
        analysis = {
            "fit_score": None,
            "matched_skills": [],
            "missing_skills": [],
            "improvement_suggestions": [],
            "red_flags": [],
            "ats_optimization": []
        }
        
        # Extract fit score - try multiple regex patterns to capture various formats
        fit_score_patterns = [
            r"Fit Score[:\s-]*(\d+)[%\s]*",                   # Standard format: "Fit Score: 80%"
            r"MATCH PERCENTAGE[:\s-]*(\d+)[%\s]*",            # Our requested format
            r"^[\s\*]*(\d+)[%\s]*",                           # If it starts with just a number
            r"[\s\*]*(\d+)%[\s\*]*match",                     # "80% match"
            r"match.*?[\s\*]*(\d+)%",                         # "match of 80%"
            r"score.*?[\s\*]*(\d+)%",                         # "score of 80%"
            r"percentage.*?[\s\*]*(\d+)%",                    # "percentage of 80%"
            r".*?(\d{1,3})%.*?fit",                           # Anything with a number and % near "fit"
            r".*?fit.*?(\d{1,3})%"                            # Anything with "fit" and a number with %
        ]
        
        for pattern in fit_score_patterns:
            fit_score_match = re.search(pattern, response, re.IGNORECASE | re.DOTALL)
            if fit_score_match:
                try:
                    score = int(fit_score_match.group(1))
                    if 0 <= score <= 100:  # Validate the score is a percentage
                        analysis["fit_score"] = score
                        break
                except (ValueError, IndexError):
                    continue
        
        # Simple extraction of sections (could be improved with more robust parsing)
        sections = {
            "matched_skills": r"Matched Skills(.*?)(?:Missing or Weak Skills|$)",
            "missing_skills": r"Missing or Weak Skills(.*?)(?:Improvement Suggestions|$)",
            "improvement_suggestions": r"Improvement Suggestions(.*?)(?:Resume Red Flags|$)",
            "red_flags": r"Resume Red Flags(.*?)(?:ATS Optimization Tips|$)",
            "ats_optimization": r"ATS Optimization Tips(.*?)$"
        }
        
        for key, pattern in sections.items():
            match = re.search(pattern, response, re.DOTALL | re.IGNORECASE)
            if match:
                content = match.group(1).strip()
                # Convert to list items if content contains bullet points
                if "•" in content or "-" in content:
                    items = re.split(r"\s*[•-]\s*", content)
                    analysis[key] = [item.strip() for item in items if item.strip()]
                else:
                    analysis[key] = [content]
        
        # If we couldn't parse structured data, save the full response
        if all(len(v) == 0 for v in analysis.values() if isinstance(v, list)) and analysis["fit_score"] is None:
            # Fallback: just split by double newlines to get paragraphs
            paragraphs = [p.strip() for p in response.split("\n\n") if p.strip()]
            analysis["full_response"] = paragraphs
            
            # Try to distribute paragraphs to sections
            section_titles = ["Fit Score", "Matched Skills", "Missing Skills", "Improvement Suggestions", 
                             "Resume Red Flags", "ATS Optimization"]
            
            for i, paragraph in enumerate(paragraphs):
                # Try to determine which section this belongs to
                for section, title in zip(analysis.keys(), section_titles):
                    if title.lower() in paragraph.lower():
                        analysis[section] = [paragraph]
                        break
        
        return analysis
    
    def print_response(self, resume_path: str, job_description: str, stream: bool = True):
        """Print the analysis response to the console."""
        return self.analyze_resume(resume_path, job_description, stream=stream)

# Example usage
if __name__ == "__main__":
    resume_agent = ResumeAIAgent()
    
    # Sample usage
    resume_path = "path/to/resume.pdf"  # Replace with actual path
    job_description = """
    Job Description: Senior Software Engineer
    
    Required Skills:
    - Python programming (5+ years)
    - Cloud computing (AWS, Azure, or GCP)
    - Database design and management
    - API development
    - Agile methodologies
    
    Responsibilities:
    - Design and implement scalable software solutions
    - Collaborate with cross-functional teams
    - Mentor junior developers
    - Contribute to architecture decisions
    """
    
    resume_agent.print_response(resume_path, job_description)