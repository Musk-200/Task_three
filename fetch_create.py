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

def generate_issue(json_obj, jira_url, email, api_key, j):
   headers={
     "Accept": "application/json",
     "Content-Type": "application/json"
}
   project_key = "QOPS"
   issue_component = json_obj[j]["name"]
   issue_summary = issue_component.split('-')[-1]+ "-750 UP7 IF04 Patch"
   issue_description = "None"
   issue_type = "Task"
   issue_priority = "High"
   issue_labels = ["interim_fix_750UP7IF04"]
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
          "components": issue_component 
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

def fetch_data(json_obj, j):
  try:
    data = json.loads(json_obj.text)
    if(json_obj.status_code == 200):
      project_key = "QOPS"
      issue_component = data[j]["name"]
      issue_summary = issue_component.split('-')[-1]+ "-750 UP7 IF04 Patch"
      issue_description = "None"
      issue_type = "Task"
      issue_priority = "High"
      issue_labels = ["interim_fix_750UP7IF04"]

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

   #credentials from where api is being fetched
   '''fetch_url = os.environ.get('API_URL')
   fetch_email = os.environ.get('USERNAME')
   fetch_api_key = os.environ.get('PASSWORD')

   # credentials of the location where jira issue is to be generated
   generate_jira_url = os.environ.get('API_URL')
   generate_email = os.environ.get('USERNAME')
   generate_api_key= os.environ.get('PASSWORD')'''

fetch_api = "https://jira.secintel.intranet.ibm.com/rest/api/2/project/QOPS/components/"
fetch_email = "Neha.Singh41@ibm.com"
fetch_api_key = "VfwPFdtKVS80nnH3Mhgqb8P4SQxhhQocYM6VeA"

generate_jira_url = "https://ibm-team-uz9mmme2.atlassian.net/rest/api/2/issue"
generate_email= "muskan.kumari@ibm.com"
generate_api_key= "ATATT3xFfGF0H8mA20P9_bwWZZ1M8S2i4wIk6fJJwMVhAVZUODWFpAL2jgt-EcUXQGYzz9lzLhmK8hGtAyg24Hue8AzefX3FkkrisbXJNKS5GkrZMWlGb0WK10r7vaoqdGrwigYSWncjoIP3TAF1qreKgVHU0sI_76pVf_c6i7ZtDH7t8-IBJ_0=605A6439"


response = requests.get(fetch_api, auth = HTTPBasicAuth(fetch_email,fetch_api_key))
   
   
   # validating the response for the request made by calling it in get_authenticated()  function
json_obj= get_authenticated(response)

try:
#using loop to generate required number of issues
  payload = json.loads(json_obj.text)
  if payload:
   for j in range(9):
     if(payload[j]["archived"] == "false"):
#  Fetching values of different fields for creating jira issue under fetch_data() function and storing those data 
      json_data = fetch_data(json_obj, j)
# print(j)
# generating new issue on jira after passing under the given function name 
      generate_issue(json_data, generate_jira_url, generate_email, generate_api_key, j)

  else:
   print("Could not fetch data")

except JIRAError:
     print("Error:", json_obj.status_code)


if __name__== "__main__": 
   main()






   
   
   
  
  