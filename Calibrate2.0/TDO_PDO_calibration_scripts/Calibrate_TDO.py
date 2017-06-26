""" The purpose of this script is to fit a sawtooth wave to the TDO data for each channel.
Currently, all data with the maximal available TPDAC is used in the calibration. The loss on
a given sawtooth wave is found as follows:

For a given slope m, y-intercept b, we generate all lines y = mx + b + k*(5*m) for all k natural numbers.
For each given data point (x,y), we define the error to be square(min((x,y) - (x,L_k(x))). In english, 
we find the closest line to our point, then take the squared difference to this point. This problem 
addresses the issue of pulses which crosses the edge of the BCID.

The output is a .dat file with the following parameters for every channel (see nice_params in the script for how these are calculated):
    
    MMFE8:    last three digits of the board's IP Address
    VMM:      VMM index, 0-indexed
    CH:       channel index, 1-indexed
    Gain:     TDO = time (ns) * Gain + Pedestal. Gain has units (TDO counts)/ns
    Pedestal: TDO = time (ns) * Gain + Pedestal. Pedestal has units (TDO counts)
    m:        slope of fitted fitted sawtooth wave. Has units (TDO counts)/(Delay index)
    b:        y-intercept of fitted sawtooth wave. Units: TDO counts
    floor:    the lower bound on TDO for this channel, AKA the TDO counts for 25/2 ns
    n_samps:  the number of data points that were fitted
    p_8:      the fraction of TDO on this channel which were a multiple of 8. 
              This variable should hopefully lead to a better understanding of
              the mysterious VMM Lower Bit Issue.
    sigma:    standard error for time prediction from this channel. Noisy channels
              will have high sigma.
    chi2:     sum of variance. Included to make crogan's TDO_to_time function work.
    prob:     probability of fit given above chi2. Not meaningful since we don't know
              the actual variance in our data.
    delta_b:  standard error on the calibration value found for b
    delta_m:  standard error on the calibration value found for m
    delta_f:  a value proportional to the standard error on the calibration value found for floor

Channels with no calibration data are labeled "GHOST"

EX:
    python Calibrate_TDO.py 101_TDOfit_calib.p 101_TDOoutput.dat 101

-Jonah
"""

from __future__ import division

import numpy as np
#import matplotlib.pyplot as plt
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
parser.add_argument("dictionary_file", help="the dictionary (ouput by Fit_TDO) which will be fit")
parser.add_argument("output_file", help="the name of the .dat file that the program will generate")
parser.add_argument("board_num", help="the name of the board that this dictionary corresponds to")
args = parser.parse_args()

#fit params
slope_initial_guess = -7.
learning_rate = .0005
loss_difference_lower_bound = .001
n_cycle_check = 100

#extra params
n_vmms = 8
n_channels = 64
num_bot_posses = 100
lower_ignore = 10
top_ignore = 200
min_num_data_points = 10


print 'loading ', args.board_num
TDO_dict = pickle.load( open(args.dictionary_file , "rb" ) )
print 'done'
locs_to_check = list(itertools.product(range(n_vmms), range(1, n_channels+1)))

writer = open(args.output_file, 'w')
writer.write('MMFE8 VMM CH  ' + 'Gain'.ljust(10) + 'Pedestal'.ljust(10) + 'm'.ljust(10) + 
                    'b'.ljust(10) + 'floor'.ljust(10) + 'n_samps'.ljust(10) + 'p_8'.ljust(10) + 
                    'sigma'.ljust(10) + 'chi2'.ljust(10) + 'prob'.ljust(10) + 'delta_b'.ljust(10) + 
                    'delta_m'.ljust(10) + 'delta_f'.ljust(10) + '\n')        


