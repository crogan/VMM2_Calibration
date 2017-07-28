"""The purpose of this script is to convert the data into a dictionary (TDO_dict)
which will be fed to a tensorflow graph in Calibrate_TDO.py

EX:
        python Fit_TDO.py TDO_input.root TDO_dict.p


-Jonah
"""

import itertools
from time import time, sleep
import pickle
import argparse
from rootpy.io import root_open
from rootpy import asrootpy

class Event:
    def __init__(self, TDO, PDO, BCID, Delay, TPDAC):
        self.TDO = TDO
        self.PDO = PDO
        self.BCID = BCID
        self.Delay = Delay
        self.TPDAC = TPDAC
        # self.CHword = CHword
        # self.CHpulse = CHpulse
    def __repr__(self):
        return str(self.TDO)

def categorize(event):
    global TDO_dict
    if event.CHword == event.CHpulse:
        TDO_dict[event.VMM, event.CHword].append(Event(event.TDO, event.PDO, event.BCID, event.Delay, event.TPDAC))

def get_TDO_data(file_name):
    global TDO_dict
    with root_open(file_name) as f:
        vm = f.VMM_data
        TDO_dict = {(i_vmm, i_channel): [] for i_vmm,i_channel in itertools.product(range(n_vmms), range(1, n_channels+1))}
        t0 = time()
        map(categorize, vm)
        t1 = time()
        print 'TIME: ', t1-t0
    return TDO_dict

parser = argparse.ArgumentParser()
parser.add_argument("TDO_input", help="the .root file to be calibrated", type=str)
parser.add_argument("TDO_output", help="the .p file to store the result", type=str)

args = parser.parse_args()

n_channels = 64
n_vmms = 8
n_delays = 5

TDO_dict = {}
TDO_dict = get_TDO_data(args.TDO_input)
pickle.dump( TDO_dict, open( args.TDO_output, "wb" ) )

with root_open(args.TDO_input) as f:
    vm = f.VMM_data
    for event in vm:
        ev = event
        break
    board_num = ev.MMFE8
pickle.dump( {'board_num': board_num}, open(args.TDO_output[:-2] + '_boardnum.p', "wb"))



     


