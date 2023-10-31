# CV Match app
 
This is a Streamlit app that allows users to upload a CV and then obtain a summary of the CV from a Large-Language Model (LLM), using Azure Open AI. 
If the user also enters an URL containing a job description, the LLM evaluates the candidate's fit for the role.

# Installation
 
You can install the required libraries using:
```
pip install requirements.txt
```

# Configuration

To use the app, you will need to configure the following secrets in your Streamlit app's configuration:
```
[azureopenai]
AZURE_OPENAI_ENDPOINT = "https://<your_endpoint>.openai.azure.com/"
AZURE_OPENAI_KEY = "<your_key>"
AZURE_OPENAI_DEPLOYMENT_NAME = "<your_deployment_name>"
```
You can set these secrets in a secrets.toml file in a folder called .streamlit (i.e., `.streamlit/secrets.toml`) or in the "Secrets" tab of your Streamlit app's configuration.

# Usage

To run the app, run the following command:
```
streamlit run cv-match.py
```

This will start a Streamlit server and launch the app in your browser.

When the app starts, you can upload a CV in PDF format by clicking the "Upload your CV (PDF)" button and selecting a PDF file. The app will extract the text from the CV, generate a summary of the key information using an Azure OpenAI LLM, and display the summary in the app.

You can then enter a job description URL in the text input box and press enter, and then click the "Evaluate CV fit to the role" button to evaluate the candidate's fit for the role using an Azure OpenAI LLM. The app will scrape the job description from the URL, generate a prompt for the LLM to evaluate the fit, and display the LLM's response in the app.