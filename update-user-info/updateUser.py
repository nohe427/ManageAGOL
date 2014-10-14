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
    return jres['urlKey']

def roleDict():
    #note, there is no error messaging so all roles must be valid
    roleUrl= 'http://www.arcgis.com/sharing/rest/portals/self/roles?f=json&token=' + token
    response = requests.get(roleUrl)
    jres = json.loads(response.text)
    return jres

def roleID(roleName):
    # matches role name with role id.

    roleID = 'blank'
    for item in roleDict['roles']:
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

    print roleID
    return roleID

def myEsri():
    usertype= 'arcgisonly'
    if line[4].lower() == 'my esri':
        usertype='both'
    return usertype

def updateUser(line):

       #updates description, Enables My Esri Access and makes account searchable to public
       userURL ='https://{}.maps.arcgis.com/sharing/rest/community/users/{}/update'.format(urlKey, line[0])
       data = {'f':'json','usertype':usertype,'fullName': line[1],'description': line[2], 'access':'public','token':token}
       response = requests.post(userURL, data=data, verify=False).json()
       print response
def updateUserRole():
    #updates user role to Administrator
       updateURL = 'http://{}.maps.arcgis.com/sharing/rest/portals/self/updateUserRole'.format(urlKey)
       data ={'f':'json', 'token':token ,'user':line[0],'role':rID}
       response = requests.post(updateURL, data=data, verify=False).json()
       print response

if __name__ == "__main__":
    #Enter admin Username and password
    user = raw_input("Admin username:")
    pw  = raw_input("Password:")

    #Generates Token
    token = getToken(user, pw)
    #Acquires Account information of the Admin user and assigns Variables
    urlKey= accountInfo(token)


    #Input CSV file
    CSV = r"input file"

    #get role
    roleDict = roleDict()

    #Open CSV file and Read first header line
    openedfile = open(CSV, 'r')


    #Lops through CSV file to invite users and update account information
    for x in openedfile.readlines():
        print x
        line = x.split(",")
        action= line[11]
        if line[11].lower()=='update\n':
            rID =roleID(line[5])
            usertype= myEsri()
            updateUser(line)
            updateUserRole()

        else:
            print 'no'







