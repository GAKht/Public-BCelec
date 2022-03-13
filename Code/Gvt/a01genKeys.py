"""""
        This script generates all needed secret information and saves it in a JSON

        Author: Guillaume A. Khayat
        Date: 2022/01/30
"""""

# Importing packages and global parameters
from globImp import *
from globParams import nVoters, N, g, pathSecAllV, pathPubKeyCompL
from Util.Fcts.genKeysFcts import jsonSecAll
from Util.Fcts.compUncompP import compP

secAllGvtDB = "Db/secAlljson.json"

# Generating random numbers to be used as the secret key, the nonce to initiate the ring signature (voting right)
# and the random numbers to be used in the ring signature as signatures of the (nVoters - 1) other voters
# global secAll, secL
secAll = []
for _ in range(nVoters):
    # secAll.append( ( secrets.randbelow(g.order()), secrets.randbelow(g.order()), tuple(map(secrets.randbelow, [g.order()] * (N-1) )), tuple(random.sample(range(nVoters), N - 1)) ) )
    secAll.append((secrets.randbelow(g.order()), secrets.randbelow(g.order()), secrets.randbelow(g.order()),
                   tuple(map(secrets.randbelow, [g.order()] * (N - 1)))))
secAll = tuple(secAll)




secAlldict = list(map(lambda a: jsonSecAll(a), secAll ))
secAlljson = json.dumps(secAlldict, indent = 4)

jsonFileSecAll = open(secAllGvtDB, "w")
jsonFileSecAll.write(secAlljson)
jsonFileSecAll.close()

secAllVjson = json.dumps(secAlldict[0], indent = 4)
jsonFileSecAllV = open(pathSecAllV, "w")
jsonFileSecAllV.write(secAllVjson)
jsonFileSecAllV.close()

# The two below JSONs are used for testing purposes only - CONSIDER DELETING BEFORE RELEASE
secAllVjson2 = json.dumps(secAlldict[1], indent = 4)
jsonFileSecAllV2 = open("../Voter/Db/secAllV2json.json", "w")
jsonFileSecAllV2.write(secAllVjson2)
jsonFileSecAllV2.close()

secAllVjson3 = json.dumps(secAlldict[2], indent = 4)
jsonFileSecAllV3 = open("../Voter/Db/secAllV3json.json", "w")
jsonFileSecAllV3.write(secAllVjson3)
jsonFileSecAllV3.close()



# Generating public keys
secL = tuple([secAllV[0] for secAllV in secAll])

# Eligible voter's public key
pubKeyL = list(map(lambda x: ecdsa.ecdsa.Public_key( g, g * x , verify = True), secL))
pubKeyCompL = list(map(lambda a: compP( (a.point.to_affine().x(), a.point.to_affine().y()) ), pubKeyL ))
# Export public keys to a JSON
pubKeyCompLjson = json.dumps(pubKeyCompL, indent = 4)
jsonFilePubKeyCompL = open(pathPubKeyCompL, "w")
jsonFilePubKeyCompL.write(pubKeyCompLjson)
jsonFilePubKeyCompL.close()



