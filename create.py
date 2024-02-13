'''importing all the required jira libraries'''

from jira import JIRA
import requests 
import json
import sys 
from requests.auth import HTTPBasicAuth
from jira import JIRA, JIRAError
from jira.exceptions import JIRAError



# Function to generate  jira issue taking inf of different fields

def generate_issue(json_obj):
   url="https://ibm-team-uz9mmme2.atlassian.net//rest/api/2/issue"
   headers={
     "Accept": "application/json",
     "Content-Type": "application/json"
}
   payload=json.dumps(
   {
      "fields": {
         "project":
         {
            "key": "JN"
         },
         "summary": json_obj['title'] ,
         "description": json_obj['description'] ,
         "issuetype": {
            "name": json_obj['issuetype']
         } ,
         "priority": {
            "name" : json_obj['Priority']
          } ,
          "labels": ["patch_750UP7IF04"]
      }
   }
   )
   response=requests.post(url,headers=headers, data=payload, auth=("muskan.kumari@ibm.com","ATATT3xFfGF0NLTmYfrrBknz_BymaCv3YNOnAkIusmell0sXMMfigOZWKWDo-0JU3JaXjqkyFxCigpppF-eh1RLrAW_rkJir-O4793sN-IY6vAN03goDgXlgBB--WXfjkdVC3OJp-GO1KeJYeXmdW5ofsdpoM3iZ5S-YaGDrhwXQTh9EE0non9o=D99A6AEF"))
   data=response.json()
   print(response.text)
   print ('Issue generated successfully')
    
   
'''Function to authenticate  the api key and email wtih the given url'''

def get_authenticated(response):
    if response.status_code == 200:
      print ('Data retrieved successfully')
      print (response.status_code)
      return response.status_code

    else:
      print('Error retrieving data:', response.text)


      
'''' Function  posting notification on slack'''


def post_slack_notification( json_data):
    slack_message = {"text": f"New jira issue has been created\n Key :{json_data['title']}\n Summary: {json_data['description']}"}

    try:
        webhook_url = "https://ibm.slack.com/team/U06B63UAKAS"    
        response = requests.post(webhook_url, data=json.dumps(slack_message), headers={'Content-Type': 'application/json'})

        if response.status_code == 200:
            print("Slack notification sent successfully.")
        else:
            print(f"Failed to send Slack notification. Status code: {response.status_code}")

    except Exception as e:
        print(f"Error sending Slack notification: {str(e)}")



def main():
    
    # Authenticate to the JIRA server
    email = "muskan.kumari@ibm.com"
    api_key = "ATATT3xFfGF0NLTmYfrrBknz_BymaCv3YNOnAkIusmell0sXMMfigOZWKWDo-0JU3JaXjqkyFxCigpppF-eh1RLrAW_rkJir-O4793sN-IY6vAN03goDgXlgBB--WXfjkdVC3OJp-GO1KeJYeXmdW5ofsdpoM3iZ5S-YaGDrhwXQTh9EE0non9o=D99A6AEF"
    
    url1= "https://ibm-team-uz9mmme2.atlassian.net/jira/servicedesk/projects/JN/queues/custom/1"

    response = requests.get(url1, auth = HTTPBasicAuth(email,api_key))
     
     
     # validating the response for the request made
    
    json_obj= get_authenticated(response)
    print(json.dumps(json_obj,indent=3))


    #  Taking values of different fields for creating jira issue from the programmer
    
    json_data = {'title': 'Sample Issue', 'description': 'This is a sample issue.', 'issuetype': 'Task' , 'Priority': 'High'}
         
    # generating new issue on jira taking all the information and passing under the given function

    generate_issue(json_data)

    # posting notification on slack about the generation of new jira issue

    post_slack_notification(json_data)


if __name__=="__main__": 
    main()






   
   
   
  
  