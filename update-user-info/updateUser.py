#-------------------------------------------------------------------------------
# Name:        Create Users Template
# Purpose:      Creates users and updates them to have specific roles upon initial
#               Login. Reads usernames from a list and updates users to have
#               My Esri Access Enabled, public searchable account, administrator account
#               users are entitled a pro license
#
# Author:      kell6873
#
# Created:     28/09/2014
# Copyright:   (c) kell6873 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os, os.path
import sys
import requests
import json

# Function to return a token for this session
def getToken(user, pw):
    #generates token
    data = {'username': user,
        'password': pw,
        'referer' : 'https://www.arcgis.com',
        'f': 'json'}
    url  = 'https://arcgis.com/sharing/rest/generateToken'
    jres = requests.post(url, data=data, verify=False).json()
    return jres['token']

def accountInfo(token):
    #requests account information
    URL= 'http://www.arcgis.com/sharing/rest/portals/self?f=json&token=' + token
    response = requests.get(URL)
    jres = json.loads(response.text)
    return jres['urlKey'], jres['name'], jres['user']['fullName'], jres['user']['email']

def roleID(roleName, token):
    # matches role name with role id.
    #note, there is no error messaging so all roles must be valid
    roleUrl= 'http://www.arcgis.com/sharing/rest/portals/self/roles?f=json&token=' + token
    response = requests.get(roleUrl)
    jres = json.loads(response.text)
    roleID = 'blank'
    for item in jres['roles']:
        #print roleName
        if roleName.lower() == item['name'].lower():
            #print roleName.lower() +item['name'].lower()
            roleID = item['id']
        elif roleName.lower() == 'administrator':
            roleID= 'account_admin'
        elif roleName.lower() == 'publisher':
            roleID= 'account_publisher'
        elif roleName.lower() == 'user':
            roleID= 'account_user'

    return roleID

def readLine(openedfile):
    #Reads file and splits contents by comma
    line = openedfile.readline()
    splitstring = line.split(",")
    return splitstring

def updateUser(line):
    #  Provisions new users Pro Entitlements
       proUrl= 'http://{}.maps.arcgis.com/sharing/rest/content/listings/2d2a9c99bb2a43548c31cd8e32217af6/provisionUserEntitlements'.format(urlKey)
       data = {'f':'json', 'token':token ,'userEntitlements':'{"users":["'+line[0]+'"],"entitlements":["desktopAdvN","spatialAnalystN","3DAnalystN","networkAnalystN","geostatAnalystN","dataReviewerN","workflowMgrN","dataInteropN"]}'}
       response = requests.post(proUrl, data=data, verify=False).json()

      #updates user role to Administrator
       updateURL = 'http://{}.maps.arcgis.com/sharing/rest/portals/self/updateUserRole'.format(urlKey)
       data ={'f':'json', 'token':token ,'user':line[0],'role':'account_admin'}
       response = requests.post(updateURL, data=data, verify=False).json()

        #updates description, Enables My Esri Access and makes account searchable to public
       userURL ='https://{}.maps.arcgis.com/sharing/rest/community/users/{}/update'.format(urlKey, line[0])
       data = {'f':'json','usertype':'both','description': line[1], 'access':'public','token':token}
       #data = {'f':'json','description': line[1], 'access':'public','token':token}
       response = requests.post(userURL, data=data, verify=False).json()
       #print response


if __name__ == "__main__":
    #Enter admin Username and password
    user = raw_input("Admin username:")
    pw  = raw_input("Password:")

    #Generates Token
    token = getToken(user, pw)
    #Acquires Account information of the Admin user and assigns Variables
    aInfo = accountInfo(token)
    urlKey = aInfo[0]
    orgName= aInfo[1]
    orgFullName = aInfo[2]
    adminEmail = aInfo[3]

    #Input CSV file
    CSV = r"\\kellyg\python\manage_AgolUser.csv"

    #Open CSV file and Read first header line
    openedfile = open(CSV, 'r')
    openedfile.readline()

    #Lops through CSV file to invite users and update account information
    while True:
        line = readLine(openedfile)
        print len(line)
        #invitelist = inviteUsers(line)
        if len(line) == 1:
            break
        else:
            inviteUsers(line)
            updateUser(line)



