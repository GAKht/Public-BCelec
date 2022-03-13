"""""
        This script includes various functions used when a vote is created

        Author: Guillaume A. Khayat
        Date: 2022/02/09
"""""
# Importing global parameters
from globImp import *
from Util.Cls.Vote import Vote as Vote
from Util.Fcts.sigFuncs import indRgSig



def Vvoting(secV, msgVote, votesToVerif, VRlI, pubKeyRSAI):
    """""
        This function creates the vote of the voter V and appends it to the list votesToVerif:
            - Input:
                - secV: tuple, contains the 3 secret information related to the voter V 
                        (see Gvt.01genKey.py for more details)
                - msgVote: str, voting message to be RSA encrypted
                            The voting message before encryption should respect str(nonce)_||msgVote||_str(nonce)
                - votesToVerif: list of compressed EC points, 
                                (N-1) compressed public keys to create the ring signature from 
                - VRlI: list of all voting rights
                - pubKeyRSAI: public RSA keys used in the election
            - Output: 
                - NONE: the function only appends the vote to the list votesToVerif by adding a dict 
    """""
    vVR = hashlib.sha256((str(secV['nonceRightV'])).encode('utf-8')).hexdigest()
    hashVRl = [VR['VRhash'] for VR in VRlI]
    (eLv, KlV) = indRgSig(secV, VRlI[hashVRl.index(vVR)]['VRsigPubKeyL'])

    msgVoteFull = str( str(secV['nonceRightV']) + "_" + str(msgVote) )
    msgVoteCryptedHex = rsa.pkcs1.encrypt(msgVoteFull.encode('utf-8'), rsa.key.PublicKey(pubKeyRSAI['n'], pubKeyRSAI['e'])).hex()
    timeStamp = str(datetime.datetime.now(datetime.timezone.utc))
    ID = hashlib.sha256((str(vVR) + str(timeStamp)).encode('utf-8')).hexdigest()

    voteV = Vote(ID, vVR, eLv, msgVoteCryptedHex, timeStamp)
    votesToVerif.append(
        {
            "Vid": voteV.Vid,
            "Vvr": voteV.Vvr,
            "eLv": voteV.VeL,
            "msgVote": voteV.Vmsg,
            "tStamp": voteV.Vtm
        }
    )
