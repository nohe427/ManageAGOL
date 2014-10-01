#-------------------------------------------------------------------------------
# Name:        ManageUsers
# Purpose:
#
# Author:      kell6873
#
# Created:     28/09/2014
# Copyright:   (c) kell6873 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os, os.path
import sys
import urllib2, urllib, requests
import json

# Function to return a token for this session
def getToken(user, pw):
    data = {'username': user,
        'password': pw,
        'referer' : 'https://www.arcgis.com',
        'f': 'json'}
    url  = 'https://arcgis.com/sharing/rest/generateToken'
    jres = requests.post(url, data=data, verify=False).json()
    return jres['token']

def accountInfo(token):
    URL= 'http://www.arcgis.com/sharing/rest/portals/self?f=json&token=' + token
    response = requests.get(URL)
    jres = json.loads(response.text)
    return jres['urlKey'], jres['name'], jres['user']['fullName'], jres['user']['email']

def roleID(roleName, token):
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
        #else:
            #print 'there is no matching role for ' + roleName
    return roleID

def readLine(openedfile):
    line = openedfile.readline()
    #line = line.rstrip('\n')
    print line
    splitstring = line.split(",")
    return splitstring

<<<<<<< HEAD

if __name__ == "__main__":

    CSV = r"\\kellyg\python\manage_AgolUser.csv"
    openedfile = open(CSV, 'r')
    openedfile.readline()
    openedfile.readline()
    t=True

    while t == True:
        line = readLine(openedfile)
        print len(line)
        if len(line)<0:
            t =False
        else:
            invitelist = inviteUsers(line)
    #return line

=======
>>>>>>> origin/master
def inviteUsers(line):
    #invite users from spreadsheet
    invitelist =[]
    print line

    #Invite Users
    if line[6].lower() == 'invite':
        print line[0]
        invitelist.append(line[0])
        rID = roleID(line[5], token)
        url = 'http://{}.maps.arcgis.com/sharing/rest/portals/self/invite'.format(urlKey)
        subject = 'An invitation to join an ArcGIS Online Organization, ' + orgName + '. DO NOT REPLY'
        text = '<html><body><p>' + orgFullName+ ' has invited you to join an ArcGIS Online Organization, ' +orgName + '. Please click this link to join:<br><a href="https://www.arcgis.com/home/signin.html?invitation=@@invitation.id@@">https://www.arcgis.com/home/signin.html?invitation=@@invitation.id@@</a></p><p>If you have difficulty signing in, please email your administrator at '+ adminEmail+ '. Be sure to include a description of the problem, your username, the error message, and a screenshot.</p><p>For your reference, you can access the home page of the organization here: <br>http://'+urlKey +'.maps.arcgis.com/home/</p><p>This link will expire in two weeks.</p><p style="color:gray;">This is an automated email, please do not reply.</p></body></html>'
        #send without sending an email notification to user
        invitationlist = '{"invitations":[{"username":"'+line[0]+'", "password":"Password123", "firstname":"' + line[3]+'","lastname":"'+ line[4]+'","fullname":"'+line[3] + ' ' + line[4]+'","email":"'+line[2]+'","role":"' +rID +'"}]}'
        print invitationlist
        data={'subject':subject, 'html':text, 'invitationlist':invitationlist,'f':'json', 'token':token}
        #jres = requests.post(url, data=data, verify=False).json()

        #Send invitations to preestablished user names.
        #invitationlist = '{"invitations":[{"username":"'+line[0]+'", "firstname":"' + line[3]+'","lastname":"'+ line[4]+'","fullname":"'+line[3] + ' ' + line[4]+'","email":"'+line[2]+'","role":"' +rID +'"}]}'
        #Send invitations for existing users.
        #invitationlist = '{"invitations":[{"email":"'+line[2]+'","role":"' +rID +'"}]}'

#format Users to have contact name, myesri access, public
        userURL ='https://{}.maps.arcgis.com/sharing/rest/community/users/{}/update'.format(urlKey, line[0])
        #data = {'f':'json','usertype':'both','description': line[1], 'access':'public','token':token}
        data = {'f':'json','description': line[1], 'access':'public','token':token}
        response = requests.post(userURL, data=data, verify=False).json()
        print response

        #update csv so staus isn't invite

    return invitelist


def updateUser():
    #  give new users Pro Entitlements
       proUrl= 'http://{}.maps.arcgis.com/sharing/rest/content/listings/2d2a9c99bb2a43548c31cd8e32217af6/provisionUserEntitlements'.format(urlKey)
       data = {'f':'json', 'token':token ,'userEntitlements':'{"users":'+str(invitelist)+',"entitlements":["desktopAdvN","spatialAnalystN","3DAnalystN","networkAnalystN","geostatAnalystN","dataReviewerN","workflowMgrN","dataInteropN"]}'}
       response = requests.post(proUrl, data=data, verify=False).json()
       print response

       for user in invitelist:
         updateURL = 'http://{}.maps.arcgis.com/sharing/rest/portals/self/updateUserRole'.format(urlKey)
         data ={'f':'json', 'token':token ,'user':user,'role':'account_admin'}
         response = requests.post(updateURL, data=data, verify=False).json()
         print response


if __name__ == "__main__":
    #variables
    user = 'Karate_Kelly'#raw_input("Admin username:")
    pw  = 'Browncow1'#raw_input("Password:")

    token = getToken(user, pw)
    aInfo = accountInfo(token)
    urlKey = aInfo[0]
    orgName= aInfo[1]
    orgFullName = aInfo[2]
    adminEmail = aInfo[3]

    CSV = r"\\kellyg\python\manage_AgolUser.csv"
    openedfile = open(CSV, 'r')
    openedfile.readline()
    openedfile.readline()


    while True:
        line = readLine(openedfile)
        print len(line)
        #invitelist = inviteUsers(line)
        if len(line) == 1:
            break
        else:
            invitelist = inviteUsers(line)



###variables
##user = 'Karate_Kelly'#raw_input("Admin username:")
##pw  = 'Browncow1'#raw_input("Password:")

#open file
##fileLoc = '\\\\kellyg\python\manage_AgolUser.csv' #'raw_input("Put in the file path to store the data here \nExample: C:\Documents\FILE.csv \n")
##f=open(fileLoc, "r")

##
##
###get token and URL Key
##token = getToken(user, pw)
##aInfo = accountInfo(token)
##urlKey = aInfo[0]
##orgName= aInfo[1]
##orgFullName = aInfo[2]
##adminEmail = aInfo[3]

##CSV = r"\\kellyg\python\manage_AgolUser.csv"
##openedfile = open(CSV, 'r')
##openedfile.readline()
##openedfile.readline()
##
##while True:
##
##  line = readLine(openedfile)
##  print len(line)
##  if not line:
##    break
##  else:
##    invitelist = inviteUsers(line)
##return line


<<<<<<< HEAD
#get token and URL Key
token = getToken(user, pw)
aInfo = accountInfo(token)
urlKey = aInfo[0]
orgName= aInfo[1]
orgFullName = aInfo[2]
adminEmail = aInfo[3]

##CSV = r"\\kellyg\python\manage_AgolUser.csv"
##openedfile = open(CSV, 'r')
##openedfile.readline()
##openedfile.readline()
##
##while True:
##
##  line = readLine(openedfile)
##  print len(line)
##  if not line:
##    break
##  else:
##    invitelist = inviteUsers(line)
##return line


=======
>>>>>>> origin/master
updateUser()

