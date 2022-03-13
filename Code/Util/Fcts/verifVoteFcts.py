"""""
        This script includes various functions used for vote functions

        Author: Guillaume A. Khayat
        Date: 2022/02/20
"""""
# Importing global parameters
import datetime
from Util.Fcts.sigFuncs import verifF
from collections import Counter


def verVote(vote, VRfctInt):
    """""
        An intermediary function used in checking if the vote is valid of not
        It gets the vote right related to the vote to verify and returns a boolean if the vote is valid or not
    """""
    vrVotes = list(filter(lambda item: item['VRhash'] == vote['Vvr'], VRfctInt))
    if len(vrVotes) == 0:
        print("No voting right that correspond to this vote")
        return
    return verifF(vrVotes[0]['VRsigL'], vrVotes[0]['VRsigPubKeyL'], vrVotes[0]['VRsigNonceECpts'], vote['eLv'])


def vIDfinFct(vIDfct, vIDtoRemFct):
    """""
        An intermediary function used to remove replicated votes 
        (could be replicate in difference with only vote message => fraud)
    """""
    if len(vIDtoRemFct) == 0:
        return vIDfct
    elif len(vIDtoRemFct) < 2:
        return list(filter((vIDtoRemFct[0]).__ne__, vIDfct))
    else:
        return vIDfinFct(list(filter((vIDtoRemFct[(len(vIDtoRemFct)-1)]).__ne__, vIDfct)), vIDtoRemFct[:(len(vIDtoRemFct)-1)])

def firstTmStamp(vVR, vldVotes):
    """""
        An intermediary function used to get the vote with the first time stamp when replicated votes are available
    """""
    vIDvotes = list(filter(lambda item: item['Vvr'] == vVR, vldVotes))
    voteTmStamp = min(vIDvotes, key=lambda x:datetime.datetime.strptime(x['tStamp'], '%Y-%m-%d %H:%M:%S.%f%z'))
    return voteTmStamp


def verVotesToBck(voteDictL, VRfctInt):
    """""
        This function verifies which of the votes provided as input are valid and returns them as output
                - Input:
                    - voteDictL: list of dict, the list of votes to be verified
                    - VRfctInt: list of dict, list of all voting rights
                - Output:
                    - validVotes: list of dict, 
                                    list of valid votes from the list of votes provided as input to the function
    """""
    # Check which of the saved votes are valid eLv wise (second validation step to be checked later)
    boolVotes = list(map(lambda a: verVote(a, VRfctInt), voteDictL))
    indTrue = [i for i in range(len(boolVotes)) if boolVotes[i] == True]
    validEl = [voteDictL[i] for i in indTrue]
    # From the list of valid (1st step check), is there any replicate?
    #    - If yes, pick the first vote time stamp wise
    vIDl = list(map(lambda a: a['Vvr'], validEl))
    cntVid = Counter(vIDl)
    vIDtoRem = list(filter(lambda item: cntVid[item] > 1, cntVid))

    vIDnoRep = vIDfinFct(vIDl, vIDtoRem)
    vldVotesNoRep = list(filter(lambda item: item['Vvr'] in vIDnoRep, validEl))

    vldVotesRep = list(map(lambda a: firstTmStamp(a, validEl), vIDtoRem))
    validVotes = vldVotesNoRep + vldVotesRep
    return validVotes

