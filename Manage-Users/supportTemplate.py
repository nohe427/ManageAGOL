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

def inviteUsers(line):
    #invite users from spreadsheet
    rID = roleID(line[5], token)
    url = 'http://{}.maps.arcgis.com/sharing/rest/portals/self/invite'.format(urlKey)
    #subject and text for email
    subject = 'An invitation to join an ArcGIS Online Organization, ' + orgName + '. DO NOT REPLY'
    text = '<html><body><p>' + orgFullName+ ' has invited you to join an ArcGIS Online Organization, ' +orgName + '. Please click this link to join:<br><a href="https://www.arcgis.com/home/signin.html?invitation=@@invitation.id@@">https://www.arcgis.com/home/signin.html?invitation=@@invitation.id@@</a></p><p>If you have difficulty signing in, please email your administrator at '+ adminEmail+ '. Be sure to include a description of the problem, your username, the error message, and a screenshot.</p><p>For your reference, you can access the home page of the organization here: <br>http://'+urlKey +'.maps.arcgis.com/home/</p><p>This link will expire in two weeks.</p><p style="color:gray;">This is an automated email, please do not reply.</p></body></html>'

    #send invitation without sending an email notification to user
    invitationlist = '{"invitations":[{"username":"'+line[0]+'", "password":"Password123", "fullname":"'+line[1] + '","email":"'+line[3]+'","role":"' +rID +'"}]}'
    data={'subject':subject, 'html':text, 'invitationlist':invitationlist,'f':'json', 'token':token}
    jres = requests.post(url, data=data, verify=False).json()

        #Send invitations to preestablished user names.
        #invitationlist = '{"invitations":[{"username":"'+line[0]+'", "firstname":"' + line[3]+'","lastname":"'+ line[4]+'","fullname":"'+line[3] + ' ' + line[4]+'","email":"'+line[2]+'","role":"' +rID +'"}]}'
        #Send invitations for existing users.
        #invitationlist = '{"invitations":[{"email":"'+line[2]+'","role":"' +rID +'"}]}'


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
       data = {'f':'json','usertype':'both','description': line[2], 'access':'public','token':token}
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
    CSV = r"\\kellyg\python\user.csv"

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



