"""""
        This script initializes the blockchain used in the election
        It creates the initial block of the blockchain

        Author: Guillaume A. Khayat
        Date: 2022/01/30
"""""

# Importing packages and global parameters
from globImp import *
from globParams import g, pathBlocks


initBckNonces = {
    "Nonce1": secrets.randbelow(g.order()),
    "Nonce2": secrets.randbelow(g.order())
}

initBckNoncesJSON = json.dumps(initBckNonces, indent = 4)

jsonFileInitBckNonces = open("Db/initBckNonces.json", "w")
jsonFileInitBckNonces.write(initBckNoncesJSON)
jsonFileInitBckNonces.close()


initBck = {
            "Bhash": hashlib.sha256(str(str(initBckNonces['Nonce1']) + "Initial Block" + str(initBckNonces['Nonce2'])).encode('utf-8')).hexdigest(),
            "BprevHash": "",
            "Vids": tuple()
            }

initBckJSON = json.dumps([initBck], indent = 4)

jsonFileInitBck = open(pathBlocks, "w")
jsonFileInitBck.write(initBckJSON)
jsonFileInitBck.close()

