# Shared Files Toolkit
Repository for handy scripts and tools for Admins

# Disclaimer
Please note that this code is supplied for example and experimentation is not officially supported. When this was tested locally, it ran quite fast across one of our demo environments but the time it takes to complete obviously depends on the size of your Dropbox instance.

# Important!
Keep in mind these scripts will consume your API call quota. Please ensure not to impact any other services or integrations that rely on API calls from your Dropbox instance. Please be aware of your API call quota limits and make sure using these script will not cause disruption to production integrations or services dependant on api interaction with Dropbox.

# Acknowledgement of original code authors
This is a call out to those who originally developed the scripts within this repository. As these have been written by Dropboxers past and present who have shared this code publically through various repositories, this repository is an attempt to consolidate them all and form a central repository for ongoing development and to make it easier to share and surface handy code for the benefit of Dropbox customers.

# Prerequisites
In order to run all of the code in this repository, you will need to generate the required Access tokens and paste the relevant tokens into the individual scripts for them to be able to be authorised to execute the required API commands against your Dropbox instance. You will need to be a Team Admin on your Dropbox team in order to generate the tokens.

## Generate a Team Member File Access token

To generate your Team Member File Access Token:

1. Go to https://dropbox.com/developers in your web browser.
2. Click Sign in in the top right corner and enter your Dropbox administrator credentials.
3. Click My apps in the left sidebar, then click Create app.
4. Select Dropbox Business API then select Team member file access.
5. Create a unique name for the app (e.g. <CompanyName> File Access).
6. Choose the Dropbox account that will own your app.
7. Agree to the Dropbox API Terms and Conditions and click Create App.
8. Under the Settings tab, in the OAuth 2 section, generate an access token by clicking Generate.
9. Copy the generated Team Member File Access Token to the scripts where required.

## Generate a Team Member Management token

To generate your Team Member Management Token:

1. Go to https://dropbox.com/developers in your web browser.
2. Click Sign in in the top right corner and enter your Dropbox administrator credentials.
3. Click My apps in the left sidebar, then click Create app.
4. Select Dropbox Business API then select Team member management.
5. Create a unique name for the app (e.g. <CompanyName> Team Management).
6. Choose the Dropbox account that will own your app.
7. Agree to the Dropbox API Terms and Conditions and click Create App.
8. Under the Settings tab, in the OAuth 2 section, generate an access token by clicking Generate.
9. Copy the generated Team Member Management Token to the scripts where required.

## Generate a Team Information Access token

To generate your Team Information Access Token:

1. Go to https://dropbox.com/developers in your web browser.
2. Click Sign in in the top right corner and enter your Dropbox administrator credentials.
3. Click My apps in the left sidebar, then click Create app.
4. Select Dropbox Business API then select Team information.
5. Create a unique name for the app (e.g. <CompanyName> Team Info).
6. Choose the Dropbox account that will own your app.
7. Agree to the Dropbox API Terms and Conditions and click Create App.
8. Under the Settings tab, in the OAuth 2 section, generate an access token by clicking Generate.
9. Copy the generated Team Information Token to the scripts where required.


# Scripts and instructions
## getCollaborationReport-py3
As a Team Admin, this script will show you, the user who runs the script, what shared folders you currently have and who these are shared with.

### Requirements
  - Python 3
  - Team Member File Access token
  - Team Member Management Access token
  - Team Information Access token
  - getCollaborationReport-py3
  - Classes.py
  - users.csv

### How to run getCollaborationReport-py3

1. Place the ‘getCollaborationReport-py3’,  ‘Classes.py’ and ‘users.csv’ files into necessary location on your machine.
2. Edit line 41-43 of the script and set your Access tokens  to the appropriate variables, it should look like the following:
    `aTokenTMFA = 'xxxxx' # Team Member File Access`
    `aTokenTMM =  'yyyyy' # Team Member Management` 
    `aTokenTI =   'zzzzz' # Team Information Access`
    Where x, y and z are your tokens etc.
3. Open the ‘users.csv’ file in a text editor and enter your email address into it, it includes an example for you to simply replace with your email address.
4. Run the script, noting that it is a python 3 script, and an output csv file will be generated in the local folder.
5. Open the .csv file produced in Excel

The output should contain;
- Owner email - Email address of the share, note if this is blank someone is sharing this folder with you, so you can filter out the blanks for simplicity
- Owner Name - As above, if this is blank, you are not the owner, so filter out the blanks
- Folder Name - Name of folder shared
- Folder Path - Path of shared folder
- Folder ID - Folder ID
- Collaborator Email - Who has access to this share
- Collaborator Permissions - What type of access does the collaborator have with this share, note you can filter this field to show only shares where you are the owner. Editors or Read Only users have access to the share and those respective permissions.
- Collaborator on Team - Tells you if the person is inside or outside your Dropbox Team, False means the collaborator is external to the Atlassian Team
- Folder Mount Status - Mounted or Unmounted
- Group Name - TBC
- Group Members - TBC
- Group Permissions - TBC
- Group Type - TBC
- Team Owned Folder - TBC

## ListSharedLinks.py
This script will show you what shared links are currently live across the whole of your Dropbox team.

### Requirements
- Team Member File Access token
- Python 3

### How to run ListSharedLinks.py

1. Place the ‘ListSharedLinks.py’ file in necessary location on your machine
2. Edit line 22 of the script and set your Team Member File Access token as the “dfbToken” variable. It should look like this:  `dfbToken = '123456'` where 123456 is your Team Member File Access token.
3. Run the script. Note that by default it will output to stdout, you can redirect the stdout to a .csv file and open in Excel, or tweak the code to produce a .csv if desired.

The output should contain the following columns:
- User - User who created/owns the link
- Path - Path to the content shared
- Visibility - Indicates if the shared link is team_only, public or shared folder only
- URL - The actual shared link URL

## List_all_shared_folders_of_a_team.py
This script will show you all Shared Folders (and Shared Files) that are shared externally across the entire Dropbox Team.

### Requirements
- Team Member File Access token
- Python 3
- List_all_shared_folders_of_a_team.py

### How to run List_all_shared_folders_of_a_team.py

1. Place the ‘List_all_shared_folders_of_a_team.py’ script in the necessary location on your machine
2. Edit line 23 of the script and set you Team Member File Access token agains the dfbToken variable, remember to include “Bearer “ before your token. 
    It should look like this  `dfbToken = "Bearer 123456"` where 123456 is your Team Member File Access token.
3. Run the script. Note that by default it will output to stdout, you can redirect the stdout to a .csv file and open in Excel, or tweak the code to produce a .csv if desired.
4. When you open the file, filter on ‘[e]’ (without the single quotes) in the Members column to show those links that are going to an external person ([i] = internal and [e] = external in this column of the output csv file).

The output should contain the following columns:
- User - The user who shared the content 
- Shared Owned Folder Path - The path to the shared folder
- Last updated (#days) - How long since this share was updated
- No. of files - Number of files shared
- No. of bytes - What is the total size of shared content
- Members - Who are collaborating via this share
