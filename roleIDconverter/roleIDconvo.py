#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      kell6873
#
# Created:     09/10/2014
# Copyright:   (c) kell6873 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    pass

if __name__ == '__main__':
    main()
def roleID(roleName, token):
    # matches role name with role id.
    #note, there is no error messaging so all roles must be valid
    roleUrl= 'http://www.arcgis.com/sharing/rest/portals/self/roles?f=json&token=' + token
    response = requests.get(roleUrl)
    jres = json.loads(response.text)
    roleID = 'blank'
    for item in jres['roles']:
        #print roleName
        if roleName.lower() == item['name'].lower():
            #print roleName.lower() +item['name'].lower()
            roleID = item['id']
        elif roleName.lower() == 'administrator':
            roleID= 'account_admin'
        elif roleName.lower() == 'publisher':
            roleID= 'account_publisher'
        elif roleName.lower() == 'user':
            roleID= 'account_user'
    return roleID

def roleName(roleID, token):
    roleUrl= 'http://www.arcgis.com/sharing/rest/portals/self/roles?f=json&token=' + token
    response = requests.get(roleUrl)
    jres = json.loads(response.text)
    roleID = 'blank'
    for item in jres['roles']:
        #print roleName
        if roleID == item['id']:
            #print roleName.lower() +item['name'].lower()
            roleName = item['name']
        elif roleId == 'account_admin':
            roleName= 'Administrator'
        elif roleId == 'account_publisher':
            roleName= 'Publisher'
        elif roleID == 'account_user':
            roleName= 'User'
