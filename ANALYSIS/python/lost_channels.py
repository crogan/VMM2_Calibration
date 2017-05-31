"""
Check channel differences between calibration files

Run like:
> python lost_channels.py -o old.root -n new.root 

"""

import argparse, time
import os, sys, ROOT

thr = [100,100]

def main():

    ops = options()
    if not ops.o or not ops.n:
        fatal("Please provide two calibration ROOT files to compare")
    if not os.path.isfile(ops.o):
        fatal("The -o file does not exist")
    if not os.path.isfile(ops.n):
        fatal("The -n file does not exist")

    dt = [1, 1] # data type default MM_data, 0 = calib, 2 = TPfit_data
        
    f = [ROOT.TFile(ops.o),ROOT.TFile(ops.n)]
    tr = [f[i].Get("VMM_data") or f[i].Get("MM_data") or f[i].Get("TPfit_data") for i in range(len(f))]

    if not all(itr for itr in tr):
        fatal("Files don't have VMM_data, MM_data, or TPfit_data")

    ents = [-1, -1]
    
    for i, itr in enumerate(tr):
        if "tp" in itr.GetName().lower():
            dt[i] = 2
        elif "vmm" in itr.GetName().lower():
            dt[i] = 0
            thr[i] = 10
        ents[i] = itr.GetEntries()
        
    print
    print "ROOT file 1 : %s" %(ops.o)
    print "ROOT file 2 : %s" %(ops.n)
    print

    hits = [{},{}]

    for i in range(len(hits)):
        if ops.prog:
            print 
            print "Processing file %i" %(i)
            print
        start_time = time.time()
        for e in xrange(ents[i]):
            if e % 1000 == 0 and e > 0 and ops.prog:
                pbftp(time.time() - start_time, e, ents[i])
            #if e > 200000 and dt[i] != 0:
            #    break
            _ = tr[i].GetEntry(e)
            if (dt[i] != 0):
                nhits = len(tr[i].tpfit_CH) if dt[i] == 2 else len(tr[i].mm_CH)
                for ih in xrange(nhits):
                    mmfe, vmm, ch = (tr[i].tpfit_MMFE8[ih], tr[i].tpfit_VMM[ih], tr[i].tpfit_CH[ih]) if dt[i] == 2 else \
                                    (tr[i].mm_MMFE8[ih], tr[i].mm_VMM[ih], tr[i].mm_CH[ih])
                    if (mmfe, vmm, ch) in hits[i]:
                        hits[i][mmfe, vmm, ch] += 1
                    else:
                        hits[i][mmfe, vmm, ch] = 1

            else:
                mmfe, vmm, chw, chp = (tr[i].MMFE8, tr[i].VMM, tr[i].CHword, tr[i].CHpulse)
                if (mmfe, vmm, chw) in hits[i]:
                    hits[i][mmfe, vmm, chw] += 1
                else:
                    hits[i][mmfe, vmm, chw] = 1
        print

    active = []
    for i in range(len(hits)): 
        act = [key for key in hits[i] if hits[i][key] > thr[i]]
        active.append(act)

    og_ch = {}
    boards = []
    for (mmfe, vmm, chw) in hits[0]:
        boards.append(mmfe)
        if (mmfe,vmm) in og_ch:
            og_ch[mmfe,vmm] += 1
        else:
            og_ch[mmfe,vmm] = 1

    ubds = sorted(list(set(boards)))
    diffs = list(set(active[0]).difference(set(active[1])))

    for ib in ubds:
        channels = {0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[]}
        for (mmfe, vmm, chw) in sorted(diffs):
            if mmfe != ib:
                continue
            channels[vmm].append(chw)
        print 
        if (ops.c):
            print color.blue + "BOARD %i" %(ib) + color.end
        else:
            print "BOARD %i" %(board)
        print
        for vmm in channels:
            if (ops.c):
                if (ib,vmm) in og_ch:
                    print color.pink + "%i" %(vmm) + color.end + color.gray +  " (%i)" %(og_ch[ib,vmm]) + color.end +" : %s" %(channels[vmm])
                else:
                    print color.pink + "%i" %(vmm) + color.end + color.gray +  " (XX)" + color.end +" : %s" %(channels[vmm])
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


def pbftp(time_diff, nprocessed, ntotal):
    nprocessed, ntotal = float(nprocessed), float(ntotal)
    rate = (nprocessed+1)/time_diff
    msg = "\r > %6i / %6i | %2i%% | %8.2fHz | %6.1fm elapsed | %6.1fm remaining"
    msg = msg % (nprocessed, ntotal, 100*nprocessed/ntotal, rate, time_diff/60, (ntotal-nprocessed)/(rate*60))
    sys.stdout.write(msg)
    sys.stdout.flush()

def options():
    parser = argparse.ArgumentParser(usage=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-o", default=None, help= "Old calibration ROOT file")
    parser.add_argument("-n", default=None, help= "New calibration ROOT file")
    parser.add_argument("-c", default=False, action="store_true", help= "colors")
    parser.add_argument("--prog", default=False, action="store_true", help= "progress bar")
    return parser.parse_args()

def fatal(msg):
    sys.exit("Error in %s: %s" % (__file__, msg))

if __name__ == "__main__":
    main()
