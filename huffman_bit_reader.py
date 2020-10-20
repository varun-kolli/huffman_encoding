#
#   Bit-packing reader and writer for Huffman encoder and decoder
#

import struct 
   
# --------------------------------------------------------------------
# HuffmanBitReader is a HuffmanBitReader(string)
class HuffmanBitReader:
    # side effect: open a file with file name 'fname' for reading in binary mode
    def __init__(self, fname):
        self.file = open(fname, 'rb')
        self.n_bits = 0
        self.byte = 0
        self.mask = 0

    # side effect: closes opened file  
    def close(self):
        self.file.close()
      
    # Use this method to read the header from the compressed file. 
    def read_str(self): 
        data = self.file.readline()
        return data.decode('utf-8')
   
    # Use this method to read a single bit from opened file
    # It returns False if a 0 was read, 1 otherwise
    def read_bit(self):  
        if self.mask == 0:     # all bits consumed, need to read in the next byte
            self.byte = self.read_byte()
            self.mask = 1 << 7
        bit = self.byte & self.mask
        self.mask = self.mask >> 1
        if bit == 0:
            return False
        else:
            return True
         
    # Reads a 1 byte from opened file and returns as unsigned int
    # You should not need to call this method
    def read_byte(self):
        return struct.unpack('B', self.file.read(1))[0]  # 1 byte unsigned int      

