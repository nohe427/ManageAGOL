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
fileLoc = 'c:\python\manage_AgolUser.csv' #'raw_input("Put in the file path to store the data here \nExample: C:\Documents\FILE.csv \n")
f=open(fileLoc, "r")

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
#get token and URL Key
token = getToken(user, pw)
aInfo = accountInfo(token)
urlKey = aInfo[0]
name= aInfo[1]
fullName = aInfo[2]
email = aInfo[3]
roleID = 'jdsfhskhte'

print urlKey + name + fullName

#get list of users to be removed
for line in f.readlines()[1:]:
    splitstring = line.split(",")
    if splitstring[7] == 'Invite':
        url = 'http://ess.maps.arcgis.com/sharing/rest/portals/self/invite'
        subject = 'An invitation to join an ArcGIS Online Organization, ' + name + ' Esri Support Services. DO NOT REPLY'
        text = '<html><body><p>' + fullName+ ' has invited you to join an ArcGIS Online Organization, ' +name + '. Please click this link to join:<br><a href="https://www.arcgis.com/home/signin.html?invitation=@@invitation.id@@">https://www.arcgis.com/home/signin.html?invitation=@@invitation.id@@</a></p><p>If you have difficulty signing in, please email your administrator at '+ email+ '. Be sure to include a description of the problem, your username, the error message, and a screenshot.</p><p>For your reference, you can access the home page of the organization here: <br>http://'+urlKey +'.maps.arcgis.com/home/</p><p>This link will expire in two weeks.</p><p style="color:gray;">This is an automated email, please do not reply.</p></body></html>'
        invitationlist = {"invitations":[{"username":"'+splitstring[0]+'", "password":"'+splitstring[1]+'", "firstname":"' + splitstring[4]+'","lastname":"'+ splitstring[5]+'","fullname":"'splitstring[4] + " " + splitstring[5]+'","email":"'+splitstring[2]+'","role":"' +roleID +'"}]}
        print invitationlist
         # data={'subject':subject, 'html':text, 'invitationlist':invitationlist,'f':'json', 'token':token}
          #jres = requests.post(url, data=data, verify=False).json()