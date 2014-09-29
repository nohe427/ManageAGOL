#-------------------------------------------------------------------------------
# Name:       Email Organization
# Purpose:    Email all users in the organization
#
# Author:      kell6873
#
# Created:     20/08/2014
# Copyright:   (c) kell6873 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    pass


import json, time, string, smtplib, urllib,requests
from cookielib import CookieJar

# Function to return a token for this session
def getToken(user,pw):
    data = {'username': user,
        'password': pw,
        'referer' : 'https://www.arcgis.com',
        'f': 'json'}
    urlT  = 'https://arcgis.com/sharing/rest/generateToken'
    jres = requests.post(urlT, data=data, verify=False).json()
    return jres['token']

#email address
def eMAIL(gTo, gSubject, gMsg):
   gHOST    = "SMTP.ESRI.COM"
   gFrom    = "email@esri.com"
   BODY  = string.join((
           "From: %s" % gFrom,
           "To:   %s" % gTo,
           "Subject: %s" % gSubject,
           "",
           gMsg), "\r")
   eMsg = smtplib.SMTP(gHOST)
   eMsg.sendmail(gFrom,gTo,BODY)

#Function returns unique URL key for organization
def GetURL(token):
    URL= 'http://www.arcgis.com/sharing/rest/portals/self?f=json&token=' + token
    response = requests.get(URL)
    URLKey = json.loads(response.text)['urlKey']
    return URLKey

#function returns email list for all users in the organization
def getEmail(token, URLKey):
    maxURL ='http://{}.maps.arcgis.com/sharing/rest/portals/self/users'.format(URLKey)
    request = maxURL +"?f=json&token="+token
    response = requests.get(request)
    jres = json.loads(response.text)
    maxUsers = jres['total']
    start = 1
    number = 50
    userlist =[]
    while start < maxUsers:
        listURL ='http://{}.maps.arcgis.com/sharing/rest/portals/self/users'.format(URLKey)
        request = listURL +"?start="+str(start)+"&num="+str(number)+"&f=json&token="+token
        response = requests.get(request)
        jres = json.loads(response.text)
        for item in jres['users']:
            userlist.append(item['email'])
        start+=number
    return userlist

#variables
user=#username
pw=#password

#get token and URL
token=getToken(user,pw)
URLKey= GetURL(token)

#create email list
emailList =getEmail(token,URLKey)
print emailList

message = #insert body of email
subject = #subject of email (suggest starting with Do Not Reply)

#Send the email to each user
for email in emailList:
    try:
        eMAIL(email, subject, message)
    except:
       print 'error'
