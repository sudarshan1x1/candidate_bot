import pandas as pd
import os

class Model:
    def __init__(self):
        self.df = pd.DataFrame(columns=['Name','Phone no','Email','Location','Education','Field','College','Tech Stack','Work Experience','Designation','Role', 'Choice'])

    def add_profile(self, profileinfo):
        new_row = pd.DataFrame([profileinfo])
        self.df = pd.concat([self.df, new_row], ignore_index=True)

    def save_to_csv(self, filename):
       self.df.to_csv(filename, index=False, mode='a', header=not os.path.exists(filename))


class Job_Description:
    def __init__(self, role):
        self.role = role
        self.descriptions = {
            "AI/ML Intern": {
                "description": "This is the job description for the AI/ML Intern role.",
                "experience": "0-1 year",
                "location": "Remote",
                "tech_stack": ["Python", "TensorFlow", "PyTorch"],
                "education": "Bachelor's Degree in Computer Science or related field",
                "salary": "$30,000 - $40,000"
            },
            "Software Developer Intern": {
                "description": "This is the job description for the Software Developer Intern role.",
                "experience": "0-1 year",
                "location": "On-Location (San Francisco, CA)",
                "tech_stack": [".NET", "C#", "Java"],
               "education": "Bachelor's Degree in Computer Science or related field",
                "salary": "$35,000 - $45,000"
            },
            "AI/ML engineer": {
                "description": "This is the job description for the AI/ML engineer role.",
                "experience": "2-5 years",
                "location": "Hybrid (Remote & On-Location)",
                "tech_stack": ["Python", "TensorFlow", "PyTorch"],
                "education": "Master's Degree in Computer Science or related field",
                "salary": "$60,000 - $70,000"
            },
            "Software Developer Engineer": {
                "description": "This is the job description for the Software Developer Engineer role.",
                "experience": "3-7 years",
                "location": "On-Location (New York, NY)",
                "tech_stack": [".NET", "C#", "Java"],
                "education": "Bachelor's Degree in Computer Science or related field",
                "salary": "$80,000 - $90,000"
            }
        }

    def get_description(self):
        description = self.descriptions[self.role]
        output = f"Role: {self.role}\n"
        output += f"Experience required: {description['experience']}\n"
        output += f"Location: {description['location']}\n"
        output += f"Tech Stack: {', '.join(description['tech_stack'])}\n"
        output += f"Education qualification: {description['education']}\n"
        output += f"Salary: {description['salary']}\n"
        return output