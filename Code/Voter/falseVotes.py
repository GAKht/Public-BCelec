"""""
        This script creates non-valid votes for testing purposes of the verification process

        Author: Guillaume A. Khayat
        Date: 2022/02/08
"""""
# Importing global parameters
import time

from globImp import *
from globParams import pathVotes, pathSecAllV, pathPubKeyRSA, pathVoteRights
from Util.Fcts.voteRightsFcts import listToTupleVR
import os
from Util.Cls.Vote import Vote as Vote
from Util.Fcts.sigFuncs import indRgSig


nFalseVotes = 100

# Importing the list of secret information of all eligible voters
jsonFile = open(pathSecAllV, "r")
secV = json.load(jsonFile)
jsonFile.close()

# Importing RSA public key
jsonFile = open(pathPubKeyRSA, "r")
pubKeyRSAI = json.load(jsonFile)
jsonFile.close()

# Importing voting rights
jsonFile = open(pathVoteRights, "r")
y = json.load(jsonFile)
jsonFile.close()

tuple(map(lambda a: listToTupleVR(a), y ))
VRlI = tuple(y)

msgVote = str(secV['nonceRightV']) + "_" + "Guillaume"



if os.path.isfile(pathVotes):
    # Importing votes to verify
    jsonFilevotesImp = open(pathVotes, "r")
    votesToVerif = json.load(jsonFilevotesImp)
    jsonFilevotesImp.close()
else:
    votesToVerif = []



hashV = hashlib.sha256((str(secV['nonceRightV'])).encode('utf-8')).hexdigest()
hashVRl = [VR['VRhash'] for VR in VRlI]


(eLv, KlV) = indRgSig(secV, VRlI[hashVRl.index(hashV)]['VRsigPubKeyL'])

msgVoteCryptedHex = rsa.pkcs1.encrypt(msgVote.encode('utf-8'), rsa.key.PublicKey(pubKeyRSAI['n'], pubKeyRSAI['e'])).hex()
# print(eLv)
# print([eLv[0]+1] + eLv[1:len(eLv)])

for i in range(nFalseVotes):
    time.sleep(1)
    # eLv2 = [eLv[0]+1] + eLv[1:len(eLv)]
    timeStamp = str(datetime.datetime.now(datetime.timezone.utc))
    vID = hashlib.sha256((str(str(hashV) + str(timeStamp))).encode('utf-8')).hexdigest()
    eLv2 = eLv[0:(len(eLv)-2)] + [eLv[len(eLv)-1] + 1]
    voteV = Vote(vID, hashV, eLv2, msgVoteCryptedHex, timeStamp)
    votesToVerif.append(
        {
            "Vid": voteV.Vid,
            "Vvr": voteV.Vvr,
            "eLv": voteV.VeL,
            "msgVote": voteV.Vmsg,
            "tStamp": voteV.Vtm
        }
    )

# Exporting the appended list of votes to verify
votesToVerifIjson = json.dumps(votesToVerif, indent = 4)
jsonFilevotesExp = open(pathVotes, "w")
jsonFilevotesExp.write(votesToVerifIjson)
jsonFilevotesExp.close()
