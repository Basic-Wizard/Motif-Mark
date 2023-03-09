#!/usr/bin/env python

import cairo
import argparse
import re

def get_args():
    parser = argparse.ArgumentParser(description="draw a rectangle")
    #parser.add_argument("-o", help="output file name", type=str, default="output.png")
    parser.add_argument("-f", help="input FASTA file", type=str, required=True)
    parser.add_argument("-m", help="input motif file", type=str, required=True)
    return parser.parse_args()


parameters = get_args()
#o = parameters.o
f = parameters.f
m = parameters.m

motifs = []
sequences = []

prefix = (f.split(".")[0])

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
        search_term = search_term.replace("U","T")
        search_term = search_term.replace("R","[AG]")
        search_term = search_term.replace("M","[AC]")
        search_term = search_term.replace("K","[GT]")
        search_term = search_term.replace("S","[CG]")
        search_term = search_term.replace("W","[AT]")
        search_term = search_term.replace("H","[ACT]")
        search_term = search_term.replace("B","[CGT]")
        search_term = search_term.replace("V","[ACG]")
        search_term = search_term.replace("D","[AGT]")
        search_term = search_term.replace("N","[ACTG]")
        line = line.upper()
        matches = [(match.start(),match.end()) for match in re.finditer(search_term, line)]
        return(matches)

#this class will hold all the motif objects

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

#this class will hold the sequence options


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
                    print (line, end = "", file = fo)

#this is the function that makes sure the input fasta is rewritten to have the sequence all be on one line of the file

with open (m, "r") as min:
     while True:                                                
        line = min.readline().strip()
        if line == "":
            break
        seq = line
        line = BindingMotif(seq)
        motifs.append(line)

#this code reads through the file with the motifs in it to fill the motif class

p_motifs = [] 
for motif in motifs:
    p_motifs.append(motif.sequence)
#for some unknown reason after the list of motif objects breaks in the later code so I am saving another list containing the motifs

f1 = "oneline.fasta"
oneline_fasta(f,f1)
#this will run the code to make the fasta file have the sequence in one line

pic_width = 0
#sets the picture width as zero so it can be set to 0 so it can be compared to length of sequences and be set to have room for whatever sequence is needed

with open (f1, "r") as fin:
    while True:                                                
        line = fin.readline().strip()
        #holds the header of the FASTA file
        if line == "":
            break
        seq = fin.readline().strip()
        #holds the sequence
        line = Sequence(seq,line,len(seq))
        #sets the sequence object to be saved as the header while holding the rest of the variables inside
        sequences.append(line)
        if line.size > pic_width:
            pic_width = line.size

pic_width = pic_width + 25
#adds a margin to the picture

plots = {}
#makes a dictionary to hold all the information to generate the image

for seq in sequences:
    plots[seq.header] = []
    for mot in motifs:
        plots[seq.header].append((mot.sequence,mot.find(seq.sequence)))
#makes fills the disctionary with the information in my lists of sequence and motif objects

pic_hight = (len(sequences) * 60) + (len(motifs)*25)
#sets the height of the image based on the number of sequences

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
    #makes the intron and exon rectangles based in the info saved in the sequence objects
    x = 0
    for motifs in plots[sequence.header]:
        for motif in motifs:
            if motif != [] and type(motif[0]) == str:
                x+=1
            #itterates at the switch between motifs
            if motif != [] and type(motif[0]) ==tuple:
                #grabs the tuple that holds the list of instances
                for instance in motif:
                    if x ==1:
                        ctx.set_source_rgb(1,0,1) #purple ygcy
                    elif x ==2:
                        ctx.set_source_rgb(0,0,1) #blue GCAUG
                    elif x ==3:
                        ctx.set_source_rgb(0,1,0) #green catag
                    elif x ==4:
                        ctx.set_source_rgb(0,1,1) #cyan YYYYYY
                    elif x ==5:
                        ctx.set_source_rgb(1,.5,0)
                    #sets the color of the rectangle based on the motif
                    ctx.rectangle(10 + instance[0],(50 * n) - x, instance[1] - instance[0], 10)
                    ctx.stroke()
                    #draws the box with each motif at a different height to show overlap
    ctx.stroke()


ctx.set_source_rgb(0,0,0)

ctx.move_to(200,(len(sequences) * 60) + 15)
ctx.show_text("intron")
ctx.move_to(200,(len(sequences) * 60) + 35)
ctx.show_text("exon")
ctx.rectangle(240,(len(sequences) * 60) + 10,15,3)
ctx.rectangle(240,(len(sequences) * 60) + 27,15,10)
ctx.fill()
#makes the intron and exon key


#code below makes the key for the motifs
ctx.move_to(10,len(sequences) * 60)
ctx.show_text("Key:")

x = 1
for motif in p_motifs:
    if x ==1:
        ctx.set_source_rgb(1,0,1) #purple ygcy
    elif x ==2:
        ctx.set_source_rgb(0,0,1) #blue GCAUG
    elif x ==3:
        ctx.set_source_rgb(0,1,0) #green catag
    elif x ==4:
        ctx.set_source_rgb(0,1,1) #cyan YYYYYY
    elif x ==5:
        ctx.set_source_rgb(1,.5,0)
    ctx.move_to(10,(len(sequences) * 60) + (x * 15))
    ctx.show_text(p_motifs[x-1])
    x+=1


surface.write_to_png(prefix + ".png")
