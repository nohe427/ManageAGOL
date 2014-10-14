#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      kell6873
#
# Created:     10/10/2014
# Copyright:   (c) kell6873 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import json, time, datetime, string, smtplib
from cookielib import CookieJar

#emails content to users
def eMAIL(gTo, gSubject, gMsg):
   gHOST    = "SMTP.ESRI.COM"
   gFrom    = "kgerrow@esri.com"
   BODY  = string.join((
           "From: %s" % gFrom,
           "To:   %s" % gTo,
           "Subject: %s" % gSubject,
           "",
           gMsg), "\r")
   eMsg = smtplib.SMTP(gHOST)
   eMsg.sendmail(gFrom,gTo,BODY)

def emailUsersUpdateDesc():
    if line[9] == 'N':
        message = "Hello " + line[1]+", \n\nThere is currently no description associated with your ArcGIS Online Account, " +line[0]+". As a new naming convention in the ESS organization, we request that all usernames for Analysts in the organization have their group leads as their description. If you do not have a group lead, feel free to contact Kelly Gerrow about how to proceed. Please update your description to have the first and last name of your group lead. To find out how to modify your profile please look at the following link: http://doc.arcgis.com/en/arcgis-online/reference/profile.htm#GUID-A4615C09-5968-4C67-B5DD-DC796C8CD09A.\n\nPlease let me know if you have any questions, and thank you in advance!\n\nKelly"
        Subject = "Please update your description for " +line[0]+ " in the ESS Organization"
        eMAIL('kgerrow@esri.com', Subject, message)




def emailGroupLeads():
    #fields: username, Fullname, duplicate, credits, number
    pass


def main():
    pass

if __name__ == "__main__":

     #Opens files for reading
    inputCSV= r"C:\ManageAgol\user.csv"
    GLEmails =r"C:\ManageAgol\GLEmail.csv"


    #creates date that emails are sent
    today = datetime.datetime.now()
    form = datetime.datetime.strftime(today, "%m-%d-%y")


    #Opens files
    inputCSVO = open(inputCSV, 'r')
    GLEmailO=open(GLEmails, 'r')


    #reads through COI high confidence list and extracts information
    for read in inputCSVO.readlines():
        line = read.split(",")
        emailUsersUpdateDesc()


##            #reads through sent email list to identify potential duplicates
##            for hello in outputEmail.readlines():
##                print hello
##                splitstring = hello.split(",")
##                #verify that there is a line om file
##                if len(splitstring)>1:
##                    #identifies duplicate crashes as to not send multiple emails
##                    if splitstring[1] == email and cr==splitstring[3]:
##                        print 'emails match and CRs match'
##                        match = True
##                        pass
##                    #closes existing email file
##                    outputEmail.close()
##            #If the email has never been sent, this generates a message and sends the email
##            Subject = "ArcGIS "+ verReport[:5] +" Software Failure"
##            if match == False:
##                message = generateEmail()
##                if message != 'blank':
##                     eMAIL(email, Subject, message)
##                     updateEmail()
    inputCSVO.close()
    GLEmailO.close()

