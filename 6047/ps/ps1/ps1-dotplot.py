#!/usr/bin/env python

####
# 6.047/6.878 - Problem Set 1 - string hashing/dotplots
#
# INSTRUCTIONS FOR USE:
# call program as follows:
#  ./ps1-dotplot.py <FASTA 1> <FASTA 2> <PLOTFILE>
#     e.g. ./ps1-dotplot.py human-hoxa-region.fa mouse-hoxa-region.fa dotplot.jpg
#
# Make sure the ps1-dotplot.py is marked as executable:
#     chmod +x ps1-dotplot.py
# or in windows with:
#     python ps1-dotplot.py human-hoxa-region.fa mouse-hoxa-region.fa dotplot.jpg
# once you have put python in your path
#
#
# GNUPLOT
# Gnuplot is used to generate plots for this program.  It is a common plotting
# program installed on most unix systems.  To use gnuplot on athena do the
# following:
#
# athena% add gnu
#
# To test that it works do this:
#
# athena% gnuplot
# gnuplot> plot cos(x)
#
# you should then see a cosine plot appear.
#
# Note: plotting.py and util.py must be in the same directory as this script.
# These files contain the code for generating plots.  You should not
# worry about understanding any of the code contained within these files.
# Much of it is copied from another project and is unrelated.
#

import sys, random
import plotting
import string

def readSeq(filename):
    """reads in a FASTA sequence"""

    stream = open(filename)
    seq = []

    for line in stream:
        if line.startswith(">"):
            continue
        seq.append(line.rstrip())

    return "".join(seq)

def quality(hits):
    """determines the quality of a list of hits"""

    slope1 = 1.0e6 / (825000 - 48000)
    slope2 = 1.0e6 / (914000 - 141000)
    offset1 = 0 - slope1*48000
    offset2 = 0 - slope2*141000

    goodhits = []

    for hit in hits:
        upper = slope1 * hit[0] + offset1
        lower = slope2 * hit[0] + offset2

        if lower < hit[1] < upper:
            goodhits.append(hit)

    return goodhits

def makeDotplot(filename, hits):
    """generate a dotplot from a list of hits
       filename may end in the following file extensions:
         *.ps, *.png, *.jpg
    """
    x, y = zip(* hits)

    slope1 = 1.0e6 / (825000 - 48000)
    slope2 = 1.0e6 / (914000 - 141000)
    offset1 = 0 - slope1*48000
    offset2 = 0 - slope2*141000

    hits2 = quality(hits)
    print "%.5f%% hits on diagonal" % (100 * len(hits2) / float(len(hits)))

    # create plot
    p = plotting.Gnuplot()
    p.enableOutput(False)
    p.plot(x, y, xlab="sequence 2", ylab="sequence 1")
    p.plotfunc(lambda x: slope1 * x + offset1, 0, 1e6, 1e5)
    p.plotfunc(lambda x: slope2 * x + offset2, 0, 1e6, 1e5)

    # set plot labels
    p.set(xmin=0, xmax=1e6, ymin=0, ymax=1e6)
    p.set(main="dotplot (%d hits, %.5f%% hits on diagonal)" %
          (len(hits), 100 * len(hits2) / float(len(hits))))
    p.enableOutput(True)

    # output plot
    p.save(filename)

    return p

def invert(s):
    translate = string.maketrans("ACGT", "TGCA")
    return s.translate(translate)[::-1]

def main():

    # NOTE to WINDOWS users:
    #   If you do not want to use the command line, comment out the command line
    #   parsing code and hard-code the input filenames.
    #
    # For example, use the following:
    # file1 = "human-hoxa-region.fa"
    # file2 = "mouse-hoxa-region.fa"
    # plotfile = "dotplot.jpg"

    # parse command-line arguments
    if len(sys.argv) < 4:
        print "you must call program as:  "
        print "   python ps1-dotplot.py <FASTA 1> <FASTA 2> <PLOT FILE>"
        print "   PLOT FILE may be *.ps, *.png, *.jpg"
        sys.exit(1)
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    plotfile = sys.argv[3]

    # read sequences
    print "reading sequences"
    seq1 = readSeq(file1)
    seq2 = readSeq(file2)

    # Length and skip of hash key

    # B0. Exact 30-mers
    # kmerlen = 30
    # kmerskip = 1

    # Bi. Exact 100-mers
    # kmerlen = 100
    # kmerskip = 1

    # Bii. 60-mers, every other base
    # kmerlen = 60
    # kmerskip = 2

    # Biii. 90-mers, every third base
    # kmerlen = 90
    # kmerskip = 3

    # Biv. 120-mers, every fourth base
    # kmerlen = 120
    # kmerskip = 4
    
    # Bv. 100-mers, at most 2 per 6 mismatch
    # kmerlen = 100
    # kmerskip = 6

    # E. 200-mers, finding inversions
    kmerlen = 200
    kmerskip = 1

    # hash table for finding hits
    lookup = {}

    # store sequence hashes in hash table
    print "hashing seq1..."
    for i in xrange(0, len(seq1) - kmerlen + 1):
        key = seq1[i:i + kmerlen]
        key = key[::kmerskip]
        lookup.setdefault(key, []).append(i)


    # look up hashes in hash table
    print "hashing seq2..."
    hits = []
    chain = []
    # for i in xrange(0, len(seq2) - kmerlen + 1):
    for i in xrange(len(seq2) - 1, -1, -1):
        key = seq2[i:i + kmerlen]
        key = key[::kmerskip]
        key = invert(key)

        # store hits to hits list
        any_hits = lookup.get(key, [])
        if len(any_hits) != 0:
            chain.append(i)
            if len(chain) > 50:
                print(max(chain))
                quit()
        else:
            chain = []

        for hit in any_hits:
            hits.append((i, hit))


    # hits should be a list of tuples
    # [(index1_in_seq2, index1_in_seq1),
    #  (index2_in_seq2, index2_in_seq1),
    #  ...]

    print "%d hits found" % len(hits)
    print "making plot..."
    p = makeDotplot(plotfile, hits)

main()