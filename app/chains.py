import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Chain:
    def __init__(self):
        # Initialize the language model (LLM) with specified parameters
        self.llm = ChatGroq(
            temperature=0,  # Set the LLM's response determinism (0 = most deterministic)
            groq_api_key=os.getenv("GROQ_API_KEY"),  # Retrieve API key from environment variables
            model_name="llama-3.1-70b-versatile"  # Specify the LLM model version to use
        )
    
    def extract_jobs(self, cleaned_text):
        """
        Extracts job postings from the provided cleaned text and returns them in JSON format.
        
        Args:
            cleaned_text (str): The text scraped from a careers page.

        Returns:
            list: A list of job postings in JSON format, with keys:
                  - role
                  - experience
                  - skills
                  - description
        """
        # Define the prompt template for extracting job postings
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        # Chain the prompt template with the LLM
        chain_extract = prompt_extract | self.llm

        # Pass the input data (scraped text) to the chain
        res = chain_extract.invoke(input={"page_data": cleaned_text})

        try:
            # Parse the LLM's response as JSON using the JsonOutputParser
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            # Raise an exception if the response is too large or cannot be parsed
            raise OutputParserException("Context too big. Unable to parse jobs.")

        # Ensure the output is returned as a list (if it's a single job, wrap it in a list)
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links):
        """
        Generates a personalized email for a given job posting.
        
        Args:
            job (dict): A dictionary containing job details such as role, experience, skills, and description.
            links (list): A list of relevant links to include in the email.

        Returns:
            str: A formatted email tailored to the job description.
        """
        # Define the prompt template for generating the email
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            You are an agent called Classy_Job_AI. 
            Classy_Job_AI helps in standing out by tailoring their job applications using AI and ML tools to match their skills with the most relevant job opportunities.
            Your job is to help in applying for a role of demonstrating and highlighting their skills, experiences, and enthusiasm for the role.
            You should emphasize the condidates's alignment with the job requirements and explain why they are the ideal candidate.
            show in bullets that they have the required skills.
            keep in mind a good stucture of the email and make sure each line dont have more than 20 word if so go back to a new line .
            be realistic , you dont have to be perfect in all the needed skills .
            ### EMAIL (NO PREAMBLE):

            """
        )
        # Chain the prompt template with the LLM
        chain_email = prompt_email | self.llm

        # Pass the job description and links to the chain
        res = chain_email.invoke({"job_description": str(job), "link_list": links})

        # Return the generated email content
        return res.content

if __name__ == "__main__":
    # Print the Groq API key to verify it's loaded correctly
    print(os.getenv("GROQ_API_KEY"))
