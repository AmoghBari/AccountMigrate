# AccountMigrate


Instructions for migrate.yml file

1. Create a repo secret with the name of DESTINATION_TOKEN in Secrets and add the GitHub Token of the destination account having      the permissions of repo and admin:org.
2. Create another repo secret named SOURCE_SECRET and add the names of all the secrets that are in the repo except the new secrets    which we are creating.



<br> <br>
Python Script
1. Regarding the Python Script The GitHub API does not allow the migration of Secrets and if we try to convert them into json         format and then migrate then there is an error showing that the format of the secrets is not correct.
2. Also if we try to convert the Secrets into Envirnoment Variables and then migrate it then there is an error showing that the       secrets were not found as they cannot read them.
3. So, in conclusion GitHub does not allow the migration of secrets as we even the owner cannot access them after we have created     them and can only delete them or update them. So, any script using GitHub API does not allow the migration of the secrets as       they cannot read them.
4. You have to manually create the secrets in the new repo.
