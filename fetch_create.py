'''importing all the required jira libraries'''

from jira import JIRA
import requests 
import json
import sys 
import os
from requests.auth import HTTPBasicAuth
from jira import JIRA, JIRAError
from jira.exceptions import JIRAError



# Function to generate  jira issue taking inf of different fields

def generate_issue(json_obj, jira_url, email, api_key):
   #url="https://ibm-team-uz9mmme2.atlassian.net//rest/api/2/issue"
   headers={
     "Accept": "application/json",
     "Content-Type": "application/json"
}
   project_key = json_obj["fields"]["project"]["key"]
   issue_summary = json_obj["fields"]["summary"]
   issue_description = issue_summary.split('-')[-1]
   issue_type = json_obj["fields"]["issuetype"]["name"]
   issue_priority = json_obj["fields"]["priority"]["name"]
   issue_component = [component['name'] for component in json_obj["fields"]["components"]]
   issue_labels =  json_obj["fields"]["labels"]
   

   payload=json.dumps(
   {
      "fields": {
         "project":
         {
            "key":project_key
         },
         "summary": issue_summary,
         "description": issue_description,
         "issuetype": {
            "name": issue_type
         } ,
         "priority": {
            "name" : issue_priority 
          } ,
          "labels": issue_labels,
          "components":  [
            {"name": val}
               for val in issue_component]
      }
   }
   )
   response=requests.post(jira_url,headers=headers, data=payload, auth=(email, api_key))
   #data=response.json()
   print(response.status_code)
   if(response.status_code == 201):
     print ('Issue generated successfully')
   else:
      print('failed')
    
   
'''Function to authenticate  the api key and email wtih the given url'''

def get_authenticated(response):
    if response.status_code == 200:
      print ('Data retrieved successfully')
      print (response.status_code)
      return response

    else:
      print (response.status_code)
      print('Error retrieving data:', response.text)


'''Fetching the required data from the user '''

def fetch_data(json_obj):
  try:
    data = json.loads(json_obj.text)
    if(json_obj.status_code == 200):
      # fetching all the required details to create an issue in JIRA
      project_key = data["fields"]["project"]["key"]
      issue_summary = data["fields"]["summary"]
      issue_description = issue_summary.split('-')[-1]
      issue_type = data["fields"]["issuetype"]["name"]
      issue_priority = data["fields"]["priority"]["name"]
      issue_component = [component['name'] for component in data["fields"]["components"]]
      issue_labels = data["fields"]["labels"]

      # displaying all the fetched data
      print("ProjectKey: ",project_key)
      print("Summary: ",issue_summary)
      print("Description: ",issue_description)
      print("IssueType: ",issue_type)
      print("IssuePriority: ",issue_priority)
      print("IssueLabels: ",issue_labels)
      print("IssueComponents: ",issue_component)

      # returns json data in dictionary format
      return data
   
  except JIRAError:
        # Handle JSON decoding error
        print("Error: Unable to decode JSON data")
        print(f"Error: HTTP status code {json_obj.status_code}")
        return None



def main():
    
    # Authenticate to the JIRA server
    #email = "muskan.kumari@ibm.com"
    #api_key = "ATATT3xFfGF0NLTmYfrrBknz_BymaCv3YNOnAkIusmell0sXMMfigOZWKWDo-0JU3JaXjqkyFxCigpppF-eh1RLrAW_rkJir-O4793sN-IY6vAN03goDgXlgBB--WXfjkdVC3OJp-GO1KeJYeXmdW5ofsdpoM3iZ5S-YaGDrhwXQTh9EE0non9o=D99A6AEF"
   # jira_url="https://ibm-team-uz9mmme2.atlassian.net//rest/api/2/issue/TES-9"
  

   #jira_url = input('Enter API url to fetch fields:')
   #mail = input('Enter your email or username:')
   #api_key = input('Enter your jira token password:')

   # Taking inputs from the environment 

   jira_url = os.environ.get('API_URL')
   email = os.environ.get('USERNAME')
   api_key = os.environ.get('PASSWORD')
   
   print("Jira URL: \n",jira_url)
   print("username/ email: \n",email)
   print("access token password: \n",api_key)
   response = requests.get(jira_url, auth = HTTPBasicAuth(email,api_key))
   
   
   # validating the response for the request made
   
   json_obj= get_authenticated(response)
   #print(json.dumps(json_obj,indent=3))
    

   #  Fetching values of different fields for creating jira issue from the programmer
   json_data = fetch_data(json_obj)

   
   # generating new issue on jira taking all the information and passing under the given function

   generate_issue(json_data, "https://ibm-team-uz9mmme2.atlassian.net//rest/api/2/issue", email, api_key)


if __name__== "__main__": 
   main()






   
   
   
  
  