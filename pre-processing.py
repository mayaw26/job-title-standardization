import pandas as pd

input_path = ""

data = pd.read_excel(input_path)

replacements = {
    "Mgr": "Manager",
    "Mgr.": "Manager",
    "Engr": "Engineer",
    "Engr.": "Engineer",
    "Eng": "Engineer",
    "Eng.": "Engineer",
    "Engrg": "Engineer",
    "Engrg.": "Engineer",
    "Sr": "Senior",
    "Sr.": "Senior",
    "Asst": "Assistant",
    "Asst.": "Assistant",
    "Assoc.": "Associate",
    "Dir": "Director",
    "Dir.": "Director",
    "Dr": "Director",
    "Dr.": "Director",
    "Rep": "Representative",
    "Rep.": "Representative",
    "Exec": "Executive",
    "Exec.": "Executive",
    "VP": "Vice President",
    "V.P.": "Vice President",
    "VP.": "Vice President",
    "CEO": "Chief Executive Officer",
    "C.E.O.": "Chief Executive Officer",
    "CTO": "Chief Technology Officer",
    "CFO": "Chief Financial Officer",
    "COO": "Chief Operating Officer",
    "Assoc Prof": "Associate Professor",
    "Assoc. Prof.": "Associate Professor",
    "Rsch": "Research",
    "Rsch.": "Research",
    "Prof": "Professor",
    "Prof.": "Professor",
    "Grad": "Graduate",
    "Grad.": "Graduate",
    "and": "&",
    "And": "&",
    "AI": "Artificial Intelligence",
    "Devel": "Development",
    "Devel.": "Development",
    "OBGYN": "Obstetrician & Gynecologist",
    "OB/GYN": "Obstetrician & Gynecologist",
    "Ob/Gyn": "Obstetrician & Gynecologist",
    "DVM": "Doctor of Veterinary Medicine",
    "MD": "Medical Doctor",
    "ESL": "English Sign Language",
    "IT": "Information Technology",
    "HR": "Human Resources",
    "Proj": "Project",
    "Proj.": "Project",
    "R&D": "Research & Development",
    "R & D": "Research & Development",
    "GM": "General Manager",
    "QA": "Quality Assurance",
    "Acct": "Accountant",
    "Acct.": "Accountant",
    "QC": "Quality Control",
    "RN": "Registered Nurse",
    "DDS": "Doctor of Dental Surgery",
    "PT": "Physical Therapist",
    "Cust": "Customer",
    "Svc": "Service",
    "Admin": "Administrator",
    "Tech": "Technology",
    "Tech.": "Technology",
    "Ass.": "Assistant",
    "Ass't": "Assistant",
    "Acctg": "Accounting",
    "Acctg.": "Accounting",
    "Ofcr": "Officer",
    "Ofcr.": "Officer",
    "Supt": "Superintendent",
    "Supt.": "Superintendent",
    "Tchr": "Teacher",
    "Tchr.": "Teacher",
    "Cnslt.": "Consultant",
    "Dept.": "Department",
    "Spec.": "Specialist",
    "Spec": "Specialist",
    "Mgmt": "Management",
    "Bus.": "Business",
    "Sci.": "Science",
    "Coord.": "Coordinator",
    "Atty.": "Attorney",
    "Atty": "Attorney",
    "Dir.": "Director",
    "Supv.": "Supervisor",
    "Coord.": "Coordinator",
    "Couns.": "Counsel",
    "In'tl": "International",
    "Elem": "Elementary",
    "Elem.": "Elementary",
    "Kinder": "Kindergarten",
    "kinder": "Kindergarten",
    "first": "1st",
    "First": "1st",
    "second": "2nd",
    "Second": "2nd",
    "third": "3rd",
    "Third": "3rd",
    "fourth": "4th",
    "Fourth": "4th",
    "fifth": "5th",
    "Fifth": "5th",
    "sixth": "6th",
    "Sixth": "6th",
    "seventh": "7th",
    "Seventh": "7th",
    "eighth": "8th",
    "Eighth": "8th",
    "ninth": "9th",
    "Ninth": "9th",
    "tenth": "10th",
    "Tenth": "10th",
    "eleventh": "11th",
    "Eleventh": "11th",
    "twelfth": "12th",
    "Twelfth": "12th",
    "/": " & "
}

# Function to replace abbreviations only if they match whole words
def replace_exact_words(text, replacements):
    if not isinstance(text, str):  # Skip non-string values
        return text
    
    # Normalize spacing and case
    text = text.strip()  # Remove leading/trailing spaces
    words = text.split()  # Split the text into words
    
    # Replace words only if they match a key
    replaced_words = [replacements.get(word, word) for word in words]
    return " ".join(replaced_words)  # Join the words back together

# Apply replacements and update the AFTER_PREPROCESSING column
data['AFTER_PREPROCESSING'] = data['EXISTING_JOB_TITLE'].apply( # UPDATE
    lambda x: replace_exact_words(x, replacements)
)

# Save the updated file
data.to_excel(input_path, index=False)