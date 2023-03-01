#!/usr/bin/env python

import cairo
import argparse

def get_args():
    parser = argparse.ArgumentParser(description="draw a rectangle")
    parser.add_argument("-o", help="output file name", type=str, default="output.png")
    parser.add_argument("-f", help="input FASTA file", type=str, required=True)
    parser.add_argument("-m", help="input motif file", type=str, required=True)
    return parser.parse_args()


parameters = get_args()
o = parameters.o
f = parameters.f
m = parameters.m

motifs = []

class BindingMotif:

    def __init__(self, sequence):
        '''A motif that binds a expression protein'''
        ## Data ##
        self.sequence = sequence
    ## Methods ##
    def count(self, line):
        counter = line.count(self.sequence)
        return(counter)


def oneline_fasta(f,o):
    '''docstring'''
    with open (o, "w") as fo:
        with open(f,"r") as fh:   #opens the file as fh
            for n,line in enumerate(fh):     #starts a for loop for each line in file f 
                line = line.strip('\n')
                if n == 0:
                    print (line, file = fo)
                elif n!=0 and line[0] == ">":
                    print (file = fo)
                    print (line, file = fo)
                else:
                    #seq
                    print (line, end = "", file = fo)

with open (m, "r") as min:
     while True:                                                
        line = min.readline().strip()
        if line == "":
            break
        seq = line
        line = BindingMotif(seq)
        motifs.append(line)
f1 = "oneline.fasta"

oneline_fasta(f,f1)

with open (f1, "r") as fin, open (o,"w") as oout:
    while True:                                                
        line = fin.readline().strip()
        if line == "":
            break
        for a in motifs:
            print (a.sequence)
            print(a.count(line))
# print (Binding_motif.ygcy)
# print (motifs)



# surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 250, 250)

# ctx = cairo.Context(surface)

# ctx.rectangle(10, 10, 20, 20)
# ctx.stroke()


# surface.write_to_png(o)
