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
    number = 5
    #retreive information of all users in organization
    while start < maxUsers:
        listURL ='http://{}.maps.arcgis.com/sharing/rest/portals/self/users'.format(URLKey)
        request = listURL +"?start="+str(start)+"&num="+str(number)+"&f=json&token="+token
        response = requests.get(request)
        jres = json.loads(response.text)
        userDict = []
        allvals = ['username','fullName', 'description', 'email', 'userType', 'access', 'role']
        for row in jres['users']:
           userLst = []
           for val in allvals:
                userLst.append(row[val])
           userDict.append(userLst)
        start +=number
    return userDict

def writeCSV(f):
    #updates list to record which emails have been sent to the users
    for user in userlist:
        for i,j in enumerate(user):
            print i
            if user[i]:
                user[i] = user[i]
            else:
                user[i] = 'none'
        f.write(user[0]+ "," + user[1]+ "," +user[2]+"," +user[3]+"," +user[4]+"," +user[5]+","+user[6]+"\n")

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



#variable
user = 'Karate_Kelly'#raw_input("Admin username:")
pw  = 'Browncow1'#raw_input("Password:")

#get token and URL Key
token = getToken(user, pw)
URLKey = GetURL(token)

#create a file and add header
fileLoc = 'c:\python\manageSupport.csv'#'raw_input("Put in the file path to store the data here \nExample: C:\Documents\FILE.csv \n")
f=open(fileLoc, "w")
header="Username,Full Name, Description,Email,Type, Access,Role,Action\n"
f.write(header)

#get list of users to be removed
userlist = CreateUserlist(token,URLKey)
writeCSV(f)

#analyzeUser = Analyze(token, userlist)
f.close()
