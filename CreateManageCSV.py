#-------------------------------------------------------------------------------
# Name:        Create Management Spreadsheet
# Purpose:
#
# Author:      Kelly Gerrow
# Created:     09/08/2014
# Copyright:   (c) kell6873 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

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
#import xml.dom.minidom as DOM
import os, os.path
import sys
import urllib2, urllib, requests
import json

#variables
user = 'Karate_Kelly'#raw_input("Admin username:")
pw  = 'Browncow1'#raw_input("Password:")

#create a file and add header
fileLoc = r'c:\python\manageCSV3.csv'#'raw_input("Put in the file path to store the data here \nExample: C:\Documents\FILE.csv \n")
f=open(fileLoc, "w")
header="Username,Description,Email,Full Name,Role,Action\n"
f.write(header)

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

def CreateCSV(token, URLKey,f):
    maxURL ='http://{}.maps.arcgis.com/sharing/rest/portals/self/users'.format(URLKey)
    request = maxURL +"?f=json&token="+token
    response = requests.get(request)
    jres = json.loads(response.text)
    maxUsers = jres['total']
    start = 1
    number = 50
    while start < maxUsers:
        listURL ='http://{}.maps.arcgis.com/sharing/rest/portals/self/users'.format(URLKey)
        request = listURL +"?start="+str(start)+"&num="+str(number)+"&f=json&token="+token
        response = requests.get(request).json()
        #jres = json.loads(response.text)
        for row in response['users']:
            print str(row['username']) + str(row['description']) + str(row['email']) + str(row['fullName'])
            f.write("{0},{1},{2},{3},{4}\n".format(str(row['username']),
                                           str(row['description']),
                                           str(row['email']),
                                           str(row['fullName']),
                                           str(row['role'])))
        start+=number


#get token and URL Key
token = getToken(user, pw)
URLKey = GetURL(token)

#get list of users to be removed
userlist = CreateCSV(token,URLKey,f)
f.close()
