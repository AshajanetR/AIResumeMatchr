import argparse
import os
from agent import ResumeAIAgent

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Resume Analysis AI Agent')
    parser.add_argument('--resume', '-r', required=True, 
                       help='Path to the resume file (PDF preferred, also supports DOCX)')
    parser.add_argument('--job-description', '-j', required=True, 
                        help='Path to a text file containing the job description OR a string with the job description')
    parser.add_argument('--output', '-o', help='Path to save the analysis results (optional)')
    parser.add_argument('--no-stream', action='store_true', help='Disable streaming output')
    parser.add_argument('--mock', '-m', action='store_true', help='Use mock model (no API key required)')
    parser.add_argument('--api-key', '-k', help='Groq API key (if not provided, will use the hardcoded key)')
    return parser.parse_args()

def read_job_description(job_description_input):
    """Read job description from file if it's a file path, otherwise return the input as is."""
    if os.path.exists(job_description_input) and os.path.isfile(job_description_input):
        with open(job_description_input, 'r', encoding='utf-8') as file:
            return file.read()
    return job_description_input

def save_results(results, output_path):
    """Save analysis results to a file."""
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write("# Resume Analysis Results\n\n")
        
        # Add a prominent match percentage section at the top
        if results.get("fit_score"):
            file.write(f"# 🎯 MATCH PERCENTAGE: {results['fit_score']}%\n\n")
            file.write("---\n\n")
        
        # Check if we have structured data or just the full response
        if "full_response" in results and (results.get("fit_score") is None or 
                                         all(len(v) == 0 for v in [results.get(k, []) for k in 
                                                                 ["matched_skills", "missing_skills", 
                                                                  "improvement_suggestions", "red_flags", 
                                                                  "ats_optimization"]])):
            # Just write the full response if parsing failed
            if isinstance(results["full_response"], list):
                for paragraph in results["full_response"]:
                    file.write(f"{paragraph}\n\n")
            else:
                file.write(results["full_response"])
        else:
            # Write Fit Score again in the detailed section
            if results.get("fit_score"):
                file.write(f"## Fit Score: {results['fit_score']}%\n\n")
            
            # Write other sections
            sections = {
                "matched_skills": "## Matched Skills",
                "missing_skills": "## Missing or Weak Skills",
                "improvement_suggestions": "## Improvement Suggestions",
                "red_flags": "## Resume Red Flags",
                "ats_optimization": "## ATS Optimization Tips"
            }
            
            for key, title in sections.items():
                file.write(f"{title}\n\n")
                if results.get(key):
                    for item in results[key]:
                        file.write(f"- {item}\n")
                file.write("\n")

def main():
    """Main function to run the Resume AI Agent."""
    args = parse_arguments()
    
    # Check if resume file exists
    if not os.path.exists(args.resume) or not os.path.isfile(args.resume):
        print(f"Error: Resume file '{args.resume}' does not exist or is not a valid file.")
        return
    
    # Initialize the agent
    agent = ResumeAIAgent(use_mock=args.mock, api_key=args.api_key)
    
    # Read job description
    job_description = read_job_description(args.job_description)
    
    # Analyze resume
    stream = not args.no_stream
    results = agent.analyze_resume(args.resume, job_description, stream=stream)
    
    # Save results if output path is provided
    if args.output and not stream:
        save_results(results, args.output)
        print(f"Analysis results saved to {args.output}")

if __name__ == "__main__":
    main()
