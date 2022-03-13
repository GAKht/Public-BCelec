"""""
        This script creates the Vote class to impose restrictions on creating a vote

        Author: Guillaume A. Khayat
        Date: 2022/02/19
"""""

class Vote:
    def __setattr__(self, name, value):
        if hasattr(self, name):
            raise AttributeError("Cannot modify attributes: Vid, Vvr, VeL, Vmsg or Vtm")
        else:
            super().__setattr__(name, value)

    def __delattr__(self, name, value):
        if name in ["Vid", "Vvr", "VeL", "Vmsg", "Vtm"]:
            raise AttributeError("Cannot delete attributes: Vid, Vvr, VeL, Vmsg or Vtm")
        else:
            super().__setattr__(name, value)


    def __init__(self, Vid, Vvr, VeL, Vmsg, Vtm):
        if not isinstance(Vid, str):
            raise ValueError("Vote ID should be a the hash of the voter's voting right nonce")
        self.Vid = Vid
        self.Vvr = Vvr
        self.VeL = VeL
        self.Vmsg = Vmsg
        self.Vtm = Vtm


    def attrDesc(self):
        strVid = "Vid: vote ID, the hash of the hash of the voter's voting right nonce and the vote's time stamp \n"
        strVvr = "Vvr: vote right, the hash of the voter's voting right nonce \n"
        strVeL = "VeL: tuple containing the hashes in the ring signature to verify the voter's identity \n"
        strVmsg = "Vmsg: tuple containing the RSA password protected encoded vote message \n"
        strVtm = "Vtm: string, time stamp of the vote creation \n"
        print("\n", strVid, strVvr, strVeL, strVmsg, strVtm)
