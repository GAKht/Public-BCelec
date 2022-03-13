"""""
        This script creates the VoteRigh class to impose restrictions on creating voting right

        Author: Guillaume A. Khayat
        Date: 2022/01/29
"""""

class VoteRight:
    def __setattr__(self, name, value):
        if hasattr(self, name):
            raise AttributeError("Cannot modify attributes: VRhash, VRsigL, VRsigPubKeyL or VRsigNonceECpts")
        else:
            super().__setattr__(name, value)

    def __delattr__(self, name, value):
        if name in ["VRhash", "VRsigL", "VRsigPubKeyL"]:
            raise AttributeError("Cannot delete attributes: VRhash, VRsigL, VRsigPubKeyL or VRsigNonceECpts")
        else:
            super().__setattr__(name, value)


    def __init__(self, VRhash, VRsigL, VRsigPubKeyL, VRsigNonceECpts):
        if not isinstance(VRhash, str):
            raise ValueError("Vote right identifier should be a the hash of the voter's nonce")
        self.VRhash = VRhash
        self.VRsigL = VRsigL
        self.VRsigPubKeyL = VRsigPubKeyL
        self.VRsigNonceECpts = VRsigNonceECpts

    def attrDesc(self):
        strVRhash = "VRhash: eligible voter's hashed nonce \n"
        strVRsigL = "VRsigL: tuple containing signatures used in the ring signature to verify the vote \n"
        strVRsigPubKeyL = "VRsigPubKeyL: tuple containing compressed public keys used in the " \
                          "ring signature to verify the vote \n"
        strVRsigNonceECpts = "VRsigNonceECpts: tuple containing compressed nonce EC points used in " \
                             "the ring signature to verify the vote \n"
        print("\n", strVRhash, strVRsigL, strVRsigPubKeyL, strVRsigNonceECpts)
