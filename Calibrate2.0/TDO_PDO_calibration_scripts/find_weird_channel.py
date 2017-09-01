"""This script is intended to be used within an ipython script.
That way, the TDO dictionary (.p file) only has to be loaded once. If you
don't have the TDO caibration data in a .p, run Fit_TDO.py on your 
TDO data. In the current setup, we search through the calibration data for 
channels with unusually high standard error (sigma). Riffle through these plots
by pressing Enter.

EX:
    python plot_TDO.py TDOApr22_17/TDO_calib_106

-Jonah
"""
%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import *
import tensorflow as tf
from collections import Counter, defaultdict
from copy import deepcopy
import sys
import pickle
import itertools
from time import time
from scipy import stats
import os
import argparse
from scipy import stats

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
parser.add_argument("TDO_info_name", help="The name of the files you would like to extract plots from. TDO_info_name.p and TDO_info_name.dat must both exist")

args = parser.parse_args()

print 'loading dictionary...'
TDO_dict = pickle.load( open(args.TDO_info_name + '.p', "rb" ) )
print 'done loading'

#############################################

#data params
n_vmms = 8
n_channels = 64
lower_ignore = 10
top_ignore = 200
min_num_data_points = 10

locs_to_check = list(itertools.product(range(n_vmms), range(1, n_channels+1)))


#this loop figures out the board number
with open(args.TDO_info_name + '.dat', 'r') as reader:
    reader.readline()
    board_num = int(reader.readline()[:3])

for i_vmm, i_channel in locs_to_check:
    isghost = False
    with open(args.TDO_info_name + '.dat', 'r') as reader:
        compare = str(board_num).ljust(6) + str(i_vmm).ljust(4) + str(i_channel).ljust(4)
        reader.readline()
        for line in reader:
            if line[:14] == compare:
                if line[14:19] == 'GHOST':
                    isghost = True
                    break
                keys = ['MMFE8', 'VMM', 'CH', 'Gain', 'Pedestal', 'm', 'b', 'floor', 'n_samps', 'p_8', 'sigma', 'chi2', 'prob', 'delta_b', 'delta_m', 'delta_f']
                vals = [float(va) for va in line.split(' ') if (va != '' and va != '\n')]
                info_dict = {keys[i]: vals[i] for i in range(len(keys))}
                break
    if isghost:
        print 'skipping ghost ', i_vmm, i_channel
        continue
    if info_dict['sigma'] > 3:
        bot = info_dict['floor']
        top = info_dict['floor'] - 5*info_dict['m']
        curr_W = info_dict['m']
        curr_b = info_dict['b']

        #1) Get train_data (if there is any for this channel)
        data_without_crazy_TDO = [event for event in TDO_dict[i_vmm, i_channel] if lower_ignore < event.TDO < top_ignore]

        if len(data_without_crazy_TDO) > min_num_data_points:

            TPDAC_select = max([event.TPDAC for event in data_without_crazy_TDO])
            train_data = np.array([[event.Delay, event.TDO] for event in data_without_crazy_TDO if event.TPDAC == TPDAC_select])


            #6) Plot the data!  
            fig = plt.figure(figsize=(10,6))      
            sns.set_style("whitegrid", {'axes.grid' : False})
            plt.plot((-.1,4.1), (bot, bot), 'k--', alpha=.3)
            plt.plot((-.1,4.1), (top, top), 'k--', alpha=.3)
            plt.hist2d(train_data[:,0], train_data[:,1], bins=[np.arange(-.1,4.2,.2), np.arange(10, 120)], cmap='Greys')
            plt.colorbar()

            x_show = np.linspace(-.1,4.1,400)
            y_show = [curr_W*x_s+curr_b for x_s in x_show]
            for i,y_s in enumerate(y_show):
                if y_show[i]>top:
                    y_show[i] += 5*curr_W
                if y_show[i]<bot:
                    y_show[i] -= 5*curr_W
            plt.plot(x_show, y_show, 'k', alpha=1, linewidth=1)
            #plt.errorbar(x_show, y_show, yerr=[info_dict['sigma'] for da in x_show], ecolor='y', fmt=None, alpha=.1)
            plt.fill_between(x_show, np.array(y_show) - info_dict['sigma'], np.array(y_show) + info_dict['sigma'], alpha=.2, color='#fff200')
            #get parameters ready for printing
            m_convert = (top-bot)/25.
            p_convert = m_convert*(-25/2.) + bot


            #add plot styling
            plt.xlabel('Delay (5 ns)')
            plt.ylabel('TDO (counts)')
            plt.annotate('{0: <8}'.format('m: ') + str(info_dict['m']) + r' $\pm$ ' + str(info_dict['delta_m'])[:5], xy=(1.17,.8), xycoords='axes fraction')
            plt.annotate('{0: <8}'.format('b: ') + str(info_dict['b']) + r' $\pm$ ' + str(info_dict['delta_b'])[:5], xy=(1.17,.7), xycoords='axes fraction')
            plt.annotate('{0: <8}'.format('f: ') + str(info_dict['floor'])+ r' $\pm$ ' + str(info_dict['delta_f']/85.)[:5], xy=(1.17,.6), xycoords='axes fraction')
            plt.annotate('{0: <8}'.format('N: ') + str(int(info_dict['n_samps'])), xy=(1.17,.5), xycoords='axes fraction')
            plt.annotate('{0: <8}'.format('p8: ') + str(info_dict['p_8']*100) + '%', xy=(1.17,.4), xycoords='axes fraction')
            plt.annotate('{0: <8}'.format('$\sigma$: ') + str(info_dict['sigma']), xy=(1.17,.3), xycoords='axes fraction')
            #plt.annotate('{0: <3}'.format('_f: ') + nice_params['delta_f'], xy=(1.20,.5), xycoords='axes fraction')
            plt.title(str(board_num) + '_' + str(i_vmm) + '_' + str(i_channel))
            plt.draw()

            #plt.savefig(str(args.board_num) + '_' + str(i_vmm) + '_' + str(i_channel) + '.png')
            # plt.close(fig)
            plt.pause(.1)
            raw_input('')
            plt.close(fig)

        else:
            print 'That channel is a ghost.'
    



