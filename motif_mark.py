#!/usr/bin/env python

import cairo
import argparse
import re

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
sequences = []

class BindingMotif:

    def __init__(self, sequence):
        '''A motif that binds an expression protein'''
        ## Data ##
        self.sequence = sequence
    ## Methods ##
    def find(self, line):
        search_term = self.sequence
        search_term = search_term.upper()
        search_term = search_term.replace("Y","[CT]")
        line = line.upper()
        matches = [(match.start(),match.end()) for match in re.finditer(search_term, line)]
        return(matches)

class Sequence:
    def __init__(self, sequence, header, size):
        '''a sequence containing introns exons and motifs'''
        ## Data ##
        self.sequence = sequence
        self.header = header
        self.size = size
        ## Methods ##
    def find(self):
        exon = [(match.start(),match.end()) for match in re.finditer("[ATGCN]+",self.sequence)]
        return(exon[0])






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

pic_width = 0

with open (f1, "r") as fin, open (o,"w") as oout:
    while True:                                                
        line = fin.readline().strip()
        if line == "":
            break
        seq = fin.readline().strip()
        line = Sequence(seq,line,len(seq))
        sequences.append(line)
        if line.size > pic_width:
            pic_width = line.size


pic_width = pic_width + 50

plots = {}


for seq in sequences:
    plots[seq.header] = []
    for mot in motifs:
        plots[seq.header].append((mot.sequence,mot.find(seq.sequence)))

# for m in motifs:
#     print (m.sequence)


#for seqs in plots:
#    print (seqs,plots[seqs])

pic_hight = (len(sequences) * 60) + (len(motifs)*25)
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, pic_width, pic_hight)

ctx = cairo.Context(surface)

ctx.rectangle(0,0, pic_width, pic_hight)
ctx.set_source_rgb(1,1,1)
ctx.fill()

for n,sequence in enumerate(sequences, 1):
    ctx.set_source_rgb(0,0,0)
    ctx.move_to(10,(50*n)-10)
    ctx.show_text(sequence.header)
    ctx.rectangle(10, 50 * n, sequence.size, 3)
    ctx.rectangle(10 + sequence.find()[0], (50 * n) - 3, sequence.find()[1]-sequence.find()[0], 10)
    ctx.fill()
    x = 0
    for motifs in plots[sequence.header]:
        for motif in motifs:
            if motif != [] and type(motif[0]) == str:
                x+=1
            if motif != [] and type(motif[0]) ==tuple:
                for instance in motif:
                    if x ==1:
                        ctx.set_source_rgb(1,0,1) #purple ygcy
                    elif x ==2:
                        ctx.set_source_rgb(0,0,1)
                    elif x ==3:
                        ctx.set_source_rgb(0,1,0) #green catag
                    elif x ==4:
                        ctx.set_source_rgb(0,1,1) #cyan YYYYYY
                    elif x ==5:
                        ctx.set_source_rgb(1,.5,0)
                    ctx.rectangle(10 + instance[0],(50 * n) - x, instance[1] - instance[0], 10)
                    ctx.stroke()
    ctx.stroke()
  
ctx.set_source_rgb(0,0,0)
g = 0
for g, motif in enumerate(motifs):
    ctx.move_to(10,(len(sequences) * 60) + (g * 15))
    if g == 0:
        ctx.show_text("Key")
    ctx.show_text(motif)

# ctx.rectangle(10,10, 200, 30)
# ctx.stroke()

surface.write_to_png(o)

# for plot in plots:
#     print(plot)
#     print (len(plots[plot]))
#     for item in plots[plot]:
#         print(item[0])
#         print(len(item[1]))