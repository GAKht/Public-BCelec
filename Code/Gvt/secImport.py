"""""
        This script imports secret information of the JSON

        Author: Guillaume A. Khayat
        Date: 2022/01/30
"""""


# Importing the list of secret information of all eligible voters
jsonFile = open("Db/secAlljson.json", "r")
y = json.load(jsonFile)
jsonFile.close()
# print(y)

def listToTuple(secVint):
    secVint['sigL'] = tuple(secVint['sigL'])

tuple(map(lambda a: listToTuple(a), y ))
secAllJson = tuple(y)
