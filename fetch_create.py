'''importing all the required libraries'''
from jira import JIRA
import requests 
import json
import sys 
import os
from requests.auth import HTTPBasicAuth
from jira import JIRA, JIRAError
from jira.exceptions import JIRAError

'''Function to generate  jira issue after getting values of all the fields through jira API'''

def generate_issue(json_obj, jira_url, email, api_key):
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
    
'''Function to authenticate the api_key and email wtih the given url for making a valid credential entry'''

def get_authenticated(response):
    if response.status_code == 200:
      print ('Data retrieved successfully')
      print (response.status_code)
      return response
    else:
      print (response.status_code)
      print('Error retrieving data:', response.text)

'''Function created to fetch the values of different fields from the user API '''

def fetch_data(json_obj):
  try:
    data = json.loads(json_obj.text)
    if(json_obj.status_code == 200):
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

      return data
   
  except JIRAError:
        print("Error: Unable to decode JSON data")
        print(f"Error: HTTP status code {json_obj.status_code}")
        return None


def main(): 

   '''jira_url = os.environ.get('API_URL')
   email = os.environ.get('USERNAME')
    api_key= os.environ.get('PASSWORD')'''

   jira_url = input("Enter api_url")
   email = input("Enter your username")
   api_key= input("Enter your password")

   response = requests.get(jira_url, auth = HTTPBasicAuth(email,api_key))
   
   
   # validating the response for the request made by calling it in get_authenticated()  function
   json_obj= get_authenticated(response)

   #  Fetching values of different fields for creating jira issue under fetch_data() function and storing those data
   json_data = fetch_data(json_obj)

   # generating new issue on jira after passing under the given function name 
   generate_issue(json_data, "https://ibm-team-uz9mmme2.atlassian.net//rest/api/2/issue", email, api_key)


if __name__== "__main__": 
   main()






   
   
   
  
  