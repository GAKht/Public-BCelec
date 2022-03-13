"""""
        This script verifies if a vote is valid and can be added to a block:
            - First step verification only 
            - Checks if the ring signature is valid 
        After the verification above, a block is created that includes the valid vote IDs

        Author: Guillaume A. Khayat
        Date: 2022/02/13
"""""
# Importing packages and global parameters
from globImp import *
from globParams import pathVotes, pathVoteRights, pathBlocks
from Util.Fcts.verifVoteFcts import verVotesToBck
from Util.Fcts.bckFcts import orderBckchain, bckToDict
from Util.Cls.Block import Block

# Importing the votes to be verified
jsonFileVotes = open(pathVotes, "r")
votesToVerif = json.load(jsonFileVotes)
jsonFileVotes.close()

# Importing the voting rights
jsonFileVR = open(pathVoteRights, "r")
VR = json.load(jsonFileVR)
jsonFileVR.close()

# Importing the blockchain
jsonFileBlocks = open(pathBlocks, "r")
initBlock = json.load(jsonFileBlocks)
jsonFileBlocks.close()

# Getting the IDs of only the valid votes from the list of all registered votes
vldVotes = verVotesToBck(votesToVerif, VR)
vIDsToAdd = tuple(map(lambda item: item['Vid'], vldVotes))

# Ordering the blockchain
orderedBckChainL = []
orderBckchain(initBlock, orderedBckChainL)

# Creating the new block which includes the valid votes and preparing the updated blockchain to be exported
currBlocksJSON = json.dumps(initBlock + [bckToDict(Block( orderedBckChainL[0], tuple(vIDsToAdd) ))], indent = 4)

# Exporting the appended blockchain
jsonFileBlocksW = open(pathBlocks, "w")
jsonFileBlocksW.write(currBlocksJSON)
jsonFileBlocksW.close()

