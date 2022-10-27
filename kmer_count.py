#!/usr/bin/env python3

#import os module to get files, import sys module to manipulate arguments  
import os, sys, re

#usage message 
Usage = """
kmer_count_sort.py - version 1.0
Reads in each file in fasta format, and output the sorted kmer count infor from each file 

The output file is formatted 
kmer1, count1, 
kmer2, count2,
...

Usage:
	kmer_count_sort.py folder_name kmer_size
"""

#check command, convert command line arguments to variables
if len(sys.argv) < 3:
	print(Usage)
else:
	folder = sys.argv[1]
	kmer_size = int(sys.argv[2])

#make os.listdir only list non-hidden file
if os.name == 'nt':
    import win32api, win32con
def file_is_hidden(p):
    if os.name== 'nt':
        attribute = win32api.GetFileAttributes(p)
        return attribute & (win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM)
    else:
        return p.startswith('.') 

#function to convert the name of files in the folder into a list
def read_folder(path):
	file_list = []
	for file_name in os.listdir(path):
		if not file_is_hidden(file_name):
			file_list.append(file_name)
	return(file_list)

#function to read fasta file, only take sequence part, remove line break, join together
def read_fasta(file):
	Infile = open(file, 'r')
	Sequences = ''
	for Line in Infile:
		if Line[0] != ">":
			Line = Line.rstrip("\n")
			Sequences += Line
	return(Sequences)

#function to list all kmer in a given kmer size
def kmer_iden(sequence, kmer_size):
	kmers = []
	for start in range(0, len(sequence) - (kmer_size -1), 1):
		kmer = sequence[start:start+kmer_size]
		kmers.append(kmer)
	return(kmers)

#function to count the kmer into a dictionary, sort the value of count, convert as a list
def count_kmer(kmers):
	kmer_count = {}
	for kmer in kmers:
		current_count = kmer_count.get(kmer, 0)
		new_count = current_count + 1
		kmer_count[kmer] = new_count
	sorted_kmer_count = sorted(kmer_count.items(), key=lambda x:x[1], reverse=True)
	return(sorted_kmer_count)


#use above function, get the files, read files, count kmer, sort kmer count, write the result in the result file
for file in read_folder(folder):
	file_name = file
	output = open(file_name.replace("fasta", "_result.txt"), "w")
	sequence = read_fasta(folder + file_name)
	if re.search(r"[^ATGC]", sequence):
		output.write("Warning:" + file + " has non ATGC nucleotide" + "\n")
	if kmer_size > len(sequence):
		print("For file", file_name)
		print("Kmer value is larger than the sequence length")
	elif kmer_size <= 0:
		print("Kmer value is invalid")
	kmers_find = kmer_iden(sequence, kmer_size)
	kmers_sorted_list = count_kmer(kmers_find)
	for kmer in kmers_sorted_list:
		for row in kmer:
			output.write(str(row) + ',')
		output.write('\n')
	output.close()
	
	
