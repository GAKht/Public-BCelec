"""""
        This script creates eligible votes, including repetitive eligible votes for testing

        Author: Guillaume A. Khayat
        Date: 2022/02/08
"""""
# Importing global parameters
from globImp import *
from globParams import pathVotes, pathSecAllV, pathPubKeyRSA, pathVoteRights
from Util.Fcts.voteRightsFcts import listToTupleVR
from Util.Fcts.voteFcts import Vvoting
import os


# # Importing the list of secret information of all eligible voters
# jsonFile = open(pathSecAllV, "r")
# secAllV = json.load(jsonFile)
# jsonFile.close()

# # Importing the list of secret information of all eligible voters
# jsonFile = open("../Voter/Db/secAllV2json.json", "r")
# secAllV = json.load(jsonFile)
# jsonFile.close()

# Importing the list of secret information of all eligible voters
jsonFile = open("Db/secAllV3json.json", "r")
secAllV = json.load(jsonFile)
jsonFile.close()

# Importing RSA public key
jsonFile = open(pathPubKeyRSA, "r")
pubKeyRSA = json.load(jsonFile)
jsonFile.close()

# Importing voting rights
jsonFile = open(pathVoteRights, "r")
y = json.load(jsonFile)
jsonFile.close()

tuple(map(lambda a: listToTupleVR(a), y ))
VRl = tuple(y)

# msgVote = "Anwar"
msgVote = "Guillaume"



if os.path.isfile(pathVotes):
    # Importing votes to verify
    jsonFilevotesImp = open(pathVotes, "r")
    votesToVerifI = json.load(jsonFilevotesImp)
    jsonFilevotesImp.close()
else:
    votesToVerifI = []


Vvoting(secAllV, msgVote, votesToVerifI, VRl, pubKeyRSA)


# Exporting the appended list of votes to verify
votesToVerifIjson = json.dumps(votesToVerifI, indent = 4)
jsonFilevotesExp = open(pathVotes, "w")
jsonFilevotesExp.write(votesToVerifIjson)
jsonFilevotesExp.close()



