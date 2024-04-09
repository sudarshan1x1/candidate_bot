import pandas as pd
import os

class Model:
    def __init__(self):
        self.df = pd.DataFrame(columns=['Name', 'Phone no', 'Email', 'Education', 'Field', 'Designation', 'Work Experience', 'Role', 'Tech Stack', 'Location', 'Current Salary'])

    def add_profile(self, profileinfo):
        new_row = pd.DataFrame([profileinfo])
        self.df = pd.concat([self.df, new_row], ignore_index=True)

    def save_to_csv(self, filename):
       self.df.to_csv(filename, index=False, mode='a', header=not os.path.exists(filename))
       