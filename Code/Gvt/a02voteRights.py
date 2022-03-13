"""""
        This script is written to generate initial transactions that include the voting rights:
            - A database that includes n number of transactions (n is the number of eligible voters)
            - Each transaction includes: 
                - Input: empty
                - Output: the digested hash of the eligible elector's public key and a nonce r hash(r || pubKey)
                
        Author: Guillaume A. Khayat
        Date: 2022/01/08
"""""

# Importing packages and global parameters
from globImp import *
from globParams import pathVoteRights
from Util.Fcts.voteRightsFcts import voteRightFunc


start = time.time()


exec(open('secImport.py').read())



voteRdicts = []
voteRightL = list(map(lambda a: voteRightFunc(a, voteRdicts), secAllJson ))
random.shuffle(voteRdicts)
voteRjson = json.dumps(voteRdicts, indent = 4)

jsonFile = open(pathVoteRights, "w")
jsonFile.write(voteRjson)
jsonFile.close()


end = time.time()
voteRightsTime = end - start
print("Vote Rights script:", voteRightsTime, "seconds")
