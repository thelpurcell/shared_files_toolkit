# csm-toolkit
Repository for handy scripts and tools for Admins

# Disclaimer
Please note that this code is supplied for example and experimentation is not officially supported. When this was tested locally, it ran quite fast across one of our demo environments but the time it takes to complete obviously depends on the size of your Dropbox instance.

# Acknowledgement of original code authors
This is a call out to those who originally developed the scripts within this repository. As these have been written by Dropboxers past and present who have shared this code publically through various repositories, this repository is an attempt to consolidate them all and form a central repository for ongoing development and to make it easier to share and surface handy code for the benefit of Dropbox customers.

# Prerequisites
In order to run all of the code in this repository, you will need to generate the required Access tokens and paste the token relevant tokens into the individual scripts for them to be able to be authorised to execute the required API commands against your Dropbox instance. You will need to be a Team Admin on your Dropbox team in order to generate the keys.

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
  - Python 3 installed
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
| Column Name              | Description                                                                                                                                                                                                                       |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Owner email              | Email address of the share, note if this is blank someone is sharing this folder with you, so you can filter out the blanks for simplicity                                                                                        |
| Owner Name               | As above, if this is blank, you are not the owner, so filter out the blannks                                                                                                                                                      |
| Folder Name              | Name of folder shared                                                                                                                                                                                                             |
| Folder Path              | Path of shared folder                                                                                                                                                                                                             |
| Folder ID                | Folder ID                                                                                                                                                                                                                         |
| Collaborator Email       | Who has access to this share                                                                                                                                                                                                      |
| Collaborator Permissions | What type of access does the collaborator have with this share, note you can filter this field to show only shares where you are the owner. Editors or Read Only users have access to the share and those respective permissions. |
| Collaborator on Team     | Tells you if the person is inside or outside your Dropbox Team, False means the collaborator is external to the Atlassian Team                                                                                                    |
| Folder Mount Status      | Mounted or Unmounted                                                                                                                                                                                                              |
| Group Name               | TBC                                                                                                                                                                                                                               |
| Group Members            | TBC                                                                                                                                                                                                                               |
| Group Permissions        | TBC                                                                                                                                                                                                                               |
| Group Type               | TBC                                                                                                                                                                                                                               |
| Team Owned Folder        | TBC                                                                                                                                                                                                                               |


