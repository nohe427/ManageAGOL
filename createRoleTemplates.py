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
def createRole(URLKey, Token):
    roleURL = 'http://{}.maps.arcgis.com/sharing/rest/portals/self/createRole'.format(URLKey)
    roleData= {'name':name, 'description':description, 'f':'json', 'token':token}


    privURL ='http://{}.maps.arcgis.com/sharing/rest/portals/self/roles/{}/setPrivileges'.format(URLKey, roleID)
    privData = {'id':roleID, 'privleges': privleges, 'f':'json', 'token':token}

    privleges = {"privileges":["portal:admin:inviteUsers","portal:admin:viewUsers","portal:admin:updateUsers","portal:admin:viewGroups","portal:admin:updateGroups","portal:admin:assignToGroups","portal:admin:viewItems","portal:admin:updateItems","portal:publisher:publishFeatures","portal:publisher:publishTiles","portal:user:createGroup","portal:user:joinGroup","portal:user:joinNonOrgGroup","portal:user:createItem","portal:user:shareToGroup","portal:user:shareToOrg","portal:user:shareToPublic","portal:user:shareGroupToOrg","portal:user:shareGroupToPublic","features:user:edit","opendata:user:designateGroup","premium:user:geocode","premium:user:networkanalysis","premium:user:spatialanalysis","premium:user:geoenrichment","premium:user:demographics","premium:user:elevation"]}


#variables
user='kellymooc'
pw='Browncow1'

roleDict={'Create, update, and delete':
}
#get token and URL
token=getToken(user,pw)
URLKey= GetURL(token)

