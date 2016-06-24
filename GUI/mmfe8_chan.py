#!/usr/bin/env python26

#    by Charlie Armijo, Ken Johns, Bill Hart, Sarah Jones, James Wymer, Kade Gigliotti
#    Experimental Elementary Particle Physics Laboratory
#    Physics Department
#    University of Arizona    
#    armijo at physics.arizona.edu
#    johns at physics.arizona.edu
#
#    This is version 7 of the MMFE8 GUI



import pygtk
pygtk.require('2.0')
import gtk
from array import *
#### On PCROD0 use from Numpy import *
import numpy as np
#from Numeric import *
from struct import *
import gobject 
from subprocess import call
from time import sleep
import sys 
import os
import string
import random
import binstr
import socket
import time
import math


############################################################################
############################################################################
##########################                     #############################
##########################     CHANNEL CLASS   #############################
##########################                     #############################
############################################################################
############################################################################

class channel:


    def get_chan_val(self):
        return self.chan_val

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #
    #                CHANNEL FUNCTIONS     
    # 
    #  Here we take the check box and combo box data for
    #  each channel and add it to the appropriate channel
    #  array                         
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    ##### input charge polarity #####
    def SP_callback(self, widget, data=None):
        SP = self.chan_val[0]
        if widget.get_active():
            ### toggle button is down ###
            if SP == 0:
                self.chan_val[0] = 1
                widget.set_label("p")
        else:
            ### toggle button is up ###
            if SP > 0:
                self.chan_val[0] = 0
                widget.set_label("n")

    ##### large sensor capacitance mode #####
    def SC_callback(self, widget, data=None):
        SC = self.chan_val[1]
        if widget.get_active():
        ### button is checked ###
            if SC == 0:
                self.chan_val[1] = 1
        else:
        ### button is not checked ###
            if SC > 0:
                self.chan_val[1] = 0

    ##### leakage current disable #####
    def SL_callback(self, widget, data=None):
        SL = self.chan_val[2]
        if widget.get_active():
        ### button is checked ###
            if SL == 0:
                self.chan_val[2] = 1
        else:
        ### button is not checked ###
            if SL > 0:
                self.chan_val[2] = 0

    ##### test capacitor enable #####
    def ST_callback(self, widget, data=None):
        ST = self.chan_val[3]
        if widget.get_active():
        ### button is checked ###
            if ST == 0:
                #self.msg[data-1] = self.msg[data-1] + np.uint32(0x0008)
                self.chan_val[3] = 1
        else:
        ### button is not checked ###
            if ST > 0:
                #self.msg[data-1] = self.msg[data-1] - np.uint32(0x0008)
                self.chan_val[3] = 0

    ##### mask enable #####
    def SM_callback(self, widget, data=None):
        SM = self.chan_val[4]
        if widget.get_active():
        ### button is checked ###
            if SM == 0:
                #self.msg[data-1] = self.msg[data-1] + np.uint32(0x0010)
                self.chan_val[4] = 1
        else:
        ### button is not checked ###
            if SM > 0:
                #self.msg[data-1] = self.msg[data-1] - np.uint32(0x0010)
                self.chan_val[4] = 0

    ##### threshold DAC #####
    def get_SD_value(self, widget, data=None):
        active = widget.get_active()
        if active < 0:
            return None
        else:
            SD_value = active
            #self.msg[data-1] = np.uint32(0xFE1F) & self.msg[data-1] #??????????

            ### convert value to list of binary digits ###
            SD_value = '{0:04b}'.format(SD_value)
            SD_list = list(SD_value)
            SD_list = map(int, SD_value)

            ### add new value to channel_settings ###
            #self.msg[data-1] = np.uint32(SD_value) ^ self.msg[data-1] #??????????
            for i in range(3,-1,-1):        
                self.chan_val[i+5] = SD_list[i]

    ##### channel monitor mode #####
    def SMX_callback(self, widget, data=None):
        SMX = self.chan_val[9]
        if widget.get_active():
        ### button is checked ###
            if SMX == 0:
                self.chan_val[9] = 1
        else:
        ### button is not checked ###
            if SMX > 0:
                self.chan_val[9] = 0

    ##### 10-bit ADC #####
    def get_SZ10b_value(self, widget, data=None):
        active = widget.get_active()
        if active < 0:
            return None
        else:
            SZ10b = active

            ### convert value to list of binary digits ###
            SZ10b = '{0:05b}'.format(SZ10b)
            SZ10b_list = list(SZ10b)
            SZ10b_list = map(int, SZ10b)

            ### add new value to channel_settings ###
            for i in range(4,-1,-1):
                self.chan_val[i+10] = SZ10b_list[i]

    ##### 8-bit ADC #####
    def get_SZ8b_value(self, widget, data=None):
        active = widget.get_active()
        if active < 0:
            return None
        else:
            SZ8b = active

            ### convert value to list of binary digits ###
            SZ8b = '{0:04b}'.format(SZ8b)
            SZ8b_list = list(SZ8b)
            SZ8b_list = map(int, SZ8b)

            ### add new value to channel_settings ###
            for i in range(3,-1,-1):
                self.chan_val[i+15] = SZ8b_list[i]

    ##### 6-bit ADC #####
    def get_SZ6b_value(self, widget, data=None):
        active = widget.get_active()
        if active < 0:
            return None
        else:
            SZ6b = active

            ### convert value to list of binary digits ###
            SZ6b = '{0:03b}'.format(SZ6b)
            SZ6b_list = list(SZ6b)
            SZ6b_list = map(int, SZ6b)

            ### add new value to channel_settings ###
            for i in range(2,-1,-1):
                self.chan_val[i+19] = SZ6b_list[i]

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #             __init__  and  CHANNEL WIDGETS 
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    def __init__(self, ch_num):
        self.chan_val = np.zeros((24), dtype=int)
        self.channel_box = gtk.HBox(homogeneous=False,spacing=0)
        if ch_num < 9:
            self.glabel = gtk.Label( "  " + str(ch_num + 1) )
        else:
            self.glabel = gtk.Label( str(ch_num + 1) )
        self.button_SP = gtk.ToggleButton( label="n" )
        self.button_SC = gtk.CheckButton()
        self.button_SL = gtk.CheckButton()
        self.button_ST = gtk.CheckButton()
        self.button_SM = gtk.CheckButton()
        self.combo_SD = gtk.combo_box_new_text()
        self.button_SMX = gtk.CheckButton()
        self.combo_SZ10b = gtk.combo_box_new_text()
        self.combo_SZ8b = gtk.combo_box_new_text()
        self.combo_SZ6b = gtk.combo_box_new_text()
        for i in range(16):
            self.combo_SD.append_text(str(i) + " mv")
        self.combo_SD.set_active(0)
        for i in range(32):
            self.combo_SZ10b.append_text(str(i) + " ns")        
        self.combo_SZ10b.set_active(0)
        for i in range(16):
            self.combo_SZ8b.append_text(str(i) + " ns")        
        self.combo_SZ8b.set_active(0)
        for i in range(8):
            self.combo_SZ6b.append_text(str(i) + " ns")        
        self.combo_SZ6b.set_active(0)
            
        self.button_SP.connect("toggled",self.SP_callback,ch_num)
        self.button_SC.connect("toggled",self.SC_callback,ch_num)
        self.button_SL.connect("toggled",self.SL_callback,ch_num)
        self.button_ST.connect("toggled",self.ST_callback,ch_num)
        self.button_SM.connect("toggled",self.SM_callback,ch_num)
        if ch_num < 64:
            self.button_SM.set_active(True)
        self.combo_SD.connect("changed",self.get_SD_value,ch_num)
        self.button_SMX.connect("toggled",self.SMX_callback,ch_num)
        self.combo_SZ10b.connect("changed",self.get_SZ10b_value,ch_num)
        self.combo_SZ8b.connect("changed",self.get_SZ8b_value,ch_num)
        self.combo_SZ6b.connect("changed",self.get_SZ6b_value,ch_num)

        self.channel_box.pack_start(self.glabel,expand=False)
        self.channel_box.pack_start(self.button_SP,expand=False)
        self.channel_box.pack_start(self.button_SC,expand=False)
        self.channel_box.pack_start(self.button_SL,expand=False)
        self.channel_box.pack_start(self.button_ST,expand=False)
        self.channel_box.pack_start(self.button_SM,expand=False)
        self.channel_box.pack_start(self.combo_SD,expand=False)
        self.channel_box.pack_start(self.button_SMX,expand=False)
        self.channel_box.pack_start(self.combo_SZ10b,expand=False)
        self.channel_box.pack_start(self.combo_SZ8b,expand=False)
        self.channel_box.pack_start(self.combo_SZ6b,expand=False)


