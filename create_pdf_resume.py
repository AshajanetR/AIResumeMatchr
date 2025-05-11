from fpdf import FPDF

def create_sample_resume():
    pdf = FPDF()
    pdf.add_page()
    
    # Set fonts
    pdf.set_font("Arial", "B", 16)
    
    # Header
    pdf.cell(190, 10, "JOHN DEVELOPER", 0, 1, "C")
    pdf.set_font("Arial", "", 10)
    pdf.cell(190, 5, "123 Coding Lane, Tech City, TC 12345", 0, 1, "C")
    pdf.cell(190, 5, "johndeveloper@email.com | (555) 123-4567", 0, 1, "C")
    pdf.cell(190, 5, "linkedin.com/in/johndeveloper | github.com/johndeveloper", 0, 1, "C")
    pdf.ln(5)
    
    # Summary
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, "SUMMARY", 0, 1)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(190, 5, "Dedicated software engineer with 4 years of experience developing web applications and services. Skilled in Python, JavaScript, and cloud technologies with a focus on building scalable and maintainable solutions.")
    pdf.ln(5)
    
    # Skills
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, "SKILLS", 0, 1)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(190, 5, "Programming Languages: Python, JavaScript, HTML, CSS, SQL\nFrameworks & Libraries: React, Express.js, Node.js, Bootstrap\nDatabase Systems: MongoDB, MySQL, PostgreSQL\nTools & Platforms: Git, Docker, AWS (EC2, S3, Lambda), Linux\nMethodologies: Agile, Scrum, Test-Driven Development")
    pdf.ln(5)
    
    # Experience
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, "EXPERIENCE", 0, 1)
    
    # Job 1
    pdf.set_font("Arial", "B", 11)
    pdf.cell(190, 8, "Software Engineer", 0, 1)
    pdf.set_font("Arial", "I", 10)
    pdf.cell(190, 6, "TechStart Solutions | June 2020 - Present", 0, 1)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(190, 5, "- Developed and maintained multiple RESTful APIs using Python and Flask, improving system response time by 30%\n- Implemented frontend features using React and Redux, enhancing user experience and engagement\n- Collaborated with cross-functional teams to implement new features and troubleshoot issues\n- Utilized AWS services (EC2, S3, RDS) to deploy and scale applications\n- Participated in code reviews to ensure code quality and mentor junior developers")
    pdf.ln(3)
    
    # Job 2
    pdf.set_font("Arial", "B", 11)
    pdf.cell(190, 8, "Junior Developer", 0, 1)
    pdf.set_font("Arial", "I", 10)
    pdf.cell(190, 6, "CodeCraft Inc. | August 2018 - May 2020", 0, 1)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(190, 5, "- Assisted in the development of an e-commerce platform using MERN stack\n- Created and maintained documentation for API endpoints and database schemas\n- Implemented responsive designs using CSS and Bootstrap\n- Participated in daily stand-ups and sprint planning meetings\n- Fixed bugs and optimized existing codebase")
    pdf.ln(5)
    
    # Education
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, "EDUCATION", 0, 1)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(190, 8, "Bachelor of Science in Computer Science", 0, 1)
    pdf.set_font("Arial", "I", 10)
    pdf.cell(190, 6, "Tech State University | Graduated: May 2018", 0, 1)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(190, 5, "- GPA: 3.8/4.0\n- Relevant Coursework: Data Structures, Algorithms, Database Systems, Web Development\n- Senior Project: Developed a task management application using Python and Django")
    pdf.ln(5)
    
    # Projects
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, "PROJECTS", 0, 1)
    
    # Project 1
    pdf.set_font("Arial", "B", 11)
    pdf.cell(190, 8, "Weather Forecast Application", 0, 1)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(190, 5, "- Built a responsive weather application using React and OpenWeather API\n- Implemented geolocation features and local storage for saved locations\n- Deployed application using Netlify with CI/CD pipeline")
    pdf.ln(3)
    
    # Project 2
    pdf.set_font("Arial", "B", 11)
    pdf.cell(190, 8, "Task Management System", 0, 1)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(190, 5, "- Developed a full-stack task management system using MERN stack\n- Implemented user authentication, task assignment, and notification features\n- Utilized Socket.io for real-time updates")
    pdf.ln(5)
    
    # Certifications
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, "CERTIFICATIONS", 0, 1)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(190, 5, "- AWS Certified Developer Associate (2021)\n- MongoDB Certified Developer (2020)")
    pdf.ln(3)
    
    # References
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, "REFERENCES", 0, 1)
    pdf.set_font("Arial", "", 10)
    pdf.cell(190, 5, "Available upon request", 0, 1)
    
    # Save the PDF
    pdf.output("example_resume.pdf")
    print("Created example_resume.pdf successfully!")

if __name__ == "__main__":
    create_sample_resume() 