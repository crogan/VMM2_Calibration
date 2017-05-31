"""
Check channel differences between calibration files

Run like:
> python lost_channels.py -o old.root -n new.root 

"""

import argparse
import os, sys, ROOT

thr = 30

def main():

    ops = options()
    if not ops.o or not ops.n:
        fatal("Please provide two calibration ROOT files to compare")
    if not os.path.isfile(ops.o):
        fatal("The -o file does not exist")
    if not os.path.isfile(ops.n):
        fatal("The -n file does not exist")

    f1 = ROOT.TFile(ops.o)
    f2 = ROOT.TFile(ops.n)
    tr1 = f1.Get("VMM_data")
    tr2 = f2.Get("VMM_data")

    if not tr1 or not tr2:
        fatal("Files don't have VMM_data")

    ents1 = tr1.GetEntries()
    ents2 = tr2.GetEntries()

    print
    print "ROOT file 1 : %s" %(ops.o)
    print "ROOT file 2 : %s" %(ops.n)
    print

    hits1 = {}
    hits2 = {}
    for e in xrange(ents1):
        _ = tr1.GetEntry(e)
        mmfe, vmm, chw, chp = (tr1.MMFE8, tr1.VMM, tr1.CHword, tr1.CHpulse)
        if (mmfe, vmm, chw) in hits1:
            hits1[mmfe, vmm, chw] += 1
        else:
            hits1[mmfe, vmm, chw] = 1
    for e in xrange(ents2):
        _ = tr2.GetEntry(e)
        mmfe, vmm, chw, chp = (tr2.MMFE8, tr2.VMM, tr2.CHword, tr2.CHpulse)
        if (mmfe, vmm, chw) in hits2:
            hits2[mmfe, vmm, chw] += 1
        else:
            hits2[mmfe, vmm, chw] = 1

    active1 = [key for key in hits1 if hits1[key] > thr]

    og_ch = dict(enumerate([0]*8)) #original number of channels
    board = -1
    for (mmfe, vmm, chw) in hits1:
        board = mmfe
        og_ch[vmm] += 1
    
    active2 = [key for key in hits2 if hits2[key] > thr]

    diffs = list(set(active1).difference(set(active2)))

    channels = {0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[]}
    
    for (mmfe, vmm, chw) in sorted(diffs):
        channels[vmm].append(chw)
    if (ops.c):
        print color.blue + "BOARD %i" %(board) + color.end
    else:
        print "BOARD %i" %(board)
    print
    for vmm in channels:
        if (ops.c):
            print color.pink + "%i" %(vmm) + color.end + color.gray +  " (%i)" %(og_ch[vmm]) + color.end +" : %s" %(channels[vmm])
        else:
            print "%i" %(vmm) + " (%i)" %(og_ch[vmm]) + " : %s" %(channels[vmm])
    print 

class color:
    
    pink = "\033[38;5;205m"
    blue = "\033[38;5;27m"
    gray = "\033[90m"
    green = "\033[92m"
    end = "\033[0m"
    warning = "\033[38;5;227;48;5;232m"

def options():
    parser = argparse.ArgumentParser(usage=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-o", default=None, help= "Old calibration ROOT file")
    parser.add_argument("-n", default=None, help= "New calibration ROOT file")
    parser.add_argument("-c", default=False, action="store_true", help= "colors")
    return parser.parse_args()

def fatal(msg):
    sys.exit("Error in %s: %s" % (__file__, msg))

if __name__ == "__main__":
    main()
