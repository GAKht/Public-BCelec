"""""
        This script includes signature and verification functions

        Author: Guillaume A. Khayat
        Date: 2022/01/28
"""""
# Importing global parameters
from globImp import *
from globParams import g
from Util.Fcts.compUncompP import compP, uncompP


def rgSig(nonceV, rdSignatures, pubKeys, eL, Kl):
    """""
        This function produces the hashes and nonce EC points in the ring signature:
            - Input:
                - nonceV: integer, the nonce of the eligible voter who is creating the ring signature
                - msgV: str, the encrypted message of the vote message (avoids attack: for every existing vote 
                            create a new vote by copying hashV & eLv but change encrypted voting message)
                - rdSignatures: list of (N-1) random integers, used as signatures in the ring signature 
                - pubKeys: list of (N-1) compressed EC points, the public keys of the (N-1) eligible voters chosen 
                            to be included in the ring signature
                - eL: empty list
                - Kl: empty list
            - Output:
                - e: integer transformation of the hash of latest compressed nonce public EC point in the ring signature 
                        concatenated with the voter's nonce. Used as output to have rgSig as a recursive function
                - eL: not a formal output of the function. The list includes all e (see above) of the ring signature
                - Kl: not a formal output of the function. The list of compressed nonce EC points used 
                        in the ring signature
    """""
    if len(pubKeys) < 2:
        K = g * nonceV
        e = ecdsa.ecdsa.string_to_int(
            hashlib.sha256(( str(compP((K.x(), K.y()))) + str(nonceV) ).encode('utf-8')).hexdigest())
        eL.append(e)
        Kl.append(compP((K.x(), K.y())))
    else:
        e = rgSig(nonceV, rdSignatures[:(len(pubKeys) - 1)], pubKeys[:(len(pubKeys) - 1)], eL, Kl)
    K = g * rdSignatures[(len(pubKeys) - 1)] + uncompP(pubKeys[(len(pubKeys) - 1)]) * (- e)
    e = ecdsa.ecdsa.string_to_int(
        hashlib.sha256((str(compP((K.x(), K.y()))) + str(nonceV) ).encode('utf-8')).hexdigest())
    eL.append(e)
    Kl.append(compP((K.x(), K.y())))
    return e


def indRgSig(secTplV, sigPubKeyFunc):
    """""
        This function produces the hashes and nonce EC points in the ring signature:
            - Input:
                - secTplV: tuple of eligible voter V, it includes:
                            - integer, secret key of voter V
                            - integer, nonce of voter V to be used in the election
                            - list of (N-1) random integers, used in the ring signature 
                                as signatures of the (N - 1) other voters
                - msgV: str, the encrypted message of the vote message (adding it to the ring sig avoids the following 
                                attack: for every existing vote create a new vote by copying hashV & eLv but change 
                                encrypted voting message)
                - sigPubKeyFunc: list of (N - 1) compressed EC public keys to create the ring signature
            - Output:
                - A tuple that contains:
                    - eL: the list includes all integer transformations of the hash of latest compressed 
                            nonce public EC point in the ring signature concatenated with the voter's nonce
                    - Kl: the list of compressed nonce EC points used in the ring signature
    """""
    pubKeyTemp = g * secTplV['secKeyV']
    compPubKeyTemp = compP((pubKeyTemp.to_affine().x(), pubKeyTemp.to_affine().y()))
    idxPubKeyTemp = sigPubKeyFunc.index(compPubKeyTemp)


    pubKeyRgSigTemp = sigPubKeyFunc[(idxPubKeyTemp + 1):len(sigPubKeyFunc)] + sigPubKeyFunc[0: (idxPubKeyTemp)]

    eLtemp = []
    KlTemp = []
    rgSig(secTplV['nonceECptV'], secTplV['sigL'], pubKeyRgSigTemp, eLtemp, KlTemp)
    # elToRet = tuple(eLtemp[((len(eLtemp)-1)-idxPubKeyTemp):len(eLtemp)] + eLtemp[:((len(eLtemp)-1)-idxPubKeyTemp)])
    elToRet = eLtemp[((len(eLtemp) - 1) - idxPubKeyTemp):len(eLtemp)] + eLtemp[:((len(eLtemp) - 1) - idxPubKeyTemp)]
    # KlToRet = tuple(KlTemp[((len(KlTemp))-idxPubKeyTemp):len(KlTemp)] + KlTemp[:((len(KlTemp))-idxPubKeyTemp)])
    KlToRet = KlTemp[((len(KlTemp)) - idxPubKeyTemp):len(KlTemp)] + KlTemp[:((len(KlTemp)) - idxPubKeyTemp)]
    return (elToRet, KlToRet)


def verifF(sigL, sigPubKeyL, Kl, eL):
    """""
            This verifies that the ring signatures are valid. From the signatures in the voter's right 
            and the list of hashes created during the signature process, create the corresponding nonce EC points 
            then compare this list to the list of nonce EC points published in the voting right:
                - Input:
                    - sigL: list of N integers, signatures in the ring signature to be verified
                    - sigPubKeyL: list of N compressed EC points, the public keys used in the ring signature
                    - Kl: list of N compressed EC points, the nonce EC points from the ring signature
                    - eL: list of N integers, hashes from the ring signatures
                - Output:
                    - Boolean:
                        - True: if the two lists are identical (valid vote from the eligible voter)
                        - False: if the two lists are different (invalid vote)
        """""
    KcalL = list(map(lambda a, b, c: g * a + uncompP(b) * (- c) , sigL, sigPubKeyL, eL))
    Kdecomp = list(map(lambda a: uncompP(a) , Kl))
    ver = KcalL == Kdecomp
    return ver

