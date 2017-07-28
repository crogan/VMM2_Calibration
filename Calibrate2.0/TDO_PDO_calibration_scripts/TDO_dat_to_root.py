""" The purpose of this script is to convert the .dat file produced
by Calibrate_TDO.py into a .root file for ease of analysis and compatibility
with older calibration codes. Variable definitions are identical to those found in 
Calibrate_TDO.py. The script will output a .root file with the same name as the input.
Channels with no data are not included in the .root file.

EX:
        python TDO_dat_to_root.py TDO_output.dat

-Jonah
"""

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("dat_in", help="dat file to be converted to root")

args = parser.parse_args()

assert(args.dat_in.endswith('.dat'))



from rootpy.tree import Tree
from rootpy.io import root_open
from rootpy.plotting import Hist2D

f = root_open(args.dat_in[:-4] + '.root', "recreate")

tree = Tree("TDO_calib")
tree.create_branches(
    {'MMFE8': 'D',
    'VMM': 'D',
    'CH': 'D',
    'C': 'D',
    'S': 'D',
    'chi2': 'D',
    'prob': 'D',
    'm': 'D',
    'b': 'D',
    'floor': 'D',
    'n_samps': 'D',
    'p_8': 'D',
    'sigma': 'D',
    'delta_b': 'D',
    'delta_m': 'D',
    'delta_f': 'D'})

with open(args.dat_in, 'r') as reader:
    reader.readline()
    for line in reader:
        vals = [sub_val for sub_val in line.split(' ') if sub_val != '']
        if vals[-1] != 'GHOST\n':
            tree.MMFE8 = float(int(vals[0]))
            tree.VMM = float(int(vals[1]))
            tree.CH = float(int(vals[2]))
            tree.C = float(vals[4])
            tree.S = float(vals[3])
            tree.chi2 = float(vals[11])
            tree.prob = float(vals[12])
            tree.m = float(vals[5])
            tree.b = float(vals[6])
            tree.floor = float(vals[7])
            tree.n_samps = float(vals[8])
            tree.p_8 = float(vals[9])
            tree.sigma = float(vals[10])
            tree.delta_b = float(vals[13])
            tree.delta_m = float(vals[14])
            tree.delta_f = float(vals[15])

            tree.fill()
tree.write()


f.close()
