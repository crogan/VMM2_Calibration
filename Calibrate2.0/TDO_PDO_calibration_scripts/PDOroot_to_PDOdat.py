from __future__ import division

import os
import re
from tqdm import *
import sys
import itertools
from time import time, sleep
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
import pickle
from rootpy.io import root_open
from rootpy import asrootpy
import argparse

class Event:
    def __init__(self, TDO, PDO, BCID, Delay, TPDAC):
        self.TDO = TDO
        self.PDO = PDO
        self.BCID = BCID
        self.Delay = Delay
        self.TPDAC = TPDAC
    def __repr__(self):
        return str(self.TDO)

parser = argparse.ArgumentParser()
parser.add_argument("root_in", help="root file to be converted to dat")

args = parser.parse_args()

assert(args.root_in[-5:] == '.root'), "input should be a .root file"

file_output = args.root_in[:-5] + '.dat'

n_vmms = 8
n_channels = 64
locs_to_check = list(itertools.product(range(n_vmms), range(1, n_channels+1)))

#this is purely to determine the board number
with root_open(args.root_in) as f:
    vm = f.PDO_calib
    for event in vm:
        board_num = event.MMFE8

#now we write the file by making a dictionary of the events, then writing
#each channel's info in sorted order
with open(file_output, 'w') as writer:
    writer.write('MMFE8 VMM CH  Gain      Pedestal  (PDO = Q*G + P)\n')

    file_to_convert = args.root_in
    info_dict = {(board_num, i_vmm, i_channel): {'Gain':-999, 'Pedestal': -999} for  i_vmm,i_channel in locs_to_check}

    with root_open(file_to_convert) as f:
        vm = f.PDO_calib
        for event in vm:
            info_dict[board_num, event.VMM, event.CH] = {'Gain': (event.A2*event.d21)/.5, 'Pedestal': (-2*event.t02-event.d21)*event.A2*event.d21+event.c0}

    for i_vmm,i_channel in locs_to_check:
        writer.write(str(board_num).ljust(6) + str(i_vmm).ljust(4) + str(i_channel).ljust(4) + "%.2e"%info_dict[board_num, i_vmm, i_channel]['Gain'] + '  ' + "%.2e"%info_dict[board_num, i_vmm, i_channel]['Pedestal'] + '  ' + '\n')

writer.close()




