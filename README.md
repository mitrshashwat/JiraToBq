# JiraToBq
This python script is sending data from Jira API to BigQuery in Google cloud

#Requirements
- Install google-cloud-bigquery and json package in pip3
- Either machine you are deploying script on should have BigQuery write Access or you can use Credentials of a service account via google-cloud-sdk to insert into BQ(refer this article:https://cloud.google.com/docs/authentication/application-default-credentials)
- Create a dataset with desired schema and use it in 'dataset_id' variable

#Perks
- Deploy it as a cron and just forget about it, it will handle data replication in BigQuery
- Less stress/requests on Jira api
- No space required to store retrieved JSON files.
