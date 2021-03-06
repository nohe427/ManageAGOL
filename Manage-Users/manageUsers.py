#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      kell6873
#
# Created:     28/09/2014
# Copyright:   (c) kell6873 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    pass

if __name__ == '__main__':
    main()




import os, os.path
import sys
import urllib2, urllib, requests
import json

#variables
user = 'Karate_Kelly'#raw_input("Admin username:")
pw  = 'Browncow1'#raw_input("Password:")

#open file
fileLoc = '\\\\kellyg\python\manage_AgolUser.csv' #'raw_input("Put in the file path to store the data here \nExample: C:\Documents\FILE.csv \n")
f=open(fileLoc, "r")

# Functions to handle post requests script
def sendRequest(url, data):
    result = urllib2.urlopen(url, data).read()
    jres = json.loads(result)
    return jres

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

def inviteUsers(f,urlKey, token,name, fullName, email):
    #invite users from spreadsheet
    invitelist =[]
    for line in f.readlines()[2:]:
        splitstring = line.split(",")
        print splitstring

    #Invite Users
        if splitstring[6].lower() == 'invite\n':
            print splitstring[0]
            invitelist.append(splitstring[0])
            rID = roleID(splitstring[5], token)
            url = 'http://{}.maps.arcgis.com/sharing/rest/portals/self/invite'.format(urlKey)
            subject = 'An invitation to join an ArcGIS Online Organization, ' + name + '. DO NOT REPLY'
            text = '<html><body><p>' + fullName+ ' has invited you to join an ArcGIS Online Organization, ' +name + '. Please click this link to join:<br><a href="https://www.arcgis.com/home/signin.html?invitation=@@invitation.id@@">https://www.arcgis.com/home/signin.html?invitation=@@invitation.id@@</a></p><p>If you have difficulty signing in, please email your administrator at '+ email+ '. Be sure to include a description of the problem, your username, the error message, and a screenshot.</p><p>For your reference, you can access the home page of the organization here: <br>http://'+urlKey +'.maps.arcgis.com/home/</p><p>This link will expire in two weeks.</p><p style="color:gray;">This is an automated email, please do not reply.</p></body></html>'
            #send without sending an email notification to user
            invitationlist = '{"invitations":[{"username":"'+splitstring[0]+'", "password":"Password123", "firstname":"' + splitstring[3]+'","lastname":"'+ splitstring[4]+'","fullname":"'+splitstring[3] + ' ' + splitstring[4]+'","email":"'+splitstring[2]+'","role":"' +rID +'"}]}'
            print invitationlist
            data={'subject':subject, 'html':text, 'invitationlist':invitationlist,'f':'json', 'token':token}
            jres = requests.post(url, data=data, verify=False).json()

            #Send invitations to preestablished user names.
            #invitationlist = '{"invitations":[{"username":"'+splitstring[0]+'", "firstname":"' + splitstring[3]+'","lastname":"'+ splitstring[4]+'","fullname":"'+splitstring[3] + ' ' + splitstring[4]+'","email":"'+splitstring[2]+'","role":"' +rID +'"}]}'
            #Send invitations for existing users.
            #invitationlist = '{"invitations":[{"email":"'+splitstring[2]+'","role":"' +rID +'"}]}'

    #format Users to have contact name, myesri access, public
            userURL ='https://{}.maps.arcgis.com/sharing/rest/community/users/{}/update'.format(urlKey, splitstring[0])
            #data = {'f':'json','usertype':'both','description': splitstring[1], 'access':'public','token':token}
            data = {'f':'json','description': splitstring[1], 'access':'public','token':token}
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




#makes all users administrators




#get token and URL Key
token = getToken(user, pw)
aInfo = accountInfo(token)
urlKey = aInfo[0]
name= aInfo[1]
fullName = aInfo[2]
email = aInfo[3]
invitelist = inviteUsers(f,urlKey, token,name, fullName, email)
updateUser()

#print urlKey + name + fullName
##invitelist =[]
##for line in f.readlines()[2:]:
##    print line
##    splitstring = line.split(",")
##    print splitstring
##
##    if splitstring[6].lower() == 'invite\n':
##        print splitstring[0]
##        invitelist.append(splitstring[0])
##        rID = roleID(splitstring[5], token)
##        url = 'http://{}.maps.arcgis.com/sharing/rest/portals/self/invite'.format(urlKey)
##        subject = 'An invitation to join an ArcGIS Online Organization, ' + name + '. DO NOT REPLY'
##        text = '<html><body><p>' + fullName+ ' has invited you to join an ArcGIS Online Organization, ' +name + '. Please click this link to join:<br><a href="https://www.arcgis.com/home/signin.html?invitation=@@invitation.id@@">https://www.arcgis.com/home/signin.html?invitation=@@invitation.id@@</a></p><p>If you have difficulty signing in, please email your administrator at '+ email+ '. Be sure to include a description of the problem, your username, the error message, and a screenshot.</p><p>For your reference, you can access the home page of the organization here: <br>http://'+urlKey +'.maps.arcgis.com/home/</p><p>This link will expire in two weeks.</p><p style="color:gray;">This is an automated email, please do not reply.</p></body></html>'
##        #send without sending an email notification to user
##        #invitationlist = '{"invitations":[{"username":"'+splitstring[0]+'", "password":"Password123", "firstname":"' + splitstring[3]+'","lastname":"'+ splitstring[4]+'","fullname":"'+splitstring[3] + ' ' + splitstring[4]+'","email":"'+splitstring[2]+'","role":"' +rID +'"}]}'
##        #Send invitations to preestablished user names.
##        #invitationlist = '{"invitations":[{"username":"'+splitstring[0]+'", "firstname":"' + splitstring[3]+'","lastname":"'+ splitstring[4]+'","fullname":"'+splitstring[3] + ' ' + splitstring[4]+'","email":"'+splitstring[2]+'","role":"' +rID +'"}]}'
##        #Send invitations for existing users.
##        #invitationlist = '{"invitations":[{"email":"'+splitstring[2]+'","role":"' +rID +'"}]}'
##        #data={'subject':subject, 'html':text, 'invitationlist':invitationlist,'f':'json', 'token':token}
##        #jres = requests.post(url, data=data, verify=False).json()
