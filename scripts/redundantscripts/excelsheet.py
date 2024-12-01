import pandas as pd

# Define columns based on your form structure
columns = [
    "Image Name", "Name", "ID", "Course", "Section", "Semester", "Date", "Faculty",
    "Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9", "Q10", "Total",
    "Student Signature", "Faculty Signature"
]

# Create an empty DataFrame
df = pd.DataFrame(columns=columns)

# Save this as an Excel file
df.to_excel("exam_script_data.xlsx", index=False)
print("Excel file created: exam_script_data.xlsx")
