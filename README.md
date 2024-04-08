# AccountMigrate


Instructions for main.yaml file

1. Create a repo secret with the name of DESTINATION_TOKEN in Secrets and add the GitHub Token of the destination account having the permissions of repo and admin:org.
2. Create another repo secret named SOURCE_SECRET and add the names of all the secrets that are in the repo except the new secrets which we are creating.
