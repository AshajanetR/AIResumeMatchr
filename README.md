# Resume AI Agent

An AI-powered resume analyzer that compares resumes to job descriptions and provides insights.

## Features

- Analyzes resume content against job descriptions
- Provides a fit score from 0-100%
- Identifies matched skills from the resume and job description
- Highlights missing or underrepresented skills
- Offers suggestions for improving the resume
- Flags potential issues in the resume
- Provides ATS (Applicant Tracking System) optimization tips

## Installation

1. Clone this repository
2. Create a virtual environment:
   ```
   python -m venv .venv
   ```
3. Activate the virtual environment:
   - Windows: `.venv\Scripts\activate`
   - macOS/Linux: `source .venv/bin/activate`
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Command Line Interface

```bash
python app.py --resume path/to/resume.pdf --job-description path/to/job_description.txt
```

### Options

- `--resume`, `-r`: Path to the resume file (PDF preferred, also supports DOCX)
- `--job-description`, `-j`: Path to a text file containing the job description OR a string with the job description
- `--output`, `-o`: Path to save the analysis results (optional)
- `--no-stream`: Disable streaming output
- `--api-key`, `-k`: Groq API key (if not provided, will use the hardcoded key)

### Examples

1. Analyze a resume with a job description file:
   ```bash
   python app.py -r example_resume.pdf -j example_job_description.txt
   ```

2. Analyze a resume with a job description string:
   ```bash
   python app.py -r example_resume.pdf -j "Senior Developer with 5+ years Python experience..."
   ```

3. Save the analysis to a file:
   ```bash
   python app.py -r example_resume.pdf -j example_job_description.txt --no-stream -o analysis_results.md
   ```

### Using the Example Files

This repository includes sample files for testing:

```bash
# Run with the example files
python app.py -r example_resume.pdf -j example_job_description.txt
```

## Creating a PDF Resume

You can use the included script to generate a sample PDF resume:

```bash
python create_pdf_resume.py
```

This will create a file named `example_resume.pdf` that you can use for testing.

## Supported File Formats

- Resumes: PDF (preferred), DOCX
- Job Descriptions: TXT or command-line string

## Note

This tool uses the Groq LLM API for analysis. 