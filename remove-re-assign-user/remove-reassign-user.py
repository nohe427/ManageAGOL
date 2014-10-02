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
    return jres['urlKey']

def verifyUser(delUser):
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
            if item['username'].lower() == delUser.lower():
                delUser = item['username']
                foundUser = True
        start+=number
    return delUser, foundUser

def reassignContent( URLKey, token, protected=True):
    '''Deletes all of a user's content including protected content and content
    stored in additional folders.'''

    itemURL ='http://{}.maps.arcgis.com/sharing/rest/content/users/{}'.format(URLKey, user)
    request = itemURL +"?f=json&token="+token
    response = requests.get(request)
    jres = json.loads(response.text)

    if jres['items']:
        for item in jres['items']:
            itemID= item['id']
            print "Attempting to re-assign item ID:{}".format(itemID)
            if item['protected']:
                if protected:
                    '''delete protected data'''
                    unprotectURL = 'http://{}.maps.arcgis.com/sharing/rest/content/users/{}/items/{}/unprotect'.format(URLKey,user,itemID)
                    data = {'f':'json', 'token':token}
                    response = sendRequest(unprotectURL,urllib.urlencode(data))
                    delURL = 'http://{}.maps.arcgis.com/sharing/rest/content/users/{}/items/{}/delete'.format(URLKey,user,itemID)
                    response = sendRequest(delURL,urllib.urlencode(data))

                else:
                    print "Cannot delete item id {} because it is protected; the user will not be deleted.".format(item['id'])

            else:
                '''delete unprotected data'''
                delURL = 'http://{}.maps.arcgis.com/sharing/rest/content/users/{}/items/{}/delete\n\n'.format(URLKey,user,itemID)
                data = {'f':'json', 'token':token}
                response = sendRequest(delURL,urllib.urlencode(data))

    else:
        print 'No items to delete in the default folder.'


    if jres['folders']:
        '''Delete content stored in folders'''
        for folder in jres['folders']:
            folderID = folder['id']
            foldercontentURL ='http://{}.maps.arcgis.com/sharing/rest/content/users/{}/{}?f=json&token={}'.format(URLKey, user, folderID, token)
            response = requests.get(foldercontentURL)
            jres = json.loads(response.text)

            if jres['items']:
                for item in jres['items']:
                    itemID= item['id']
                    print "Attempting to delete item ID:{}".format(itemID)

                    if item['protected']:
                        if protected:
                            '''delete protected data'''
                            unprotectURL = 'http://{}.maps.arcgis.com/sharing/rest/content/users/{}/{}/items/{}/unprotect'.format(URLKey,user,folderID,itemID)
                            data = {'f':'json', 'token':token}
                            response = sendRequest(unprotectURL,urllib.urlencode(data))
                            delURL = 'http://{}.maps.arcgis.com/sharing/rest/content/users/{}/{}/items/{}/delete'.format(URLKey,user,folderID, itemID)
                            response = sendRequest(delURL,urllib.urlencode(data))

                        else:
                            print "Cannot delete item id {} located in folder {} because it is protected; the user will not be deleted.".format(item['id'], folderID)
                    else:
                        '''delete unprotected data'''
                        if item['ownerFolder']:
                            delURL = 'http://{}.maps.arcgis.com/sharing/rest/content/users/{}/{}/items/{}/delete'.format(URLKey,user,folderID,itemID)
                            data = {'f':'json', 'token':token}
                            response = sendRequest(delURL,urllib.urlencode(data))

            #delete the folder
            try:
                folderURL = 'http://{}.maps.arcgis.com/sharing/rest/content/users/{}/{}/delete'.format(URLKey,user,folderID)
                data = {'f':'json','token':token}
                response = sendRequest(folderURL,urllib.urlencode(data))
                print "Folder {} has been deleted.".format(folderID)

            except KeyError:
                print "Unable to delete folder {}, please check that all of the items were deleted from it first.".format(folderID)

def delGroups(userlist, URLKey, token):
    for user in userlist:
        groupURL ='http://{}.maps.arcgis.com/sharing/rest/community/users/{}'.format(URLKey, user)
        request = groupURL +"?f=json&token="+token
        response = requests.get(request)
        jres = json.loads(response.text)
        for row in jres['groups']:
            if row['id'] != "":
                delURL = 'http://{}.maps.arcgis.com/sharing/rest/community/groups/{}/delete'.format(URLKey,row['id'])
                data = {'f':'json',
                        'token':token}
                response = sendRequest(delURL,urllib.urlencode(data))
                print "deleting is a group" + row['id']

def delUser(userlist, URLKey, token):
    for user in userlist:
        userURL ='http://{}.maps.arcgis.com/sharing/rest/community/users/{}/delete'.format(URLKey, user)
        data = {'f':'json',
                'token':token}
        response = sendRequest(userURL,urllib.urlencode(data))
        if response['success'] is True:
            print 'Deleted the following user: ' +user
        else:
            print 'user was not deleted'


if __name__ == '__main__':

    #variables
    user = 'Karate_Kelly'# raw_input("Admin username:")
    pw  = 'Browncow1'#raw_input("Password:")

    delUser= 'AaKanKsha_ess'#raw_input("Which user needs to be removed?")

    #get token and URL Key
    token = getToken(user, pw)
    URLKey = accountInfo()


    #get list of users to be removed
    userCase = verifyUser(delUser)
    if userCase[1] == False:
        break
    else:
        print userCase[0]



    #delete user content:
    #delCont = delContent(userlist, URLKey, token)

    #delete user groups
    #delGroup = delGroups(userlist, URLKey, token)

    #delete user
    #delUsers = delUser(userlist, URLKey, token)


