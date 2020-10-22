import unittest
import filecmp
import subprocess
from ordered_list import *
from huffman import *


class TestList(unittest.TestCase):
    def test_02_textfile(self):
        huffman_encode("declaration.txt", "declaration_out.txt")
        # capture errors by running 'diff' on your encoded file with a *known* solution file
        err = subprocess.call("diff -wb declaration_out.txt declaration_soln.txt", shell = True)
        self.assertEqual(err, 0)
        err = subprocess.call("diff -wb declaration_out_compressed.txt declaration_compressed_soln.txt", shell = True)
        self.assertEqual(err, 0)

    def test_dne(self):
        with self.assertRaises(FileNotFoundError):
            huffman_encode("doesnotexist.txt", "doesnt_matter.txt")


    def test_empty_textfile(self):
        huffman_encode("empty_file.txt", "empty_out.txt")
        # capture errors by running 'diff' on your encoded file with a *known* solution file
        err = subprocess.call("diff -wb empty_out.txt empty_file.txt", shell = True)
        self.assertEqual(err, 0)
        err = subprocess.call("diff -wb empty_out_compressed.txt empty_file.txt", shell = True)
        self.assertEqual(err, 0)


if __name__ == '__main__': 
   unittest.main()
