from ordered_list import *
from huffman_bit_writer import *
from huffman_bit_reader import *
import os

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char   # stored as an integer - the ASCII character code value
        self.freq = freq   # the freqency associated with the node
        self.left = None   # Huffman tree (node) to the left
        self.right = None  # Huffman tree (node) to the right


    def __eq__(self, other):
        '''Needed in order to be inserted into OrderedList'''
        if self is None or other is None:
            return False
        else:
            return self.freq == other.freq and self.char == other.char


    def __lt__(self, other):
        '''Needed in order to be inserted into OrderedList'''
        if self.freq < other.freq:
            return True
        elif self.freq == other.freq:
            if self.char < other.char:
                return True
            else:
                return False

    def __repr__(self):
        x = "Frequency: {0}, Char: {1}".format(self.freq, self.char)
        return x


def cnt_freq(filename):
    '''Opens a text file with a given file name (passed as a string) and counts the 
    frequency of occurrences of all the characters within that file'''
    l = [0] * 256
    f = open(filename, 'r')
    r = f.read()
    for i in r:
        x = ord(i)
        l[x] += 1
    f.close()
    return l

def create_huff_tree(char_freq):
    '''Create a Huffman tree for characters with non-zero frequency
    Returns the root node of the Huffman tree'''
    if len(char_freq) == 0:
        return None
    elif len(char_freq) == 1:
        return HuffmanNode(chr(0), char_freq[0])
    l = OrderedList()
    for i in range(len(char_freq)):
        if char_freq[i] > 0:
            node = HuffmanNode(i, char_freq[i])
            l.add(node)

    while l.size() > 1:
        lefter =  l.pop(0)
        righter = l.pop(0)
        int_freq = lefter.freq + righter.freq
        int_char = min(righter.char, lefter.char)
        internal = HuffmanNode(int_char, int_freq)
        internal.right = righter
        internal.left = lefter
        l.add(internal)
    return l.pop(0)

def inorder_helper(node, l, count):
    if node is not None:
        inorder_helper(node.left, l, count + "0")
        inorder_helper(node.right, l, count + "1")
        if node.left is None and node.right is None:
            l.append([node.char, count])
    return l

def create_code(node):
    '''Returns an array (Python list) of Huffman codes. For each character, use the integer ASCII representation 
    as the index into the arrary, with the resulting Huffman code for that character stored at that location'''
    n = [""] * 256
    l = []
    count = ""
    arr = inorder_helper(node, l, count)
    for i in range(len(arr)):
        index = arr[i][0]
        value = arr[i][1]
        n[index] = value
    return n

def create_header(freqs):
    '''Input is the list of frequencies. Creates and returns a header for the output file
    Example: For the frequency list asscoaied with "aaabbbbcc, would return “97 3 98 4 99 2” '''
    ret = []
    for i in range(len(freqs)):
        if freqs[i] > 0:
            #ret = ret + str(i) + " " + str(freqs[i]) + " "
            ret.append(str(i))
            ret.append(str(freqs[i]))

    return " ".join(ret)

def huffman_encode(in_file, out_file):
    '''Takes inout file name and output file name as parameters - both files will have .txt extensions
    Uses the Huffman coding process on the text from the input file and writes encoded text to output file
    Also creates a second output file which adds _compressed before the .txt extension to the name of the file.
    This second file is actually compressed by writing individual 0 and 1 bits to the file using the utility methods 
    provided in the huffman_bits_io module to write both the header and bits.
    Take not of special cases - empty file and file with only one unique character'''

    if not os.path.exists(in_file):
        raise FileNotFoundError
    count = 0
    freqlist = cnt_freq(in_file)
    for i in freqlist:
        count += i
    if count == 0:
        e = open(out_file, 'w')
        e.close()
        a = open(out_file[:len(out_file) - 4] + "_compressed.txt", 'w')
        a.close()
    else:
        header = create_header(freqlist)
        codes = create_code(create_huff_tree(freqlist))
        get = open(in_file, 'r')

        input = get.read()
        get.close()
        ret = ""
        for i in range(len(input)):
            key = input[i]
            code_index = ord(key)
            rep_value = codes[code_index]
            ret += rep_value

        head = "{0}\n".format(header)
        output = open(out_file, 'w')
        output.write(head)
        output.write(ret)
        output.close()
        comp_name = out_file[:len(out_file) - 4] + "_compressed.txt"
        rowling = HuffmanBitWriter(comp_name)
        rowling.write_str(head)
        rowling.write_code(ret)
        rowling.close()

def huffman_decode(encoded_file, decoded_file):
    if not os.path.exists(encoded_file):
        raise FileNotFoundError
    ret = open(decoded_file, "w")
    codes = ''
    reader = HuffmanBitReader(encoded_file)
    list_of_freqs = reader.read_str()
    if len(list_of_freqs) == 0:
        ret.close()
        reader.close()
        return
    freq_list = parse_string(list_of_freqs)
    root = create_huff_tree(freq_list)

    try:
        while True:
            if reader.read_bit():
                codes += '1'
            else:
                codes += '0'
    except:
        chars = ''

    node = root
    for i in codes:
        if not node.left and not node.right:
            chars += chr(node.char)
            node = root  # reset tree back to root
        if (i == '0'):
            node = node.left
        else:
            node = node.right

    #ret.write("{0}".format(list_of_freqs))
    ret.write(chars)
    ret.close()
    reader.close()

def parse_string(header_string):
    ret = [0] * 256
    l = header_string.split()
    times = len(l)
    for i in range(0, times, 2):
        ascii_loc = int(l[i])
        freq = int(l[i + 1])
        ret[ascii_loc] = freq
    return ret

huffman_decode("test_out_compressed.txt", "output.txt")

huffman_encode("test.txt", "test_out.txt")