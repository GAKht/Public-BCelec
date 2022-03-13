"""""
        This script determines all the global parameters needed for this project

        Author: Guillaume A. Khayat
        Date: 2021/12/19
"""""


from globImp import *


# The number of voters in the system
nVoters = 10
N = 3

# Initializing the main ECDSA parameters
g = ecdsa.ecdsa.generator_secp256k1
gOrderL = [g.order()] * nVoters


# Paths to be used in exporting and importing JSON
pathVotes = "../Verif/VoteBckChain/votes.json"
pathSecAllV = "../Voter/Db/secAllVjson.json"
pathPubKeyRSA = "../Verif/PubParams/pubKeyRSAjson.json"
pathVoteRights = "../Verif/PubParams/voteRights.json"
pathPubKeyCompL = "../Verif/PubParams/pubKeyCompL.json"
pathBlocks = "../Verif/VoteBckChain/blocks.json"

