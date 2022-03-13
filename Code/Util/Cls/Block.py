"""""
        This script creates the Block class to impose restrictions on creating a block to be added to the blockchain

        Author: Guillaume A. Khayat
        Date: 2022/02/02
"""""
import hashlib

class Block:
    def __setattr__(self, name, value):
        if hasattr(self, name):
            raise AttributeError("Cannot modify attributes: Bhash, BprevHash and Vids")
        else:
            super().__setattr__(name, value)

    def __delattr__(self, name, value):
        if name in ["Bhash", "BprevHash", "Vids"]:
            raise AttributeError("Cannot delete attributes: Bhash, BprevHash and Vids")
        else:
            super().__setattr__(name, value)


    def __init__(self, BprevHash, Vids):
        # if not isinstance(Bhash, str):
        #     raise ValueError("Bhash should be the hash of this block, the hash of BprevHash||Vids")
        if not isinstance(BprevHash, str):
            raise ValueError("BprevHash should be the hash of the previous block")
        if not isinstance(Vids, tuple):
            raise ValueError("Vids should be a tuple of valid votes IDs to be included in this block")
        self.Bhash = hashlib.sha256((str(BprevHash) + str(Vids)).encode('utf-8')).hexdigest()
        self.BprevHash = BprevHash
        self.Vids = Vids

    def attrDesc(self):
        strBhash = "Bhash: the hash of this block \n"
        strBprevHash = "BprevHash: hash of the previous block \n"
        strVids = "Vid: tuple of valid votes IDs to be included in this block \n"
        print("\n", strBhash, strBprevHash, strVids)
