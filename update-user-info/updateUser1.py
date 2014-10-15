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

def userDict():
    maxURL ='http://{}.maps.arcgis.com/sharing/rest/portals/self/users'.format(urlKey)
    request = maxURL +"?f=json&token="+token
    response = requests.get(request)
    jres = json.loads(response.text)
    maxUsers =jres['total']
    start = 1
    number = 50
    #retreive information of all users in organization
    userDict = []
    while start < maxUsers:
        listURL ='http://{}.maps.arcgis.com/sharing/rest/portals/self/users'.format(urlKey)
        request = listURL +"?start="+str(start)+"&num="+str(number)+"&f=json&token="+token
        response = requests.get(request)
        jres = json.loads(response.text)
        for row in jres['users']:
            userDict.append(row)
        start +=number

    return userDict
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
    data = {'f':'json', 'token':token, 'access':'public'}
    for item in userDict:
        if item['username']==line[0]:
            print line[0]
            if item['userType'] != usertype:
                data['userType'] = usertype
            if item['fullName'] != line[1]:
                data['fullName']= line[1]
            if item['description'] != line[2]:
                data['description'] = line[2]
        print data
#updates description, Enables My Esri Access and makes account searchable to public
    userURL ='https://{}.maps.arcgis.com/sharing/rest/community/users/{}/update'.format(urlKey, line[0])
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
    CSV = r"c:\python\usertest.csv"

    #get role
    roleDict = roleDict()
    userDict = userDict()

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







