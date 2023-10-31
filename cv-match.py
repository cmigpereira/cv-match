import io
import os
import PyPDF2
import requests
from bs4 import BeautifulSoup
import streamlit as st
from langchain.llms import AzureOpenAI
from langchain.prompts import PromptTemplate

os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_VERSION"] = "2023-08-01-preview"
os.environ["OPENAI_API_BASE"] = st.secrets["azureopenai"]["AZURE_OPENAI_ENDPOINT"]
os.environ["OPENAI_API_KEY"] = st.secrets["azureopenai"]["AZURE_OPENAI_KEY"]
DEPLOYMENT_NAME = st.secrets["azureopenai"]["AZURE_OPENAI_DEPLOYMENT_NAME"]


def scrape_job_description(url):
    '''
    Scrape text from a URL containing the job description
    '''
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        text = " ".join([p.get_text() for p in soup.find_all("p")])
        return text
    except Exception as e:
        st.error(f"Error scraping URL: {e}")
        return None


def extract_cv_text(file):
    '''
    Extract text from a CV in a PDF format
    '''
    with io.BytesIO(file.getvalue()) as data:
        pdf_reader = PyPDF2.PdfReader(data)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text


def generate_cv_summary(cv_text):
    '''
    Generate a summary of the key information from the CV using the LLM
    '''
    template = """Format the resume below to this YAML template:
    ------
    Name: ''
    Country: ''
    Websites:
    - ''
    Email: ''
    DateBirth: ''
    Education:
    - school: ''
      degree: ''
      field: ''
      startDate: ''
      endDate: ''
    WorkExperience:
    - company: ''
      position: ''
      startDate: ''
      endDate: ''
    Skills:
    - name: ''
    Certifications:
    - name: ''
    Summary: ''
    ------
    {cv}
    """

    prompt = PromptTemplate(
        input_variables=["cv"],
        template=template
    )

    llm = AzureOpenAI(deployment_name=DEPLOYMENT_NAME,
                      model_name="gpt-35-turbo",
                      temperature=0.4,
                      max_tokens=200,
                      top_p=1
                      )

    return llm(prompt.format(cv=cv_text))


def evaluate_fit(cv_text, job_description):
    '''
    Evaluate the candidate's fit for the role
    '''
    template = """Based on the following text containing a Curriculum Vitae:
    {cv}

    And the following text containing a job description:
    {jd}
 
    Advise if this is a good CV for the job. Provide 2-3 sentences justifying your answer.
    """

    prompt = PromptTemplate(
        input_variables=["cv", "jd"],
        template=template
    )
    llm = AzureOpenAI(deployment_name=DEPLOYMENT_NAME,
                      model_name="gpt-35-turbo",
                      max_tokens=300,
                      top_p=1
                      )

    return llm(prompt.format(cv=cv_text, jd=job_description))


def app():
    '''
    The app with the required UI elements and logic
    '''
    st.title("CV Match app")

    # Upload CV
    uploaded_cv = st.file_uploader("Upload your CV (PDF)", type=["pdf"])

    if uploaded_cv:
        # Extract CV text
        cv_text = extract_cv_text(uploaded_cv)
        # Generate and display CV summary
        with st.spinner("Generating Summary..."):
            cv_summary = generate_cv_summary(cv_text)
        st.write("CV Summary:")
        st.write(cv_summary)

    # Input job description URL
    job_url = st.text_input("Enter the job description URL")

    if job_url:
        if job_url == "":
            st.warning("Please enter a job description URL")
        else:
            with st.spinner("Scraping job description..."):
                job_description = scrape_job_description(job_url)
            st.write("Job description scraped!")
            # st.write(job_description)

    evaluate_fit_button = st.button("Evaluate CV fit to the role")

    # Evaluate fit button
    if evaluate_fit_button:
        try:
            with st.spinner("Generating fit evaluation..."):
                fit_evaluation = evaluate_fit(cv_text, job_description)
            # Display the fit evaluation
            st.write("Fit Evaluation:")
            st.write(fit_evaluation)
        except:
            st.warning("Please provide both CV and job description.")


if __name__ == "__main__":
    # Run the Streamlit app
    app()
