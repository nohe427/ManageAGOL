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
import json, time, datetime



# Function to return a token for this session
def getToken(adminUser, pw):
    data = {'username': adminUser,
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
    maxUsers = jres['total']
    start = 1
    number = 50
    #retreive information of all users in organization
    userDict = []
    while start < maxUsers:
        listURL ='http://{}.maps.arcgis.com/sharing/rest/portals/self/users'.format(URLKey)
        request = listURL +"?start="+str(start)+"&num="+str(number)+"&f=json&token="+token
        response = requests.get(request)
        jres = json.loads(response.text)
        allvals = ['username','fullName', 'description', 'email', 'userType', 'access', 'role']
        for row in jres['users']:
           userLst = []
           for val in allvals:
                userLst.append(row[val])
           userLst.append("")
           userLst.append("")
           userLst.append("")
           userLst.append("")
           userDict.append(userLst)
        start +=number
    return userDict

def roleDict():
    roleUrl= 'http://www.arcgis.com/sharing/rest/portals/self/roles?f=json&token=' + token
    response = requests.get(roleUrl)
    jres = json.loads(response.text)
    return jres

def roleName1(roleID):
    roleName = 'blank'
    for item in roleDict['roles']:
        #print roleName
        if roleID == item['id']:
            #print roleName.lower() +item['name'].lower()
            roleName = item['name']
        elif roleID == 'org_admin':
            roleName= 'Administrator'
        elif roleID == 'org_publisher':
            roleName= 'Publisher'
        elif roleID == 'org_user':
            roleName= 'User'
    user[6]=roleName

def writeCSV(f):
    #updates list to record which emails have been sent to the users
    for user in userlist:
        for i,j in enumerate(user):
            if user[i]:
                user[i] = user[i]
            else:
                user[i] = 'none'
        f.write(user[0]+ "," + user[1]+ "," +user[2]+"," +user[3]+"," +user[4]+"," +user[5]+","+user[6]+","+user[7]+","+user[8]+","+user[9]+","+user[10]+"\n")

def Analyze(user):
    #Identifies users with no description
    if not user[2]:
        user[2] = 'none'
        user[9] = 'N'
    else:
        user[9] = 'Y'
    #find duplicate users
    for email in userlist:
        if user[0] != email[0] and user[3] == email[3]:
            user[8] = 'Duplicate'

def appendCreditInfo(user):
    startTime =int(time.time()) -2629743
    EndTime = int(time.time())
    str_ST = str(startTime) + '000'
    str_ET =str(EndTime) + '000'
    creditURL ='http://www.arcgis.com/sharing/rest/portals/{}/usage?'.format(orgID)
    request ="f=json&startTime="+str_ST+"&endTime="+str_ET+"&period=1d&username="+user[0]+"&vars=credits%2Cstg&groupby=stype%2Cetype&token=" +token
    req = creditURL+request
    response = requests.get(req)
    jres = json.loads(response.text)
    creds=0
    for item in jres['data']:
        for x in item['credits']:
            creds += float(x[1])
    user[10]=creds

if __name__ == '__main__':
    #variable
    adminUser = raw_input("Admin username:")
    pw  = raw_input("Password:")

    #get token and URL Key
    token = getToken(adminUser, pw)
    URLKey = GetURL(token)

    #create a file and add header
    fileLoc = raw_input("Put in the file path to store the data here \nExample: C:\Documents\FILE.csv \n")
    f=open(fileLoc, "w")
    header="Username,Full Name, Description,Email,Type, Access,Role,Action,duplicate,hasDesc,credits\n"
    f.write(header)


    #get list of users to be removed
    userlist = CreateUserlist(token,URLKey)
    roleDict =roleDict()
    print userlist
    for user in userlist:
        roleName= roleName1(str(user[6]))
        Analyze(user)
        appendCreditInfo(user)


    writeCSV(f)
    f.close()
