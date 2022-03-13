"""""
        This script includes functions that compresses and uncompresses Elleptic Curve points of secp256k1

        Author: Guillaume A. Khayat
        Date: 2022/01/07
"""""
# Importing packages and global parameters
import ecdsa
import Util.Fcts.TonelliShanks as TonelliShanks
# # Importing packages and global parameters
# from globImp import *
# from globParams import nVoters, N, g, gOrderL


def uncompP(compP):
    """""
        This function uncompresses an Elliptic Curve of secp256k1:
            - Input: an integer corresponding to the compressed ECDSA point 
                     prefix || integer
                        prefix: 
                            1 if y is negative
                            2 if y is positive
                        integer: int(, 10) base 10 corresponding the x coordinate of the point
            - Output: (x, y) coordinates 
    """""
    if not isinstance(compP, int):
        return print("Compressed Elliptic Curve point should be an integer")
    elif str(compP)[0] not in ["1", "2"]:
        return print("Incorrect input, prefix must be: \n"
                     + " " * 5 + "1 if y is negative to the modulo number n\n"
                     + " " * 5 + "2 if y is positive to the modulo number n")
    else:
        curveSP = ecdsa.ecdsa.curve_secp256k1
        primeN = 2 ** 256 - 2 ** 32 - 2 ** 9 - 2 ** 8 - 2 ** 7 - 2 ** 6 - 2 ** 4 - 1  # The modulus integer
        xCoor = int(str(compP)[1:len(str(compP))]) % primeN
        yCoor = TonelliShanks.tonelli(pow(xCoor, 3, primeN) + 7, primeN)
        if str(compP)[0] == "1":
            pToReturn = (xCoor, primeN - yCoor)
            if not curveSP.contains_point(pToReturn[0], pToReturn[1]):
                return print("Incorrect input, the compressed point is not part of secp256k1")
            else:
                # return pToReturn
                return ecdsa.ellipticcurve.PointJacobi(curveSP, pToReturn[0], pToReturn[1], 1, generator=False)
        elif str(compP)[0] == "2":
            pToReturn = (xCoor, yCoor)
            if not curveSP.contains_point(pToReturn[0], pToReturn[1]):
                return print("Incorrect input, the compressed point is not part of secp256k1")
            else:
                # return pToReturn
                return ecdsa.ellipticcurve.PointJacobi(curveSP, pToReturn[0], pToReturn[1], 1, generator=False)




def compP(uncompP):
    """""
        This function compresses an Elliptic Curve of secp256k1:
            - Input: (x, y) coordinates 
            - Output: an integer corresponding to the compressed ECDSA point 
                     prefix || integer
                        prefix: 
                            1 if y is negative
                            2 if y is positive
                        integer: int(, 10) base 10 corresponding the x coordinate of the point
    """""
    if (not isinstance(uncompP, tuple)) or (not len(uncompP) == 2):
        return print("Uncompressed Elliptic Curve point should be a tuple of length 2")
    elif (not isinstance(uncompP[0], int)) or ((not isinstance(uncompP[1], int))):
        return print("The coordinates of the uncompressed Elliptic Curve point should be integers")
    else:
        curveSP = ecdsa.ecdsa.curve_secp256k1
        if not curveSP.contains_point(uncompP[0], uncompP[1]):
            return print("Incorrect input, the uncompressed point is not part of secp256k1")
        primeN = 2 ** 256 - 2 ** 32 - 2 ** 9 - 2 ** 8 - 2 ** 7 - 2 ** 6 - 2 ** 4 - 1  # The modulus integer
        xCoor = uncompP[0] % primeN
        yCoor = TonelliShanks.tonelli(pow(xCoor, 3, primeN) + 7, primeN)
        if( uncompP[1] == (primeN - yCoor)):
            # print(yCoor)
            return int((str(1) + str(xCoor)))
        elif( uncompP[1] == yCoor ):
            # print(yCoor)
            return int((str(2) + str(xCoor)))

