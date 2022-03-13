"""""
        This script creates the RSA secret and public keys

        Author: Guillaume A. Khayat
        Date: 2021/12/19
"""""

# Importing packages and global parameters
from globImp import *
from globParams import pathPubKeyRSA

start = time.time()

rsaNbits = 1500
(pubKeyRSA, secKeyRSA) = rsa.key.newkeys(rsaNbits)

pubKeyRSAToJSON = {
    "n": pubKeyRSA.n,
    "e": pubKeyRSA.e
}
secKeyRSAToJSON = {
    "d": secKeyRSA.d,
    "p": secKeyRSA.p,
    "q": secKeyRSA.q
}

pubKeyRSAjson= json.dumps(pubKeyRSAToJSON, indent = 4)
secKeyRSAjson= json.dumps(secKeyRSAToJSON, indent = 4)

jsonFilePubKeyRSA = open(pathPubKeyRSA, "w")
jsonFilePubKeyRSA.write(pubKeyRSAjson)
jsonFilePubKeyRSA.close()

jsonFileSecKeyRSA = open("Db/secKeyRSAjson.json", "w")
jsonFileSecKeyRSA.write(secKeyRSAjson)
jsonFileSecKeyRSA.close()

end = time.time()
RSAkeyGenTime = end - start
print("RSA key generation script:", RSAkeyGenTime, "seconds")
