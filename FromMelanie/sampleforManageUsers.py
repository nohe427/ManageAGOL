
def readLine(openedfile):
    line = openedfile.readline()
    splitstring = line.split(",")
    return splitstring

def inviteUser(line):
    data = {'description': line[1]}
    request = ""

def updateUser(line):
    data = {}
    request = ""


if __name__ == "__main__":

    CSV = r"\\kellyg\python\manage_AgolUser.csv"
    openedfile = open(CSV, 'r')
    openedfile.readline()
    openedfile.readline()

    while True:
      line = readLine(openedfile)
      inviteUser(line)
      if not line:
        break