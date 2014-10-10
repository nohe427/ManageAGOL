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


def main():
    pass

if __name__ == "__main__":

     #Opens files for reading
    inputEmails= r"C:\COI\HCEmailsoct6.txt"
    sentEmails =r"C:\COI\SentEmail.csv"
    crdoc = r"C:\COI\Newcrlist.txt"

    #creates date that emails are sent
    today = datetime.datetime.now()
    form = datetime.datetime.strftime(today, "%m-%d-%y")


    #Opens files
    openedfile = open(inputEmails, 'r')
    crreport= open(crdoc, 'w')


    #reads through COI high confidence list and extracts information
    for line in openedfile.readlines():
        inputInfo = line.split(";")
        print len(inputInfo)
        if len(inputInfo) == 1:
            break
        else:
            #sets variables based on information from current line
            #cr causing crash
            cr= inputInfo[2]
            #email of user who experienced crash
            email = inputInfo[3]
            #date of crash dump
            date=inputInfo[4]
            #version that experienced crash
            verReport = inputInfo[5]
            match=False
            #opens file with emails that have been sent
            outputEmail=open(sentEmails, 'r')
            #reads through sent email list to identify potential duplicates
            for hello in outputEmail.readlines():
                print hello
                splitstring = hello.split(",")
                #verify that there is a line om file
                if len(splitstring)>1:
                    #identifies duplicate crashes as to not send multiple emails
                    if splitstring[1] == email and cr==splitstring[3]:
                        print 'emails match and CRs match'
                        match = True
                        pass
                    #closes existing email file
                    outputEmail.close()
            #If the email has never been sent, this generates a message and sends the email
            Subject = "ArcGIS "+ verReport[:5] +" Software Failure"
            if match == False:
                message = generateEmail()
                if message != 'blank':
                     eMAIL(email, Subject, message)
                     updateEmail()
    openedfile.close()
    crreport.close()

