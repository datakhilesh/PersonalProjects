import streamlit as st
from PyPDF2 import PdfReader

st.markdown("""
# 📝 AI-Powered Cover Letter Generator

Generate a cover letter. All you need to do is:
1. Upload your resume or copy your resume/experiences
2. Paste a relevant job description
3. Input some other relevant user/job data
"""
)

# radio for upload or copy-paste option
res_format = st.radio(
    "Do you want to upload or paste your resume/key experience",
    ('Upload', 'Paste'))

if res_format == 'Upload':
    # upload_resume
    res_file = st.file_uploader('📁 Upload your resume in pdf format')
    if res_file:
        pdf_reader = PdfReader(res_file)

        # Collect text from pdf
        res_text = ""
        for page in pdf_reader.pages:
            res_text += page.extract_text()
else:
    res_text = st.text_input('Pasted resume elements')

with st.form('input_form'):
    # other inputs
    job_desc = st.text_input('Pasted job description')
    user_name = st.text_input('Your name')
    company = st.text_input('Company name')
    manager = st.text_input('Hiring manager')
    role = st.text_input('Job title/role')
    referral = st.text_input('How did you find out about this opportunity?')
    ai_temp = st.number_input('AI Temperature (0.0-1.0) Input how creative the API can be', value=0.99)

    # submit button
    submitted = st.form_submit_button("Generate Cover Letter")

# if the form is submitted, generate the cover letter
if submitted:
    # replace placeholders with actual content
    specific_skills = "your specific skills here"
    relevant_experience = "your relevant experience here"

    # generate cover letter using GPT-3.5-turbo within the app
    response_out = f"""
    Dear {manager},

    My name is {user_name}, and I am writing to express my interest in the {role} position at {company}. I learned about this opportunity through {referral}, and after reviewing the job description, I am confident that my skills and experiences align well with the requirements.

    In the second paragraph, I would like to highlight the strong parallels between my resume and the qualifications outlined in the job description. My background in {specific_skills} and {relevant_experience} uniquely position me to contribute effectively to your team.

    In conclusion, I am excited about the prospect of joining {company} and contributing to the success of the {role} team. I have attached my resume for your reference, and I would welcome the opportunity to discuss further how my skills and experiences make me an ideal candidate for this position.

    Thank you for considering my application. I look forward to the possibility of discussing my candidacy further.

    Sincerely,
    {user_name}
    """

    st.write(response_out)

    # include an option to download a txt file
    st.download_button('Download the cover_letter', response_out)
