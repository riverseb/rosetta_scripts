import os 
import sys

def create_set_from_files(file1, file2):
    list1 = []
    list2 = []
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        for line in f1:
            list1 += line.strip().split()
        for line in f2:
            list2 += line.strip().split()
    #print(list1, list2)       
    return list1, list2

def compare_bits(list1, list2):
    """
    This function takes two lists of binary strings, compares the binary strings 
    at equivalent positions, and counts how many bits are in common over the whole list.
    """
    assert len(list1) == len(list2), "Lists must be the same length"
    
    common_bits = 0
    numBits1 = 0
    numBits2 = 0
    for bin_str1, bin_str2 in zip(list1, list2):
        for bit1, bit2 in zip(bin_str1, bin_str2):
            if bit1 == bit2 and bit1 != '0':
                common_bits += 1
            if bit1 != '0':
                numBits1 += 1
            if bit2 != '0':
                numBits2 += 1
    print(common_bits, numBits1, numBits2)
    
    if numBits1 > numBits2:
        return common_bits / numBits2
    else:
        return common_bits / numBits1
                
   # return common_bits
def main(file1, file2):
    list1, list2 = create_set_from_files(file1, file2)
    sim_score = compare_bits(list1, list2)
    print(sim_score)

if __name__ == '__main__':
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    main(file1, file2)
