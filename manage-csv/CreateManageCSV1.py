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
    jres = json.loads(response.text)
    return jres['urlKey'], jres['id']

def CreateUserlist(token, URLKey):
    #get amount of users
    maxURL ='http://{}.maps.arcgis.com/sharing/rest/portals/self/users'.format(URLKey)
    request = maxURL +"?f=json&token="+token
    response = requests.get(request)
    jres = json.loads(response.text)
    maxUsers =jres['total']
    start = 1
    number = 50
    #retreive information of all users in organization
    userDict = []
    while start < maxUsers:
        listURL ='http://{}.maps.arcgis.com/sharing/rest/portals/self/users'.format(URLKey)
        request = listURL +"?start="+str(start)+"&num="+str(number)+"&f=json&token="+token
        response = requests.get(request)
        jres = json.loads(response.text)
        allvals = ['username','fullName', 'description', 'email', 'userType', 'role']
        for row in jres['users']:
           userLst = []
           for val in allvals:
                userLst.append(row[val])
           userLst.append("")
           userLst.append("")
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
    user[5]=roleName

def MyEsri(userType):
    if userType == 'both':
        user[4] = 'My Esri'
    elif userType == 'arcgisonly':
        user[4]= "ArcGIS Online"

def writeCSV(f):
    #updates list to record which emails have been sent to the users
    for user in userlist:
        for i,j in enumerate(user):
            if user[i]:
                user[i] = user[i]
            else:
                user[i] = 'none'
        f.write(user[0]+ "," + user[1]+ "," +user[2]+"," +user[3]+"," +user[4]+"," +user[5]+","+user[6]+","+user[7]+","+user[8]+","+str(user[9])+","+str(user[10])+","+user[11]+"\n")

def Analyze(user):
    #Identifies users with no description
    if not user[2]:
        user[2] = 'none'
        user[8] = 'N'
    else:
        user[8] = 'Y'
    #find duplicate users
    for email in userlist:
        if user[0] != email[0] and user[3] == email[3]:
            user[7] = 'Duplicate'

def creditDict():
    startTime =int(time.time()) -2629743
    EndTime = int(time.time())
    str_ST = str(startTime) + '000'
    str_ET =str(EndTime) + '000'
    creditURL ='http://www.arcgis.com/sharing/rest/portals/{}/usage?'.format(orgID)
    request ="f=json&startTime="+str_ST+"&endTime="+str_ET+"&period=1d&vars=credits%2Cbw%2Cnum%2Cstg&groupby=username&token=" +token

    req = creditURL+request
    response = requests.get(req)
    jres = json.loads(response.text)
    return jres

def appendCreditInfo(user):
    creds = 0
    for item in creditDict['data']:
        try:
            if user[0] == item['username']:
                for x in item['credits']:
                    creds += float(x[1])
        except KeyError:
            pass
        user[9]=creds

def countFeatures(user):
    itemURL ='http://{}.maps.arcgis.com/sharing/rest/content/users/{}'.format(URLKey, user[0])
    request = itemURL +"?f=json&token="+token
    response = requests.get(request)
    jres = json.loads(response.text)
    num = 0
    for item in jres['items']:
         if item['type'] == 'Feature Service':
            for x in item['typeKeywords']:
                if x=='Hosted Service':
                    num +=1
    user[10]= num
def proDict():
    url = 'http://{}.maps.arcgis.com/sharing/rest/content/listings/2d2a9c99bb2a43548c31cd8e32217af6/userEntitlements'.format(URLKey)
    request = url +"?f=json&token="+token
    response = requests.get(request)
    jres = json.loads(response.text)
    return jres

def proEntitlement(user):
     level = 'None'
     for item in proDict['userEntitlements']:
        if user[0] == item['username']:
            for x in item['entitlements']:
                if x == 'desktopAdvN':
                    level = 'Advanced'
                elif x == 'desktopBasicN':
                    level = 'Basic'
                elif x == 'desktopStdN':
                    level = 'Standard'
            user[6]=level

if __name__ == '__main__':
    #variable
    adminUser = raw_input("Admin username:")
    pw  = raw_input("Password:")

    #get token and URL Key
    token = getToken(adminUser, pw)
    accInfo = GetURL(token)
    URLKey = accInfo[0]
    orgID = accInfo[1]

    #create a file and add header
    fileLoc = raw_input("Put in the file path to store the data here \nExample: C:\Documents\FILE.csv \n")
    f=open(fileLoc, "w")
    header="Username,Full Name, Description,Email,Type, Role,Pro License,Duplicate,has Description,Credits Used, Number of Feature Services, Action\n"
    f.write(header)


    #get list of users to be removed
    userlist = CreateUserlist(token,URLKey)
    roleDict =roleDict()
    creditDict = creditDict()
    proDict = proDict()
    print userlist
    for user in userlist:
        roleName= roleName1(str(user[5]))
        Analyze(user)
        appendCreditInfo(user)
        countFeatures(user)
        proEntitlement(user)
        MyEsri(user[4])


    writeCSV(f)
    f.close()
