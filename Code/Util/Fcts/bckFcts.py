"""""
        This script includes various functions used when a block is validated and created

        Author: Guillaume A. Khayat
        Date: 2022/02/17
"""""
# Importing global parameters
from Util.Cls.Block import Block
from Util.Fcts.sigFuncs import verifF
from collections import Counter

def orderBckchain(bckChainL, orderedBckChainInt):
    """""
        This function creates a list of block hashes by order
        The first hash in the produced list is the hash of the last block of the blockchain (only non-parent block) 
        and the last hash in the produced list is the hash of the initial block of the blockchain 
        As only the government can create blocks, this function does not treat the situation 
        where there are forks (it only flags it)
            - Input:
                    - bckChainL: list of dict, python object from reading the JSON that saves 
                                    all the blocks of the blockchain
                    - orderedBckChainInt: list, the produced list of the ordered hashes will be appended to this list
    """""
    bckHashes = tuple(map(lambda item: item['Bhash'], bckChainL))
    bckPrevHashes = tuple(map(lambda item: item['BprevHash'], bckChainL))
    diffLists = list(set(bckHashes) - set(bckPrevHashes))
    if len(diffLists) > 1:
        print("Forks in the Blockchain")
        return
    lastBck = diffLists[0]
    if len(bckChainL) < 2:
        orderedBckChainInt.append(bckChainL[0]['Bhash'])
        # return list( bckChainL[0]['Bhash'] )
    else:
        lastBckL = list(filter(lambda item: item['Bhash'] == lastBck, bckChainL))
        if len(lastBckL) > 1:
            print("SOMETHING IS WRONG WITH BLOCK LIST")
            return
        orderedBckChainInt.append( lastBckL[0]['Bhash'] )
        # del bckChainL[bckChainL.index(lastBckL[0])]
        # orderBckChain(bckChainL, orderedBckChainInt)
        orderBckchain(bckChainL[0:bckChainL.index(lastBckL[0])] + bckChainL[(bckChainL.index(lastBckL[0])+1):len(bckChainL)], orderedBckChainInt)


def verVotesFromBck(voteIDs, votesAll, vrAll):
    """""
        This function verifies if any vote of a vote list is not valid. It is destined to verify if a block is valid 
        by verifying that all votes included in the block are valid.
            - Input: 
                - voteIDs: list of strings, each string is the vote ID. List of vote IDs to be verified
                - votesAll: list of dicts, list of all posted votes
                - vrAll: list of dicts, list of all voting rights created by the government
            - Output: 
                - Boolean: 
                    - True if all votes are valid
                    - False if ANY of the votes is not valid
    """""
    if len(voteIDs) == 0:
        return True
    voteDicts = list(filter(lambda a: a['Vid'] in voteIDs, votesAll))
    # Check 1: does the block include several votes from the same voting right?
    vVRl = list(map(lambda a: a['Vvr'], voteDicts))
    cntVid = Counter(vVRl)
    if max(list(cntVid.values())) > 1:
        print("The block includes several votes from the same voting right")
        return False
    # Check 2: Are the votes valid (eLv)?
    vVRll = list(map(lambda a: list(filter(lambda b: b['VRhash'] == a['Vvr'], vrAll)), voteDicts))
    vVRl = [vr for vrL in vVRll for vr in vrL]
    # list(map(lambda a: , vVRl))
    boolVerif = list(map(lambda a, b: verifF(b['VRsigL'], b['VRsigPubKeyL'], b['VRsigNonceECpts'], a['eLv']), voteDicts, vVRl))
    if any(boolVerif) == False:
        blckBool = False
    else:
        blckBool = True
    return blckBool


def bckListDictToBlock(bckDictL):
    return tuple(map(lambda item: Block(item['BprevHash'], item['Vids']) , bckDictL))

def bckListBlockToDict(bckBlockL):
    return tuple(map(lambda item: {
        'Bhash': item.Bhash,
        'BprevHash': item.BprevHash,
        'Vids': item.Vids
    } , bckBlockL))

def bckToDict(blk):
    return (
        {
            "Bhash": blk.Bhash,
            "BprevHash": blk.BprevHash,
            "Vids": blk.Vids
        }
    )

def verBckchain(bckchainDictL, votesAll, vrAll):
    """""
            This fuction orders and verifies what blocks of a blockchain are valid.
            - Input: 
                - bckchainDictL: the blockchain, list of dict. Each dict is a block of the blockchain to verify
                - votesAll: list of dicts, list of all posted votes
                - vrAll: list of dicts, list of all voting rights created by the government
            - Output: 
                - Dict:
                    - ordBckchain: list of dict, the same blockchain as provided in the input but ordered
                                    (first element is the initial block & last element is the last and only child block) 
                    - ordVldBckchain: list of dict, the ordered valid blockchain
                                        All blocks are valid, the last dict of the list if the last valid block 
                                        of the full blockchain provided in the input
                    - nonValBck: 
                        - if there is any non valid block, the index of the first non valid block 
                            of the ordered blockchain 
                        - if all blocks are valid, the length of the blockchain 
    """""
    orderedBckchainL = []
    orderBckchain(bckchainDictL, orderedBckchainL)
    orderedBckchainL.reverse()
    bckchainDictL.sort(key=lambda i: orderedBckchainL.index(i['Bhash']))
    boolBlocks = tuple(map(lambda a: verVotesFromBck(a['Vids'], votesAll, vrAll), bckchainDictL))
    try:
        valBcks = boolBlocks.index(False)
    except:
        valBcks = len(bckchainDictL)
    return {'ordBckchain': bckchainDictL, 'ordVldBckchain': bckchainDictL[0:valBcks], 'nonValBck': valBcks}
