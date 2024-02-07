import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import re
import time

# Function to extract skills from job description
def extract_skills(description):
    skills = []

    # List of skills to search for
    skill_list = ['HTML', 
                  'CSS', 
                  'JavaScript',
                  'MS Excel',
                  'Microsoft Office', 
                  'communication',
                  'technical',
                  'analytical', 
                  'teamwork', 
                  'problem-solving', 
                  'leadership', 
                  'time management', 
                  'creativity'
                  'interpersonal skill',
                  'presentation skill', ]
    
    # Iterate over each skill and check if it's mentioned in the description
    for skill in skill_list:
        if re.search(skill, description, re.IGNORECASE):
            skills.append(skill)
    return skills

def get_job_links(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            # Find all the job links on the page
            job_links = [urljoin('https://xpress.jobs', a['href']) for a in soup.find_all('a', class_='job_listing-clickbox')]
            return job_links
        else:
            print(f"Error: Unable to fetch content. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# Example usage
url = 'https://www.xpress.jobs/jobs?page=4'
job_links = get_job_links(url)
job_details = []

for job_link in job_links:
    response = requests.get(job_link)
    soup = BeautifulSoup(response.content, 'html.parser')

    titles = soup.find('h2', class_='page-title').text.strip()
    company = soup.find('h3').text.strip()
    overview_description = soup.find('div', class_='job-overview job-overview-div').text.strip()
    description = soup.find('div', class_='job_listing-description job-overview col-md-9 col-sm-12').text.strip()
    skills = extract_skills(description)

    job_details.append({ 'title': titles,
                         'company': company,
                         'description': overview_description, 
                         'job_link': job_link,  
                         'skills': skills})

# Pause execution for 3 second
time.sleep(3)

# Print in json format
print(json.dumps(job_details, indent=2))