for i_vmm,i_channel in tqdm(locs_to_check):

    #1) Get train_data (if there is any for this channel)
    data_without_crazy_TDO = [event for event in TDO_dict[i_vmm, i_channel] if lower_ignore < event.TDO < top_ignore]

    if len(data_without_crazy_TDO) > min_num_data_points:

        TPDAC_select = max([event.TPDAC for event in data_without_crazy_TDO])
        train_data = np.array([[event.Delay, event.TDO] for event in data_without_crazy_TDO if event.TPDAC == TPDAC_select])

        #2) Preprocess and modify (currently, the data is not modified at all before fitting)
        sep = defaultdict(list)
        for da in train_data:
            sep[da[0]].append(da[1])
        data_mod = deepcopy(train_data)

        #3) Get initial guesses for m and b
        #guess the slope (m)
        slope_guess = slope_initial_guess

        #guess the y-intercept (b)
        find_dense = {}
        for k in sep:
            find_dense[k] = max(sep[k]) - min(sep[k])
        dense_delays = np.argsort(find_dense.values())
        b_guess = np.mean(sep[sep.keys()[dense_delays[0]]]) - slope_guess*sep.keys()[dense_delays[0]]

        #4) Find the best slope and y-intercept using gradient descent (using tensorflow for speed)
        g = tf.Graph()
        with g.as_default():
            W = tf.Variable([slope_guess], tf.float32)
            b = tf.Variable([b_guess], tf.float32)

            x = tf.placeholder(tf.float32)
            y = tf.placeholder(tf.float32)
            n_w = tf.sign(tf.floor(-1/(5*W)*(y-W*x-b-5*W/2)))
            #n_smooth = n_w + tf.pow((-1/(5*W)*(y-W*x-b-5*W/2) - n_w), 36)

            linear_model = W*x + b + -5*W * n_w
            loss = tf.reduce_mean(tf.square(linear_model - y))
            optimizer = tf.train.AdamOptimizer(learning_rate)
            train = optimizer.minimize(loss)

            x_train = data_mod[:,0]
            y_train = data_mod[:,1]

            init = tf.global_variables_initializer()

            with tf.Session() as sess:
                sess.run(init)
                l = sess.run(loss, {x:x_train, y:y_train})
                it = 0

                #training loop
                while True:
                    sess.run(train, {x:x_train, y:y_train})
                    if it%n_cycle_check:
                        l_new = sess.run(loss, {x:x_train, y:y_train})
                        if np.abs(l_new - l) < loss_difference_lower_bound:
                            break
                        l = l_new
                    it += 1

                curr_W, curr_b, curr_guess, l, ns  = sess.run([W, b, linear_model, loss, n_w], {x:x_train, y:y_train})

        curr_W = curr_W[0]; curr_b = curr_b[0];
        #correct b to most likely window (not particularly necessary but nice)
        c = Counter(ns)
        curr_b += -curr_W*5*c.most_common(1)[0][0]
        #print m_store, b_store

        #5) Determine best "floor" and "ceiling"
        nonempty = ((curr_guess[i], da[0]) for i, da in enumerate(data_mod))
        nonempty = set(nonempty)
        mixture_data = {k: [0,0,0] for k in nonempty}
        for i, da in enumerate(data_mod):
            for k in mixture_data:
                if k[1] == da[0]:
                    mixture_data[k][1 + int(np.sign(curr_guess[i] - k[0]))] += 1
        bot_floor = min(data_mod[:,1])
        bot_ceiling = max(data_mod[:,1]) + 5*curr_W
        bot_posses = np.linspace(bot_floor, bot_ceiling, num_bot_posses)
        sigma = np.sqrt(l)
        bot_probs = []
        for bot_poss in bot_posses:
            bot_percents = {k: [1 - stats.norm.cdf(bot_poss - 5*curr_W, k[0], sigma), 
                            stats.norm.cdf(bot_poss - 5*curr_W, k[0], sigma) - stats.norm.cdf(bot_poss, k[0], sigma), 
                            stats.norm.cdf(bot_poss, k[0], sigma)] for k in mixture_data}
            bot_prob = 0
            for k in bot_percents:
                for j,el in enumerate(bot_percents[k]):
                    if el > 0:
                        bot_prob += np.log(el) * mixture_data[k][j]
            bot_probs.append(bot_prob)
        bot = bot_posses[np.argmax(bot_probs)]
        top = bot - 5 * curr_W

        #6) Plot the data!  
        # fig = plt.figure(figsize=(10,6))      
        # sns.set_style("whitegrid", {'axes.grid' : False})
        # plt.plot((0,4), (bot, bot), 'k--', alpha=.3)
        # plt.plot((0,4), (top, top), 'k--', alpha=.3)
        # plt.hist2d(train_data[:,0], train_data[:,1], bins=[np.linspace(0,4,32), np.arange(10, 120)])
        # plt.colorbar()

        x_show = np.linspace(0,4,400)
        y_show = [curr_W*x_s+curr_b for x_s in x_show]
        for i,y_s in enumerate(y_show):
            if y_show[i]>top:
                y_show[i] += 5*curr_W
            if y_show[i]<bot:
                y_show[i] -= 5*curr_W
        #plt.plot(x_show, y_show, 'k', alpha=.5)

        #get parameters ready for printing
        m_convert = (top-bot)/25
        p_convert = m_convert*(-25/2) + bot

        #calculate standard error in m and b
        X_for_error = np.array([[1, da[0]] for da in train_data])
        error_mat = l*np.linalg.inv(np.matmul(X_for_error.T, X_for_error))
        chi2 = l*len(train_data) / 4

        nice_params = {}
        nice_params['Gain'] = "%.2e"%m_convert
        nice_params['Pedestal'] = "%.2e"%p_convert
        nice_params['m'] = "%.2e"%curr_W
        nice_params['b'] = "%.2e"%curr_b
        nice_params['floor'] = "%.2e"%bot
        nice_params['n_samps'] = "%.2e"%len(train_data)
        nice_params['p_8'] = "%.2e"%(len([da for da in train_data if da[1]%8==0])/len(train_data))
        nice_params['sigma'] = "%.2e"%sigma
        nice_params['chi2'] = "%.2e"%chi2
        nice_params['prob'] = "%.2e"%(1 - stats.chi2.cdf(chi2, len(train_data) - 2))
        nice_params['delta_b'] = "%.2e"%error_mat[0][0]
        nice_params['delta_m'] = "%.2e"%error_mat[1][1]
        nice_params['delta_f'] = "%.2e"%(-max(bot_probs))

        file_line = "".join([str(args.board_num).ljust(6), str(i_vmm).ljust(4), str(i_channel).ljust(4), 
                        nice_params['Gain'].ljust(10), nice_params['Pedestal'].ljust(10), nice_params['m'].ljust(10), 
                        nice_params['b'].ljust(10), nice_params['floor'].ljust(10),
                        nice_params['n_samps'].ljust(10), nice_params['p_8'].ljust(10), 
                        nice_params['sigma'].ljust(10), nice_params['chi2'].ljust(10),
                        nice_params['prob'].ljust(10), nice_params['delta_b'].ljust(10),
                        nice_params['delta_m'].ljust(10), nice_params['delta_f'].ljust(10)])
        file_line = file_line + '\n'

        #add plot styling
        # plt.xlabel('Delay')
        # plt.ylabel('TDO')
        # plt.annotate('{0: <3}'.format('m: ') + nice_params['m'], xy=(-.1,-.12), xycoords='axes fraction')
        # plt.annotate('{0: <3}'.format('b: ') + nice_params['b'], xy=(.18,-.12), xycoords='axes fraction')
        # plt.annotate('{0: <3}'.format('f: ') + nice_params['floor'], xy=(.36,-.12), xycoords='axes fraction')
        # plt.annotate('{0: <3}'.format('N: ') + nice_params['n_samps'], xy=(.54,-.12), xycoords='axes fraction')
        # plt.annotate('{0: <3}'.format('p8: ') + nice_params['p_8'], xy=(.75,-.12), xycoords='axes fraction')
        # plt.annotate('{0: <3}'.format('s: ') + nice_params['sigma'], xy=(.95,-.12), xycoords='axes fraction')
        # plt.annotate('{0: <3}'.format('ch: ') + nice_params['chi2'], xy=(1.20,.1), xycoords='axes fraction')
        # plt.annotate('{0: <3}'.format('p: ') + nice_params['prob'], xy=(1.20,.2), xycoords='axes fraction')
        # plt.annotate('{0: <3}'.format('_b: ') + nice_params['delta_b'], xy=(1.20,.3), xycoords='axes fraction')
        # plt.annotate('{0: <3}'.format('_m: ') + nice_params['delta_m'], xy=(1.20,.4), xycoords='axes fraction')
        # plt.annotate('{0: <3}'.format('_f: ') + nice_params['delta_f'], xy=(1.20,.5), xycoords='axes fraction')
        # plt.title(str(args.board_num) + '_' + str(i_vmm) + '_' + str(i_channel))
        #plt.draw()

        #plt.savefig(str(args.board_num) + '_' + str(i_vmm) + '_' + str(i_channel) + '.png')
        # plt.close(fig)
        # plt.pause(.1)
        #raw_input('')

    else:
        file_line = str(args.board_num).ljust(6) + str(i_vmm).ljust(4) + str(i_channel).ljust(4) + 'GHOST\n'
    writer.write(file_line)       
writer.close()
