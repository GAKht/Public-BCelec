"""""
        This script includes several functions used during the generation of the voting rights

        Author: Guillaume A. Khayat
        Date: 2022/02/19
"""""
# Importing packages and global parameters
from globImp import *
from globParams import nVoters, N, g, pathPubKeyCompL
from Util.Cls.VoteRight import VoteRight
from Util.Fcts.compUncompP import compP
from Util.Fcts.sigFuncs import indRgSig

# Importing the list of secret information of all eligible voters
jsonFile = open(pathPubKeyCompL, "r")
pubKeyCompL = json.load(jsonFile)
jsonFile.close()


def voteRightFunc(secV, voteRjsonInt):
    """""
            The function to create voting right for the eligible voter V using VoteRight class and appends
            vote rights to :
                - Input:
                    - secV: tuple that contains secret information of eligible voter V (3 elements)
                            - 0: integer, secret key of eligible voter V
                            - 1: integer, nonce of eligible voter V used in the ring signature
                            - 2: tuple of (N-1) random integers used as signatures in the ring signature
                    - voteRjsonInt: empty list to add dict of voting rights
                - Output:
                    - VoteRight object
    """""
    pubKeyV = g * secV['secKeyV']
    compPubKeyV = compP((pubKeyV.to_affine().x(), pubKeyV.to_affine().y()))

    VsigPubKeyIdx = random.sample(range(nVoters), N - 1)
    VsigPubKeyL = [pubKeyCompL[i] for i in VsigPubKeyIdx] + [compPubKeyV]
    random.shuffle(VsigPubKeyL)
    VidxPubKeySig = VsigPubKeyL.index(compPubKeyV)
    VeL = indRgSig(secV, VsigPubKeyL)[0]

    VsigL = secV['sigL'][((len(secV['sigL'])) - VidxPubKeySig):len(secV['sigL'])] \
            + ((VeL[VidxPubKeySig] * secV['secKeyV'] + secV['nonceECptV']) % g.order(),) \
            + secV['sigL'][:((len(secV['sigL'])) - VidxPubKeySig)]
    vrV = VoteRight(hashlib.sha256((str(secV['nonceRightV'])).encode('utf-8')).hexdigest(),
                    VsigL, tuple(VsigPubKeyL), tuple(indRgSig(secV, VsigPubKeyL)[1]))
    voteRjsonInt.append(
        {
            "VRhash": vrV.VRhash,
            "VRsigL": vrV.VRsigL,
            "VRsigPubKeyL": vrV.VRsigPubKeyL,
            "VRsigNonceECpts": vrV.VRsigNonceECpts
        }
    )
    return vrV


def listToTupleVR(dictVR):
    """""
        This function converts the elements of a voting right to tuples to avoid changes in the elements:
            - Input:
                - dictVR: dict, an element of the list of voting rights after importing it from the JSON
            - Output:
                - dictVR: dict, the change is the type of its values being changed to tuple
    """""
    dictVR['VRsigL'] = tuple(dictVR['VRsigL'])
    dictVR['VRsigPubKeyL'] = tuple(dictVR['VRsigPubKeyL'])
    dictVR['VRsigNonceECpts'] = tuple(dictVR['VRsigNonceECpts'])

