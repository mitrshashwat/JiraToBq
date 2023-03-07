import requests
import json
from google.cloud import bigquery
import os

url = 'https://XXX.atlassian.net/rest/api/3/search/'

# Set the headers
headers = {
    'Content-Type': 'application/json'
}

max_results = 100
start_at = 0

# Set the query parameters
params = {
    'maxResults': max_results
}


# Construct a BigQuery client object.
client = bigquery.Client()

# Set up BigQuery Client
dataset_id = "<your_dataset_id>"
table_ref = client.dataset(dataset_id).table("jira_ticket_data")
table_id = client.get_table(table_ref)


# Get the authentication credentials from environment
username = os.getenv(JIRA_USERNAME, default=None)
password = os.getenv(JIRA_PASSWORD, default=None)

# Set the initial issue variables
all_issues = []
total_issues = None

# Send the GET request with basic authentication and store the response in a variable
response = requests.get(url, headers=headers, params=params, auth=(username, password))

# Convert the response content to JSON
response_json = json.loads(response.content)

total_issues = response_json['total']
print(total_issues)

while start_at < total_issues:
    # Send the GET request with basic authentication and store the response in a variable
    response = requests.get(url, headers=headers, params={'maxResults': max_results, 'startAt': start_at}, auth=(username, password))

    # Convert the response content to JSON
    response_json = json.loads(response.content)

    # Extract the response from the JSON data
    search_results = response_json['issues']
    
    # Add the issues to the list of all issues
    all_issues.extend(search_results)
    
    # Update the startAt parameter for the next request
    start_at += max_results

rows_to_insert = []

# Extract and print the relevant data from each issue, handling null values
for issue in all_issues:
    issue_id = issue['id']
    issue_key = issue['key']
    points = issue['fields'].get('customfield_10016', None)
    status = issue['fields']['status']['name']
    project = issue['fields']['project']['name']
    sprint = issue['fields']['customfield_10020'][-1].get('name', None) if issue['fields'].get('customfield_10020', None) else None
    assignee_name = issue['fields']['assignee'].get('displayName', None) if issue['fields'].get('assignee', None) else None
    #print(f'Issue ID: {issue_id},Status: {status}, Issue Key: {issue_key}, Points: {points}, Assignee Name: {assignee_name}, Last Active Sprint: {sprint}')
    rows_to_insert.append((issue_id, issue_key, points, assignee_name, status, sprint, project))


errors = client.insert_rows(table_id, rows_to_insert, row_ids=[str(issue[0]) for issue in rows_to_insert])  # Make an API request.
if errors == []:
    print("New rows have been added.")
else:
    print("Encountered errors while inserting rows: {}".format(errors))
