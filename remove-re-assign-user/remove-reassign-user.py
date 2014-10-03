#-------------------------------------------------------------------------------
# Name:             Removes User and re-invites user
# Purpose:          Parse through users based on role and remove them from t
#                   the organizaiton, including deleting all content and groups
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
################################################################################
#Warning, This script is designed to remove all content regardless of delete
#protection. Please use carefully or remove the protected content sections


# Function to return a token for this session
def getToken(user, pw):
    data = {'username': user,
        'password': pw,
        'referer' : 'https://www.arcgis.com',
        'f': 'json'}
    url  = 'https://arcgis.com/sharing/rest/generateToken'
    jres = requests.post(url, data=data, verify=False).json()
    return jres['token']

def accountInfo():
    URL= 'http://www.arcgis.com/sharing/rest/portals/self?f=json&token=' + token
    response = requests.get(URL)
    jres = json.loads(response.text)
    return jres

def userInfo():
    url ='http://{}.maps.arcgis.com/sharing/rest/community/users/{}'.format(URLKey,remUser)
    request = url +"?f=json&token="+token
    response = requests.get(request)
    jres = json.loads(response.text)
    userDict = {'fullName':jres['fullName'], 'firstName':jres['firstName'], 'lastName': jres['lastName'], 'description':jres['description'], 'email':jres['email'], 'userType': jres['userType'], 'access': jres['access'],'role':jres['role'], 'tags':jres['tags'], 'culture':jres['culture'], 'region':jres['region'], 'thumbnail':jres['thumbnail'] }
    return userDict

def verifyUser():
    maxURL ='http://{}.maps.arcgis.com/sharing/rest/portals/self/users'.format(URLKey)
    request = maxURL +"?f=json&token="+token
    response = requests.get(request)
    jres = json.loads(response.text)
    maxUsers = jres['total']
    start = 1
    number = 50
    foundUser = False
    while start < maxUsers:
        listURL ='http://{}.maps.arcgis.com/sharing/rest/portals/self/users'.format(URLKey)
        request = listURL +"?start="+str(start)+"&num="+str(number)+"&f=json&token="+token
        response = requests.get(request)
        jres = json.loads(response.text)
        for item in jres['users']:
            if item['username'].lower() == remUser.lower():
                delUser = item['username']
                foundUser = True
        start+=number
    return delUser, foundUser

def reassignContent():
    '''Deletes all of a user's content including protected content and content
    stored in additional folders.'''

    itemURL ='http://{}.maps.arcgis.com/sharing/rest/content/users/{}'.format(URLKey, remUser)
    request = itemURL +"?f=json&token="+token
    response = requests.get(request)
    jres = json.loads(response.text)
    defaultFolderLst = []
    if jres['items']:
        for item in jres['items']:
           raURL='http://{}.maps.arcgis.com/sharing/rest/content/users/{}/items/{}/reassign'.format(URLKey,remUser,item['id'])
           data = {'targetUsername':user, 'targetFolderName':'/', 'f':'json', 'token':token}
           tjres = requests.post(raURL, data=data, verify=False).json()
           defaultFolderLst.append(item['id'])


    if jres['folders']:
        '''Delete content stored in folders'''
        folderLst = {'Folders': []}

        for folder in jres['folders']:
             foldercontentURL ='http://{}.maps.arcgis.com/sharing/rest/content/users/{}/{}?f=json&token={}'.format(URLKey, remUser, folder['id'], token)
             response = requests.get(foldercontentURL)
             jres = json.loads(response.text)

             #itemlist=[]
             if jres['items']:
                itemlist=[]
                for item in jres['items']:
                    itemlist.append(item['id'])
                    rcfURL ='http://{}.maps.arcgis.com/sharing/rest/content/users/{}/{}/items/{}/reassign'.format(URLKey,remUser,folder['id'],item['id'])
                    data = {'targetUsername':user, 'targetFolderName':'/', 'f':'json', 'token':token}
                    jres = requests.post(rcfURL, data=data, verify=False).json()


                folderLst['Folders'].append({'items':[itemlist],'folderName':folder['title'], 'folderID':folder['id']})
    return defaultFolderLst, folderLst



def reassignGroups():

        groupURL ='http://{}.maps.arcgis.com/sharing/rest/community/users/{}'.format(URLKey, remUser)
        request = groupURL +"?f=json&token="+token
        response = requests.get(request)
        jres = json.loads(response.text)
        grouplst=[]
        for item in jres['groups']:
            reassignURL = 'http://{}.maps.arcgis.com/sharing/rest/community/groups/{}/reassign'.format(URLKey,item['id'])
            data = {'f':'json', 'targetUsername': user,'token':token}
            response=requests.post(reassignURL, data=data).json()
            print response
            grouplst.append(item['id'])
        return grouplst


