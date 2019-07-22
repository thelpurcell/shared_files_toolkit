# ----------------------------------------------------
# List all shared folders of a Team
#
# Provided as-is by David Benoish
# updated 11 June 2018
#
# python 3 - multi-threaded, error management
# version 0.1 @dbenoish
# ----------------------------------------------------
import urllib.request, urllib.error, urllib.parse
from urllib.error import HTTPError
import json
import csv
import sys
from multiprocessing.dummy import Pool as ThreadPool
from datetime import datetime

#
# Global variables
#

# Application token - Team member file access rights required
dfbToken = "Bearer "

# output file (stdout by default)
csvwriter = csv.writer(sys.stdout)

# ---------------------------------------------------
# internal var
members_emails = []

# function invoked by the thread
def getInfo(member):
    if member['profile']['status']['.tag'] == 'active':
        listSharedFolders(member["profile"]["email"], member["profile"]["team_member_id"], csvwriter)

# Print all owned shared folders of a Team
def getSharedFoldersDetails(csvwriter):
    csvwriter.writerow(['User', 'Shared Owned Folder Path', 'Last updated (#days)', '#files', '#bytes', 'members'])
    members = getDfbMembers()
    for member in members:
        members_emails.append(member["profile"]["email"])

    pool = ThreadPool(len(members))
    pool.map(getInfo, members)
    pool.close()
    pool.join()

# Get all DfB members
def getDfbMembers():
    cursor = None
    members = []
    headers = {
        'Authorization': dfbToken ,
        'Content-type': 'application/json'
    }
    while True:
        if cursor is not None:
            body = {'cursor': cursor}
            request = urllib.request.Request('https://api.dropbox.com/2/team/members/list/continue', json.dumps(body).encode('utf-8'), headers)
        else:
            body = {}
            request = urllib.request.Request('https://api.dropbox.com/2/team/members/list', json.dumps(body).encode('utf-8'), headers)
        try:
            response = json.loads(urllib.request.urlopen(request).read().decode('utf_8'))
            members = members + response["members"]
            if response["has_more"]:
                cursor = response["cursor"]
            else:
                break
        except urllib.error.URLError as problem:
            print(problem.reason)
    return members

# get Folder's Owner email address
def getFolderOwner(folderId,memberId):
    owner = ''
    headers = {
        'Authorization':  dfbToken ,
        'Content-type': 'application/json',
        'Dropbox-API-Select-User': memberId
    }
    body = {
        "shared_folder_id": folderId,
        "actions": []
    }
    request = urllib.request.Request('https://api.dropboxapi.com/2/sharing/list_folder_members', json.dumps(body).encode('utf-8'), headers)
    try:
        response = json.loads(urllib.request.urlopen(request).read().decode('utf_8'))
        for user in response["users"]:
            if user["access_type"][".tag"] == "owner":
                owner = user["user"]["email"]
                break
    except urllib.error.URLError as problem:
        print(problem)
    return owner

# list all users and groups of a folder
def listAllUsersOfaFolder(memberId, folderId):
    ret = ''
    prems = True
    cursor = None
    headers = {
        'Authorization': dfbToken ,
        'Dropbox-API-Select-User': memberId,
        'Content-type': 'application/json'
    }
    while True:  
        if cursor is not None:
            body = {'cursor': cursor}
            request = urllib.request.Request('https://api.dropboxapi.com/2/sharing/list_folder_members/continue', json.dumps(body).encode('utf-8'), headers)
        else:
            body = {'shared_folder_id': folderId}
            request = urllib.request.Request('https://api.dropboxapi.com/2/sharing/list_folder_members', json.dumps(body).encode('utf-8'), headers)
        try:
            response = json.loads(urllib.request.urlopen(request).read().decode('utf_8'))
            # parse the results users / groups / invitees
            for item in response['users']:
                access_type = item['access_type']['.tag']
                email = item['user']['email']
                if email in members_emails:
                    status = '[i]'
                else:
                    status = '[e]'
                if prems == True:
                    ret = email + status + '(' +  access_type + ')'
                    prems = False
                else:
                    ret = ret + ';' + email + status + '(' +  access_type + ')'
            for item in response['groups']:
                access_type = item['access_type']['.tag']
                group_name = item['group']['group_name'] + '[g]'
                if prems == True:
                    ret = group_name + '(' +  access_type + ')'
                    prems = False
                else:
                    ret = ret + ';' + group_name + '(' +  access_type + ')'
            for item in response['invitees']:
                access_type = item['access_type']['.tag']
                email = '(invitee)' + item['invitee']['email']
                if email in members_emails:
                    status = '[i]'
                else:
                    status = '[e]'
                if prems == True:
                    ret = email + status + '(' +  access_type + ')'
                    prems = False
                else:
                    ret = ret + ';' + email + status + '(' +  access_type + ')'
            if response.get('cursor'):
                cursor = response['cursor']
            else:
                break
        except urllib.error.URLError as problem:
            print(problem.reason)
    return ret

