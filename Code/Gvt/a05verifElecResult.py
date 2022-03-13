"""""
        This script verifies the blockchain and provides the election results

        Author: Guillaume A. Khayat
        Date: 2022/02/22
"""""
# Importing packages and global parameters
from globImp import *
from globParams import pathBlocks, pathVotes, pathVoteRights, pathPubKeyRSA
from Util.Fcts.bckFcts import verBckchain, orderBckchain, verVotesFromBck

# Importing the Blocks of the blockchain to be verified
jsonFileBlocks = open(pathBlocks, "r")
blockchain = json.load(jsonFileBlocks)
jsonFileBlocks.close()

# Importing the votes to be verified
jsonFileVotes = open(pathVotes, "r")
votesToVerif = json.load(jsonFileVotes)
jsonFileVotes.close()

# Importing the voting rights
jsonFileVR = open(pathVoteRights, "r")
VR = json.load(jsonFileVR)
jsonFileVR.close()

# Importing the voting rights
jsonFileSecKeyRSA = open("../Gvt/Db/secKeyRSAjson.json", "r")
secKeyRSA = json.load(jsonFileSecKeyRSA)
jsonFileSecKeyRSA.close()

# Importing the voting rights
jsonFilePubKeyRSA = open(pathPubKeyRSA, "r")
pubKeyRSA = json.load(jsonFilePubKeyRSA)
jsonFilePubKeyRSA.close()


###### Getting the blocks in the blockchain that are valid
ordVldBckchain = verBckchain(blockchain, votesToVerif, VR)['ordVldBckchain']

# print(ordVldBckchain)

###### Making the second check: nonce before the _ in the vote message is equal to the Vvr
bckchainVidsAllL = list(map(lambda x: x['Vids'], ordVldBckchain))
bckchainVidsAll = []
for i in bckchainVidsAllL:
    bckchainVidsAll += i

bckchainVotes = list(filter(lambda x: x['Vid'] in bckchainVidsAll, votesToVerif))
bckchainMsgs = list(map(lambda x: x['msgVote'], bckchainVotes))

decrMsgs = list(map(lambda x: rsa.pkcs1.decrypt(bytearray.fromhex(x), rsa.key.PrivateKey(pubKeyRSA['n'], pubKeyRSA['e'], secKeyRSA['d'], secKeyRSA['p'], secKeyRSA['q'])).decode('utf-8'), bckchainMsgs))


vNonceMsgs = list(map(lambda x: hashlib.sha256((x[0:x.index("_")]).encode('utf-8')).hexdigest() , decrMsgs))
bckchainVvrAll = list(map(lambda x: x['Vvr'], bckchainVotes))

boolVldVotes = list(map(lambda x, y: x == y , bckchainVvrAll, vNonceMsgs))

# Valid votes (2nd check)
bckchainVldVotes = [bckchainVotes[i] for i in range(len(bckchainVotes)) if boolVldVotes[i] == True]

# Messages from the valid votes (1st & 2nd checks)
bckchainVldMsgs = list(map(lambda x: x['msgVote'], bckchainVldVotes))

# Decrypting the vote messages of valid votes
decrVldMsgs = list(map(lambda x: rsa.pkcs1.decrypt(bytearray.fromhex(x), rsa.key.PrivateKey(pubKeyRSA['n'], pubKeyRSA['e'], secKeyRSA['d'], secKeyRSA['p'], secKeyRSA['q'])).decode('utf-8'), bckchainVldMsgs))

vldMsgs = list(map(lambda x: x[(x.index("_")+1):len(x)], decrVldMsgs))


unqElem = list(set(vldMsgs))
pctElem = list(map(lambda x: vldMsgs.count(x)/len(vldMsgs), unqElem))

# The final result of the election
elecRes = dict(zip(unqElem, pctElem))
print(elecRes)