def delUser():
       #disable MyEsri Access to completly delete the account
       updateURL ='https://{}.maps.arcgis.com/sharing/rest/community/users/{}/update'.format(URLKey, remUser)
       data = {'f':'json','usertype':'arcgisonly','token':token}
       response = requests.post(updateURL, data=data, verify=False).json()

        #delete username
       userURL ='http://{}.maps.arcgis.com/sharing/rest/community/users/{}/delete'.format(URLKey, remUser)
       data = {'f':'json', 'token':token}
       response=requests.post(userURL, data=data).json()

def inviteUser():
    #invite users from spreadsheet
    url = 'http://{}.maps.arcgis.com/sharing/rest/portals/self/invite'.format(URLKey)
    #subject and text for email
    subject = 'An invitation to join an ArcGIS Online Organization, ' + accountInfo['name'] + '. DO NOT REPLY'
    text = '<html><body><p>' + user+ ' has invited you to join an ArcGIS Online Organization, ' +accountInfo['name'] + '. Please click this link to join:<br><a href="https://www.arcgis.com/home/signin.html?invitation=@@invitation.id@@">https://www.arcgis.com/home/signin.html?invitation=@@invitation.id@@</a></p><p>If you have difficulty signing in, please email your administrator at hellokitty@hotmail.com. Be sure to include a description of the problem, your username, the error message, and a screenshot.</p><p>For your reference, you can access the home page of the organization here: <br>http://'+URLKey +'.maps.arcgis.com/home/</p><p>This link will expire in two weeks.</p><p style="color:gray;">This is an automated email, please do not reply.</p></body></html>'

    #send invitation without sending an email notification to user
    invitationlist = '{"invitations":[{"username":"'+remUser+'", "password":"Password123", "firstname":"' + userDict['firstName']+'","lastname":"'+userDict['lastName']+'","fullname":"'+userDict['fullName']+'","email":"'+userDict['email']+'","role":"org_publisher"}]}'
    data={'subject':subject, 'html':text, 'invitationlist':invitationlist,'f':'json', 'token':token}
    jres = requests.post(url, data=data, verify=False).json()

    #updates description, Enables My Esri Access and makes account searchable to public
    userURL ='https://{}.maps.arcgis.com/sharing/rest/community/users/{}/update'.format(URLKey, remUser)
    data = {'f':'json','usertype': userDict['userType'],'description': userDict['description'], 'access':userDict['access'],'tags':userDict['tags'], 'culture':userDict['culture'], 'region':userDict['region'], 'thumbnail':userDict['thumbnail'],'token':token}
    response = requests.post(userURL, data=data, verify=False).json()

    updateURL = 'http://{}.maps.arcgis.com/sharing/rest/portals/self/updateUserRole'.format(URLKey)
    data ={'f':'json', 'token':token ,'user':remUser,'role':userDict['role']}
    response = requests.post(updateURL, data=data, verify=False).json()

def assignContent(defaultLst,folderLst):
    if folderLst:
        for item in folderLst['Folders']:
            urlFol ='http://{}.maps.arcgis.com/sharing/rest/content/users/{}/createFolder'.format(URLKey,remUser)
            data = {'title': item['folderName'], 'folderName': item['folderName'],'f':'json', 'token':token}
            response = requests.post(urlFol, data=data, verify=False).json()
            for row in item['items']:
                for id in row:
                    raURL='http://{}.maps.arcgis.com/sharing/rest/content/users/{}/items/{}/reassign'.format(URLKey,user,id)
                    data = {'targetUsername':remUser, 'targetFolderName':item['folderName'], 'f':'json', 'token':token}
                    tjres = requests.post(raURL, data=data, verify=False).json()
    if defaultLst:
         for id in defaultLst:
            raURL='http://{}.maps.arcgis.com/sharing/rest/content/users/{}/items/{}/reassign'.format(URLKey,user,id)
            data = {'targetUsername':remUser, 'targetFolderName':'/', 'f':'json', 'token':token}
            tjres = requests.post(raURL, data=data, verify=False).json()
def assignGroups(grouplst):
    for item in grouplst:
        reassignURL = 'http://{}.maps.arcgis.com/sharing/rest/community/groups/{}/reassign'.format(URLKey,item)
        data = {'f':'json', 'targetUsername': remUser,'token':token}
        response=requests.post(reassignURL, data=data).json()





if __name__ == '__main__':

    #variables
    user = 'essIsoOne'# raw_input("Admin username:")
    pw  = 'essIsoOne'#raw_input("Password:")

    remUser= 'poopy1'#raw_input("Which user needs to be removed?")


    #get token and URL Key
    token = getToken(user, pw)
    accountInfo = accountInfo()
    URLKey = accountInfo['urlKey']


    #get list of users to be removed
    userCase = verifyUser()
    remUser = userCase[0]
    userDict= userInfo()
    if userCase[1] == False:
        print 'Please restart as the username is not located in this organization'
    else:
        lists = reassignContent()
        defaultLst = lists[0]
        folderLst=lists[1]
        grouplst=reassignGroups()
        delUser()
        inviteUser()
        assignContent(defaultLst, folderLst)
        assignGroups(grouplst)






