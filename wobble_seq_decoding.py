#!/usr/bin/env python3

#import sys module to manipulate arguments , json to convert
import sys, json

#usage message 
Usage = """
wobble_seq_decoding.py - version 1.0
Reads in the file in fasta format, and output the wobble sequence and decoding seq in a 
JSON format

The output file is looks like: 
{
“ACTGACTGAC”: [“ACTGACTGRY”, “ACTGACTGRS”, “ACTGACTGWY”, “ACTGACTGWS”
] }

Usage:
	wobble_seq_decoding.py fasta_file
"""

#check command, convert command line arguments to variables
if len(sys.argv) < 2:
	print(Usage)
else:
	file = sys.argv[1]

#function to read fasta file, keep sequence name as key, sequence as value
def read_fasta(file):
	with open(file) as f:
		fa_dict = {}
		for line in f:
			line = line.rstrip("\n")
			if line[0] == ">":
				seq_name = line[1:]
				fa_dict[seq_name] = ''
			else:
				fa_dict[seq_name] += line.rstrip("\n")
	return(fa_dict)

#function to wobble decode the last second nucleotide
def sequence_decode_two(sequence):
	if "A" == sequence[-2:-1]:
		sequence1 = sequence[:-2] + sequence[-2:-1].replace("A","R") + sequence[-1]
		sequence2 = sequence[:-2] + sequence[-2:-1].replace("A","W") + sequence[-1]
	elif "C" == sequence[-2:-1]:
		sequence1 = sequence[:-2] + sequence[-2:-1].replace("C","Y") + sequence[-1]
		sequence2 = sequence[:-2] + sequence[-2:-1].replace("C","S") + sequence[-1]	
	elif "G" == sequence[-2:-1]:
		sequence1 = sequence[:-2] + sequence[-2:-1].replace("G","R") + sequence[-1]
		sequence2 = sequence[:-2] + sequence[-2:-1].replace("G","S") + sequence[-1]	
	elif "T" == sequence[-2:-1]:
		sequence1 = sequence[:-2] + sequence[-2:-1].replace("T","Y") + sequence[-1]
		sequence2 = sequence[:-2] + sequence[-2:-1].replace("T","W") + sequence[-1]
	return(sequence1, sequence2)		

#function to wobble decode the last nucleotide
def sequence_decode_last(sequence):
	if "A" == sequence[-1]:
		sequence1 = sequence[:-1] + sequence[-1].replace("A","R")
		sequence2 = sequence[:-1] + sequence[-1].replace("A","W")
	elif "C" == sequence[-1]:
		sequence1 = sequence[:-1] + sequence[-1].replace("C","Y")
		sequence2 = sequence[:-1] + sequence[-1].replace("C","S")	
	elif "G" == sequence[-1]:
		sequence1 = sequence[:-1] + sequence[-1].replace("G","R")
		sequence2 = sequence[:-1] + sequence[-1].replace("G","S")
	elif "T" == sequence[-1]:
		sequence1 = sequence[:-1] + sequence[-1].replace("T","W")
		sequence2 = sequence[:-1] + sequence[-1].replace("T","W")
	return(sequence1, sequence2)	
		

fasta_dic = read_fasta(file)
seq_wobble = {}
#iterate the fasta sequence, check N nucleotide and sequence length, then decode the seqeunce
#keep in the dictionary file, then convert to json file, output result.json
for name, seq in fasta_dic.items():
	if "N" in seq[-2:]:
		print(name, " has N in the wobble position.")
	elif len(seq) == 0:
		print(name, " Fasta record is empty.")
	else:
		seq_list = []
		for seq_sec in sequence_decode_two(seq):
			for seq_last in sequence_decode_last(seq_sec):
				seq_list.append(seq_last)
	seq_wobble[seq] = seq_list
with open("result.json", "w") as outfile:
    json.dump(seq_wobble, outfile)
	
