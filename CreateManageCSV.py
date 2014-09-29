#-------------------------------------------------------------------------------
# Name:            Create Management CSV
# Purpose:         Parse through users in organization, extract important information
#                  and enable create management spreadsheet.
#
# Author:     Kelly Gerrow
#
# Created:     23/06/2014
# Copyright:   (c) kell6873 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os, os.path
import sys
import urllib2, urllib, requests
import json

#variables
user = 'Karate_Kelly'#raw_input("Admin username:")
pw  = 'Browncow1'#raw_input("Password:")

#create a file and add header
#fileLoc = 'c:\python\manageCSV6print userlist.csv'#'raw_input("Put in the file path to store the data here \nExample: C:\Documents\FILE.csv \n")
#f=open(fileLoc, "w")
#header="Username,Description,Email,Full Name,Role,Action\n"
#f.write(header)

# Function to return a token for this session
def getToken(user, pw):
    data = {'username': user,
        'password': pw,
        'referer' : 'https://www.arcgis.com',
        'f': 'json'}
    url  = 'https://arcgis.com/sharing/rest/generateToken'
    jres = requests.post(url, data=data, verify=False).json()
    return jres['token']

def GetURL(token):
    URL= 'http://www.arcgis.com/sharing/rest/portals/self?f=json&token=' + token
    response = requests.get(URL)
    URLKey = json.loads(response.text)['urlKey']
    return URLKey

def CreateUserlist(token, URLKey):
    #get amount of users
    maxURL ='http://{}.maps.arcgis.com/sharing/rest/portals/self/users'.format(URLKey)
    request = maxURL +"?f=json&token="+token
    response = requests.get(request)
    jres = json.loads(response.text)
    maxUsers = 20 #jres['total']
    start = 1
    number = 50
    #retreive information of all users in organization
    while start < maxUsers:
        listURL ='http://{}.maps.arcgis.com/sharing/rest/portals/self/users'.format(URLKey)
        request = listURL +"?start="+str(start)+"&num="+str(number)+"&f=json&token="+token
        response = requests.get(request).json()
        #jres = json.loads(response.text)
        for row in response['users']:
            userlist[row['username']]={'description':row['description'], 'email':row['email'], 'FullName': row['fullName'], 'role':row['role']}
            #userlist['testnum':1, row['username']]=[{'username':row['username'],'description':row['description'], 'email':row['email'], 'FullName': row['fullName'], 'role':row['role']}]

            #print str(row['username']) + str(row['description']) + str(row['email']) + str(row['fullName'])
            #f.write("{0},{1},{2},{3},{4}\n".format(str(row['username']),
##                                           str(row['description']),
##                                           str(row['email']),
##                                           str(row['fullName']),
##                                           str(row['role'])))
        start+=number
    return userlist

def Analyze(token,userlist):
    #Identifies users with no description
    for x in userlist:
        print x
        #print userlist[x]['description']
        if userlist[x]['description']:
          userlist[x]['updDesc']='no'
        else:
         userlist[x]['updDesc']='yes'
    return userlist


#get token and URL Key
token = getToken(user, pw)
URLKey = GetURL(token)

#get list of users to be removed
userlist = CreateUserlist(token,URLKey)
analyzeUser = Analyze(token, userlist)
#f.close()