# List all files of a Team's member 
def listSharedFolders(memberEmail, memberId, csvwriter):    
    cursor = None
    headers = {
        'Authorization': dfbToken ,
        'Dropbox-API-Select-User': memberId,
        'Content-type': 'application/json'
    }
    while True:  
        if cursor is not None:
            body = {'cursor': cursor}
            request = urllib.request.Request('https://api.dropboxapi.com/2/sharing/list_folders/continue', json.dumps(body).encode('utf-8'), headers)
        else:
            body = {}
            request = urllib.request.Request('https://api.dropboxapi.com/2/sharing/list_folders',  json.dumps(body).encode('utf-8'), headers)
        try:
            response = json.loads(urllib.request.urlopen(request).read().decode('utf_8'))
            for item in response["entries"]:
                shared_folder_id = item['shared_folder_id']
                path_lower = item.get('path_lower')
                # error or deleted fodler
                if path_lower == None:
                    continue  
                # the user is not the ower - discard
                if item['access_type']['.tag'] != 'owner' :
                    continue
  
                # we do not manage TFs
                if item['is_team_folder'] == True or item['is_inside_team_folder'] == True:
                    continue
                
                list = listAllUsersOfaFolder(memberId, shared_folder_id)
                age, nfiles, sfiles = getFolderInfo(memberId, path_lower)
                lastupdated = (datetime.now() - age).days
                csvwriter.writerow([memberEmail, path_lower, lastupdated, nfiles, sfiles, list ])
            
            if response.get('cursor'):
                cursor = response["cursor"]
            else:
                break
        except urllib.error.URLError as problem:
            print(problem.reason)

def getFolderInfo(memberId, folderName):    
    lastupdated = datetime(1900,1,1)
    nbfiles = 0
    sizefiles = 0
    therearefiles = False
    cursor = None
    headers = {
        'Authorization': dfbToken ,
        'Dropbox-API-Select-User': memberId,
        'Content-type': 'application/json'
    }
    while True:  
        if cursor is not None:
            body = {'cursor': cursor}
            request = urllib.request.Request('https://api.dropboxapi.com/2/files/list_folder/continue', json.dumps(body).encode('utf-8'), headers)
        else:
            body = {
                'path': folderName ,
                'recursive': True 
            }
            request = urllib.request.Request('https://api.dropboxapi.com/2/files/list_folder',  json.dumps(body).encode('utf-8'), headers)
        try:
            response = json.loads(urllib.request.urlopen(request).read().decode('utf_8'))
            for item in response["entries"]:
                if item[".tag"] == 'file':
                    current_date = datetime.strptime(item['client_modified'],'%Y-%m-%dT%H:%M:%SZ')
                    therearefiles = True
                    if current_date > lastupdated:
                        lastupdated = current_date
                    nbfiles = nbfiles + 1
                    sizefiles = sizefiles + int(item['size'])
            if response["has_more"]:
                cursor = response["cursor"]
            else:
                break
        except urllib.error.URLError as problem:
            print(problem.reason)
    if therearefiles:
        return lastupdated, nbfiles, sizefiles
    else:
        return datetime.now(), nbfiles, sizefiles


# --------------------      
# main procedure
# --------------------
print("start")
start = datetime.now()
getSharedFoldersDetails(csvwriter)
print('-- Done in ', str(datetime.now() - start))
