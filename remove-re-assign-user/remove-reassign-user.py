#-------------------------------------------------------------------------------
# Name:             Removes User and re-invites user and reassigns content
# Purpose:          To overcome an issue with abondonned pro licesnes, this will
#                   remove and re-add the user, returning the pro-license to the organization
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

#retreives organizaiton account information
def accountInfo():
    URL= 'http://www.arcgis.com/sharing/rest/portals/self?f=json&token=' + token
    response = requests.get(URL)
    jres = json.loads(response.text)
    return jres

#makes a dictionary of user information to be applied when the user is re-added
def userInfo():
    url ='http://{}.maps.arcgis.com/sharing/rest/community/users/{}'.format(URLKey,remUser)
    request = url +"?f=json&token="+token
    response = requests.get(request)
    jres = json.loads(response.text)
    userDict = {}
    allvals = ['fullName', 'firstName', 'lastName', 'description', 'email', 'userType', 'access', 'role', 'tags', 'culture', 'region', 'thumbnail']
    for val in allvals:
        try:
            userDict[val] = jres[val]
        except KeyError:
            userDict[val] = "Not Found"
    return userDict

#verifies the correct case of the username
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
                return delUser, foundUser
        start+=number
    return foundUser

#assigns content to the administrative user running the script. Creates dictionaries
#to reassign content after the user is re-added
def reassignContent():
    '''Deletes all of a user's content including protected content and content
    stored in additional folders.'''

    #finds and reassigns content in the default folder
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

    #finds and reassigns content in any folders
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
    try:
        folderLst
    except UnboundLocalError:
        folderLst = []
        return defaultFolderLst, folderLst


#Reassigns Groups to the administrator running the script
def reassignGroups():

        groupURL ='http://{}.maps.arcgis.com/sharing/rest/community/users/{}'.format(URLKey, remUser)
        request = groupURL +"?f=json&token="+token
        response = requests.get(request)
        jres = json.loads(response.text)
        groupOlst=[]
        groupMlst=[]
        for item in jres['groups']:
            if item['userMembership']['memberType'] == 'owner':
                reassignURL = 'http://{}.maps.arcgis.com/sharing/rest/community/groups/{}/reassign'.format(URLKey,item['id'])
                data = {'f':'json', 'targetUsername': user,'token':token}
                response=requests.post(reassignURL, data=data).json()
                print response
                groupOlst.append(item['id'])
            elif item['userMembership']['memberType'] == 'member' :
                groupMlst.append(item['id'])

        return groupOlst, groupMlst

#Deletes that account after removing My Esri access (this returns the license)
def delUser():
       #disable MyEsri Access to completly delete the account
       updateURL ='https://{}.maps.arcgis.com/sharing/rest/community/users/{}/update'.format(URLKey, remUser)
       data = {'f':'json','usertype':'arcgisonly','token':token}
       response = requests.post(updateURL, data=data, verify=False).json()

        #delete username
       userURL ='http://{}.maps.arcgis.com/sharing/rest/community/users/{}/delete'.format(URLKey, remUser)
       data = {'f':'json', 'token':token}
       response=requests.post(userURL, data=data).json()

#readds the user without sending an email invitation.
def inviteUser():

    url = 'http://{}.maps.arcgis.com/sharing/rest/portals/self/invite'.format(URLKey)
    #subject and text for email  (required)
    subject = 'SampleSubject'
    text = 'some text'
    #send invitation without sending an email notification to user
    invitationlist = '{"invitations":[{"username":"'+remUser+'", "password":"Password123", "firstname":"' + userDict['firstName']+'","lastname":"'+userDict['lastName']+'","fullname":"'+userDict['fullName']+'","email":"'+userDict['email']+'","role":"org_publisher"}]}'
    data={'subject':subject, 'html':text, 'invitationlist':invitationlist,'f':'json', 'token':token}
    jres = requests.post(url, data=data, verify=False).json()

    #updates account information collected originally
    userURL ='https://{}.maps.arcgis.com/sharing/rest/community/users/{}/update'.format(URLKey, remUser)
    data = {'f':'json','usertype': userDict['userType'],'description': userDict['description'], 'access':userDict['access'],'tags':userDict['tags'], 'culture':userDict['culture'], 'region':userDict['region'], 'thumbnail':userDict['thumbnail'],'token':token}
    response = requests.post(userURL, data=data, verify=False).json()

    #updates role to previous role
    updateURL = 'http://{}.maps.arcgis.com/sharing/rest/portals/self/updateUserRole'.format(URLKey)
    data ={'f':'json', 'token':token ,'user':remUser,'role':userDict['role']}
    response = requests.post(updateURL, data=data, verify=False).json()

#Assigns content back to original user
def assignContent(defaultLst,folderLst):
    #re-assigns content into created folders
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

    #re-assigns content into default directories
    if defaultLst:
         for id in defaultLst:
            raURL='http://{}.maps.arcgis.com/sharing/rest/content/users/{}/items/{}/reassign'.format(URLKey,user,id)
            data = {'targetUsername':remUser, 'targetFolderName':'/', 'f':'json', 'token':token}
            tjres = requests.post(raURL, data=data, verify=False).json()

#re-assigns group
def assignGroups(groupOlst):
    for item in groupOlst:
        reassignURL = 'http://{}.maps.arcgis.com/sharing/rest/community/groups/{}/reassign'.format(URLKey,item)
        data = {'f':'json', 'targetUsername': remUser,'token':token}
        response=requests.post(reassignURL, data=data).json()
def readdGroups(groupAlst):
    for item in groupOlst:
        AddURL = 'http://{}.maps.arcgis.com/sharing/rest/community/groups/{}/addUsers'.format(URLKey,item)
        data = {'f':'json', 'users': remUser,'token':token}
        response=requests.post(AddURL, data=data).json()


if __name__ == '__main__':

    #variables
    user = raw_input("Admin username:")
    pw  = raw_input("Password:")

    remUser= raw_input("Which user needs to be reset?")


    #get token and URL Key
    token = getToken(user, pw)
    accountInfo = accountInfo()
    URLKey = accountInfo['urlKey']


    #verify the case of the username and executes functions
    userCase = verifyUser()
    if userCase == False:
        print 'Please restart as the username is not located in this organization'
    else:
        remUser = userCase[0]
        userDict= userInfo()

        lists = reassignContent()
        defaultLst = lists[0]
        folderLst=lists[1]
        grouplst=reassignGroups()
        groupOlst = grouplst[0]
        groupMlst = grouplst[1]
        delUser()
        inviteUser()
        assignContent(defaultLst, folderLst)
        assignGroups(groupOlst)
        readdGroups(groupMlst)






