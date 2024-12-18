Mail Generator using AI

Overview :
This project generates tailored job application emails using AI. 
By scraping job postings from a provided URL and matching the skills with a user's portfolio, 
it creates professional emails aligned with job requirements.

Features :
- Scrapes job postings from career pages.
- Cleans and processes webpage content.
- Matches job-required skills with the user's portfolio.
- Generates professional job application emails.
- Displays results in a clean Streamlit interface.

Setup Instructions : 

1.Clone the Repository: 
git clone <repo_link>
cd <project_directory>

2.Install Dependencies:
pip install -r requirements.txt

3.Configure Environment Variables:
 -Create a .env file :
GROQ_API_KEY='your_api_key_here'
groqcould for api keys link : "https://console.groq.com/keys"

4.Run the Streamlit Application:
streamlit run app/main.py

