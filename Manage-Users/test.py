#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      kell6873
#
# Created:     01/10/2014
# Copyright:   (c) kell6873 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def readLine(openedfile):
    line = openedfile.readline()
    #line = line.rstrip('\n')
    print line
    splitstring = line.split(",")
    return splitstring

if __name__ == '__main__':
    CSV = r"\\kellyg\python\manage_AgolUser.csv"
    openedfile = open(CSV, 'r')
    openedfile.readline()
    openedfile.readline()

    while True:
        line = readLine(openedfile)
        print len(line)
        #invitelist = inviteUsers(line)
        if len(line) == 1:
            break