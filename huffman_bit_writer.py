import struct 

#   Bit-packing writer for Huffman encoder
class HuffmanBitWriter:
    # side effect: open a file with file name 'fname' for writing in binary mode
    def __init__(self, fname):
        self.file = open(fname, 'wb') # open a file with file name fname
        self.n_bits = 0               # Number of accumulated bits so far
        self.byte = 0                 # accumulated bits represented as byte 

   # Use this method to close the compressed file 
    def close(self):
      # need to pad remaining bits in byte with 0s and write them to file
        if self.n_bits > 0:
            self.byte = self.byte << (7-self.n_bits)
            self.file.write(struct.pack('B', self.byte)) 
        self.file.close()
      
    # Use this method to write the header to the compressed file. 
    def write_str(self, str): # str is a string
        self.file.write(str.encode('utf-8'))
   
    # Use this method to write individual 0 and 1 bits to the compressed file  
    def write_code(self, code): # code is a string of '0's and '1's
        for bit in code:
            if bit == '1': self.byte += 1
            if self.n_bits == 7:
                self.file.write(struct.pack('B', self.byte)) 
                self.byte = 0
                self.n_bits = 0
            else:
                self.byte = self.byte << 1
                self.n_bits += 1
   
