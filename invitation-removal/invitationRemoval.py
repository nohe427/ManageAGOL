#-------------------------------------------------------------------------------
# Name:        AGOL maintenance
# Purpose:
#
# Author:      kell6873
#
# Created:     30/09/2014
# Copyright:   (c) kell6873 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import os, os.path
import sys
import urllib2, urllib, requests
import json

#variables
user = ''#raw_input("Admin username:")
pw  = ''#raw_input("Password:")

# Function to return a token for this session
def getToken(user, pw):
    data = {'username': user,
        'password': pw,
        'referer' : 'https://www.arcgis.com',
        'f': 'json'}
    url  = 'https://arcgis.com/sharing/rest/generateToken'
    jres = requests.post(url, data=data, verify=False).json()
    return jres['token']

#Revtreives short URL
def accountInfo(token):
    URL= 'http://www.arcgis.com/sharing/rest/portals/self?f=json&token=' + token
    response = requests.get(URL)
    jres = json.loads(response.text)
    return jres['urlKey']
#Creates list of invitation IDs
def pendingInvite(token, urlKey):
    URL = 'http://{}.maps.arcgis.com/sharing/rest/portals/self/invitations'.format(urlKey)
    request = URL +"?f=json&token="+token
    response = requests.get(request)
    jres = json.loads(response.text)
    total = jres['total']
    start = 1
    number = 50
    invitelist =[]
    while start < total:
        listURL ='http://{}.maps.arcgis.com/sharing/rest/portals/self/invitations'.format(urlKey)
        request = listURL +"?start="+str(start)+"&num="+str(number)+"&f=json&token="+token
        response = requests.get(request)
        jres = json.loads(response.text)
        for item in jres['invitations']:
            invitelist.append(item['id'])
        start+=number
    return invitelist

#removes old invitaitons
def removeInvites(token, urlKey, invitelist):
    for id in invitelist:
        url='http://{}.maps.arcgis.com/sharing/rest/portals/self/invitations/{}/delete'.format(urlKey,id)
        data = {'token':token, 'f':'json'}
        response = requests.post(url, data=data).json()


#calls functions
token = getToken(user,pw)
urlKey=accountInfo(token)
invitelist = pendingInvite(token, urlKey)
removeInvites = removeInvites(token, urlKey, invitelist)




