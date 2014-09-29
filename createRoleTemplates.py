#-------------------------------------------------------------------------------
# Name:       Create Role Templates
# Purpose:    Create Initial Role Templates for education organization
#
# Author:      kell6873
#
# Created:     20/08/2014
# Copyright:   (c) kell6873 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    pass


import json, urllib,requests


# Function to return a token for this session
def getToken(user,pw):
    data = {'username': user,
        'password': pw,
        'referer' : 'https://www.arcgis.com',
        'f': 'json'}
    urlT  = 'https://arcgis.com/sharing/rest/generateToken'
    jres = requests.post(urlT, data=data, verify=False).json()
    return jres['token']

#Function returns unique URL key for organization
def GetURL(token):
    URL= 'http://www.arcgis.com/sharing/rest/portals/self?f=json&token=' + token
    response = requests.get(URL)
    URLKey = json.loads(response.text)['urlKey']
    return URLKey

#function creates sample roles
def createRole(L):

#variables
user='kellymooc'
pw='Browncow1'

#get token and URL
token=getToken(user,pw)
URLKey= GetURL(token)

