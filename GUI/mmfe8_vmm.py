#!/usr/bin/env python26

#    by Charlie Armijo, Ken Johns, Bill Hart, Sarah Jones, James Wymer, Kade Gigliotti
#    Experimental Elementary Particle Physics Laboratory
#    Physics Department
#    University of Arizona    
#    armijo at physics.arizona.edu
#    johns at physics.arizona.edu
#
#
#    This is for version 7 of the MMFE8 GUI


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
from mmfe8_chan import channel
from mmfe8_udp import udp_stuff


############################################################################
############################################################################
##############################               ###############################
##############################   VMM CLASS   ###############################
##############################               ###############################
############################################################################
############################################################################

class vmm:


    def get_channel_val(self):
        for ch_num in range(64):
            chan_val = self.chan_list[ch_num].get_chan_val()
            #print str(chan_val) + " " + str(ch_num + 1)
            for i in range(24):
                self.reg[ch_num][i] = chan_val[i]
        return self.reg

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # 
    #                QUICK SET FUNCTIONS 
    #
    #  This is where we use the Quick Set button to set all
    #  or any set of channel bits.
    #  It is intended that SZ10b, SZ8b and SZ6b Combo boxes
    #  will be added in a future release.
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    def SP_qs_callback(self, widget):
        if widget.get_active():
                widget.set_label("p")
        else:
                widget.set_label("n")

    def quick_set(self, widget):
        
        if self.check_button_SP_qs.get_active():
            if self.toggle_button_SP.get_active():        
                for chan_num in range(64):
                    #if ch_num < 65:
                    self.chan_list[ch_num].button_SP.set_active(True)
                    self.chan_list[ch_num].button_SP.set_label("p") 
            else:
                for ch_num in range(64):
                    #if ch_num < 65:
                    self.chan_list[ch_num].button_SP.set_active(False)
                    self.chan_list[ch_num].button_SP.set_label("n") 
        
        if self.check_button_SC_qs.get_active():
            if self.check_button_SC.get_active():        
                for ch_num in range(64):
                    #if ch_num < 65:
                    self.chan_list[ch_num].button_SC.set_active(True) 
            else:
                for ch_num in range(64):
                    #if ch_num < 65:
                    self.chan_list[ch_num].button_SC.set_active(False)

        if self.check_button_SL_qs.get_active():
            if self.check_button_SL.get_active():        
                for ch_num in range(64):
                    #if ch_num < 65:
                    self.chan_list[ch_num].button_SL.set_active(True) 
            else:
                for ch_num in range(64):
                    #if ch_num < 65:
                    self.chan_list[ch_num].button_SL.set_active(False)

        if self.check_button_ST_qs.get_active():
            if self.check_button_ST.get_active():        
                for ch_num in range(64):
                    #if ch_num < 65:
                    self.chan_list[ch_num].button_ST.set_active(True) 
            else:
                for ch_num in range(64):
                    #if ch_num < 65:
                    self.chan_list[ch_num].button_ST.set_active(False)

        if self.check_button_SM_qs.get_active():
            if self.check_button_SM.get_active():        
                for ch_num in range(64):
                    #if ch_num < 65:
                    self.chan_list[ch_num].button_SM.set_active(True) 
            else:
                for ch_num in range(64):
                    #if ch_num < 65:
                    self.chan_list[ch_num].button_SM.set_active(False)

        if self.check_button_SD_qs.get_active():
            active = self.combo_SD_qs.get_active()        
            for ch_num in range(64):
                #if ch_num < 65:
                self.chan_list[ch_num].combo_SD.set_active(active) 

        if self.check_button_SMX_qs.get_active():
            if self.check_button_SMX.get_active():        
                for ch_num in range(64):
                    #if ch_num < 65:
                    self.chan_list[ch_num].button_SMX.set_active(True) 
            else:
                for ch_num in range(64):
                    #if ch_num < 65:
                    self.chan_list[ch_num].button_SMX.set_active(False)

        if self.check_button_SZ10b_qs.get_active():
            active = self.combo_SZ10b_qs.get_active()        
            for ch_num in range(64):
                #if ch_num < 65:
                self.chan_list[ch_num].combo_SZ10b.set_active(active) 

        if self.check_button_SZ8b_qs.get_active():
            active = self.combo_SZ8b_qs.get_active()        
            for ch_num in range(64):
                #if ch_num < 65:
                self.chan_list[ch_num].combo_SZ8b.set_active(active) 

        if self.check_button_SZ6b_qs.get_active():
            active = self.combo_SZ6b_qs.get_active()        
            for ch_num in range(64):
                #if ch_num < 65:
                self.chan_list[ch_num].combo_SZ6b.set_active(active) 




    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #
    #                GLOBAL FUNCTIONS     
    # 
    #  Here we take the check box and combo box data for
    #  the GLOBAL CONFIGURATIONS and put them in the correct 
    #  positions in a 96-bit array
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


    ##### input charge polarity #####
    def glob_SPG_callback(self, widget, data=None):
        SPG = self.globalreg[16]
        if widget.get_active():
        ### button is checked ###
            if SPG == 0:
                self.globalreg[16] = 1
        else:
        ### button is not checked ###
            if SPG > 0:
                self.globalreg[16] = 0

    ##### time delay  #####
    # def glob_DC_value(self, widget):
    #     active = widget.get_active()
    #     if active < 0:
    #         return None
    #     else:
    #         DC = active
    #         MSGsend1 = "W 0x44A10148 {0:02x} \0\n".format(DC)
    #         self.udp.udp_client(MSGsend1,self.UDP_IP,self.UDP_PORT)

    ##### disable at peak #####
    def glob_SDPeak_callback(self, widget, data=None):
        SDP = self.globalreg[17]
        if widget.get_active():
        ### button is checked ###
            if SDP == 0:
                self.globalreg[17] = 1
        else:
        ### button is not checked ###
            if SDP > 0:
                self.globalreg[17] = 0

    ##### route analog monitor to pdo output #####
    def glob_SBMX_callback(self, widget, data=None):
        SBMX = self.globalreg[18]
        if widget.get_active():
        ### button is checked ###
            if SBMX == 0:
                self.globalreg[18] = 1
        else:
        ### button is not checked ###
            if SBMX > 0:
                self.globalreg[18] = 0

    ##### analog output buffers enable tdo #####
    def glob_SBFT_callback(self, widget, data=None):
        SBFT = self.globalreg[19]
        if widget.get_active():
        ### button is checked ###
            if SBFT == 0:
                self.globalreg[19] = 1
        else:
        ### button is not checked ###
            if SBFT > 0:
                self.globalreg[19] = 0

    ##### analog output buffers enable pdo #####
    def glob_SBFP_callback(self, widget, data=None):
        SBFP = self.globalreg[20]
        if widget.get_active():
        ### button is checked ###
            if SBFP == 0:
                self.globalreg[20] = 1
        else:
        ### button is not checked ###
            if SBFP > 0:
                self.globalreg[20] = 0

    ##### analog output buffers enable mo #####
    def glob_SBFM_callback(self, widget, data=None):
        SBFM = self.globalreg[21]
        if widget.get_active():
        ### button is checked ###
            if SBFM == 0:
                self.globalreg[21] = 1
        else:
        ### button is not checked ###
            if SBFM > 0:
                self.globalreg[21] = 0

    ##### leakage current disable #####
    def glob_SLG_callback(self, widget, data=None):
        SLG = self.globalreg[22]
        if widget.get_active():
        ### button is checked ###
            if SLG == 0:
                self.globalreg[22] = 1
        else:
        ### button is not checked ###
            if SLG > 0:
                self.globalreg[22] = 0

    ##### monitor multiplexing #####
    def glob_SM_value(self, widget):
        active = widget.get_active()
        if active < 0:
            return None
        else:
            SM = active

            ### convert value to list of binary digits ###
            SM = '{0:06b}'.format(SM)
            SM_list = list(SM)
            SM_list = map(int, SM)

            ### add new value to register ###
            for i in range(5,-1,-1):
                self.globalreg[i+23] = SM_list[i]

    ##### monitor multiplexing enable #####
    def glob_SCMX_callback(self, widget, data=None):
        SCMX = self.globalreg[29]
        if widget.get_active():
        ### button is checked ###
            if SCMX == 0:
                self.globalreg[29] = 1
        else:
        ### button is not checked ###
            if SCMX > 0:
                self.globalreg[29] = 0

    ##### ART enable #####
    def glob_SFA_callback(self, widget, data=None):
        SFA = self.globalreg[30]
        if widget.get_active():
        ### button is checked ###
            if SFA == 0:
                self.globalreg[30] = 1
        else:
        ### button is not checked ###
            if SFA > 0:
                self.globalreg[30] = 0

    ##### ART mode #####
    def glob_SFAM_value(self, widget, data=None):
        SFAM = self.globalreg[31]
        if widget.get_active():
        ### 2nd option is selected ###
            if SFAM == 0:
               self.globalreg[31] = 1
        else:
        ### 1st option is selected ###
            if SFAM > 0:
                self.globalreg[31] = 0

    ##### peaking time #####
    def glob_ST_value(self, widget):
        active = widget.get_active()
        if active < 0:
            return None
        else:
            ST = active

            ### convert value to list of binary digits ###
            ST = '{0:02b}'.format(ST)
            ST_list = list(ST)
            ST_list = map(int, ST)

            ### add new value to register ###
            for i in range(1,-1,-1):
                self.globalreg[i+32] = ST_list[i]

    ##### UNKNOWN #####
    def glob_SFM_callback(self, widget, data=None):
        SFM = self.globalreg[34]
        if widget.get_active():
        ### button is checked ###
            if SFM == 0:
                self.globalreg[34] = 1
        else:
        ### button is not checked ###
            if SFM > 0:
                self.globalreg[34] = 0

    ##### gain #####
    def glob_SG_value(self, widget):
        active = widget.get_active()
        if active < 0:
            return None
        else:
            SG = active

            ### convert value to list of binary digits ###
            SG = '{0:03b}'.format(SG)
            SG_list = list(SG)
            SG_list = map(int, SG)

            ### add new value to register ###
            for i in range(2,-1,-1):
                self.globalreg[i+35] = SG_list[i]

    ##### neighbor triggering enable #####
    def glob_SNG_callback(self, widget, data=None):
        SNG = self.globalreg[38]
        if widget.get_active():
        ### button is checked ###
            if SNG == 0:
                self.globalreg[38] = 1
        else:
        ### button is not checked ###
            if SNG > 0:
                self.globalreg[38] = 0

    ##### timing outputs control ##### 
    def glob_STOT_value(self, widget, data=None):
        STOT = self.globalreg[39]
        if widget.get_active():
        ### button is checked ###
            if STOT == 0:
                self.globalreg[39] = 1
        else:
        ### button is not checked ###
            if STOT > 0:
                self.globalreg[39] = 0

    ##### timing outputs enable #####
    def glob_STTT_callback(self, widget, data=None):
        STTT = self.globalreg[40]
        if widget.get_active():
        ### button is checked ###
            if STTT == 0:
                self.globalreg[40] = 1
        else:
        ### button is not checked ###
            if STTT > 0:
                self.globalreg[40] = 0

    ##### sub-hysteresis discrimination enable #####
    def glob_SSH_callback(self, widget, data=None):
        SSH = self.globalreg[41]
        if widget.get_active():
        ### button is checked ###
            if SSH == 0:
                self.globalreg[41] = 1
        else:
        ### button is not checked ###
            if SSH > 0:
                self.globalreg[41] = 0

    ##### TAC slope adjustment #####
    def glob_STC_value(self,widget):
        active = widget.get_active()
        if active < 0:
            return None
        else:
            STC = active

            ### convert value to list of binary digits ###
            STC = '{0:02b}'.format(STC)
            STC_list = list(STC)
            STC_list = map(int, STC)

            ### add new value to register ###
            for i in range(1,-1,-1):
                self.globalreg[i+42] = STC_list[i]

    ##### course threshold DAC #####
    def glob_SDT_entry(self, widget, entry):
        try:
            entry = widget.get_text()
            value = int(entry)
        except ValueError:
            print "SDT value must be a decimal number"
            print
            return None                
        if (value < 0) or (1023 < value):
            print "SDT value out of range"
            print
            return None
        else:
            SDT = value

            ### convert value to list of binary digits ###
            SDT = '{0:010b}'.format(SDT)
            SDT_list = list(SDT)
            SDT_list = map(int, SDT)

            ### add new value to register ###
            for i in range(9,-1,-1):
                self.globalreg[i+44] = SDT_list[i] ## 28

    ##### test pulse DAC #####
    def glob_SDP_entry(self,widget,entry):
        try:
            entry = widget.get_text()
            value = int(entry)
        except ValueError:
            print "SDP value must be a decimal number"
            print
            return None                
        if (value < 0) or (1023 < value):
            print "SDP value out of range"
            print
            return None
        else:
            SDP = value

            ### convert value to list of binary digits ###
            SDP = '{0:010b}'.format(SDP)
            SDP_list = list(SDP)
            SDP_list = map(int, SDP)

            ### add new value to register ###
            for i in range(9,-1,-1):
                self.globalreg[i+54] = SDP_list[i] ## 38

    ##### 10-bit ADC conversion time #####
    def glob_SC10b_value(self,widget):
        active = widget.get_active()
        if active < 0:
            return None
        else:
            SC10b = active

            ### convert value to list of binary digits ###
            SC10b = '{0:02b}'.format(SC10b)
            SC10b_list = list(SC10b)
            SC10b_list = map(int, SC10b)

            ### add new value to register ###
            # reverse bit order
            for i in range(2):
                self.globalreg[65-i] = SC10b_list[i]

    ##### 8-bit ADC conversion time #####
    def glob_SC8b_value(self,widget):
        active = widget.get_active()
        if active < 0:
            return None
        else:
            SC8b = active

            ### convert value to list of binary digits ###
            SC8b = '{0:02b}'.format(SC8b)
            SC8b_list = list(SC8b)
            SC8b_list = map(int, SC8b)

            ### add new value to register ###
            # reverse bit order
            for i in range(2):
                self.globalreg[67-i] = SC8b_list[i]

    ##### 6-bit ADC conversion time #####
    def glob_SC6b_value(self,widget):
        active = widget.get_active()
        if active < 0:
            return None
        else:
            SC6b = active

            ### convert value to list of binary digits ###
            SC6b = '{0:03b}'.format(SC6b)
            SC6b_list = list(SC6b)
            SC6b_list = map(int, SC6b)

            ### add new value to register ###
            # reverse bit order
            for i in range(3):
                self.globalreg[70-i] = SC6b_list[i]

    ##### 8-bit ADC conversion mode #####
    def glob_S8b_callback(self,widget, data=None):
        S8b = self.globalreg[71]
        if widget.get_active():
        ### button is checked ###
            if S8b == 0:
               self.globalreg[71] = 1
        else:
        ### button is not checked ###
            if S8b > 0:
                self.globalreg[71] = 0

    ##### 6-bit ADC conversion enable #####
    def glob_S6b_callback(self, widget, data=None):
        S6b = self.globalreg[72]
        if widget.get_active():
        ### button is checked ###
            if S6b == 0:
                self.globalreg[72] = 1
        else:
        ### button is not checked ###
            if S6b > 0:
                self.globalreg[72] = 0

    ##### ADCs enable #####
    def glob_SPDC_callback(self, widget, data=None):
        SPDC = self.globalreg[73]
        if widget.get_active():
        ### button is checked ###
            if SPDC == 0:
                self.globalreg[73] = 1
        else:
        ### button is not checked ###
            if SPDC > 0:
                self.globalreg[73] = 0

    ##### dual clock edge serialized data enable #####
    def glob_SDCKS_callback(self, widget, data=None):
        SDCKS = self.globalreg[74]
        if widget.get_active():
        ### button is checked ###
            if SDCKS == 0:
                self.globalreg[74] = 1
        else:
        ### button is not checked ###
            if SDCKS > 0:
                self.globalreg[74] = 0

    ##### dual clock edge serialized ART enable #####
    def glob_SDCKA_callback(self, widget, data=None):
        SDCKA = self.globalreg[75]
        if widget.get_active():
        ### button is checked ###
            if SDCKA == 0:
                self.globalreg[75] = 1
        else:
        ### button is not checked ###
            if SDCKA > 0:
                self.globalreg[75] = 0

    ##### dual clock edge serialized 6-bit enable #####
    def glob_SDCK6b_callback(self, widget, data=None):
        SDCK6b = self.globalreg[76]
        if widget.get_active():
        ### button is checked ###
            if SDCK6b == 0:
                self.globalreg[76] = 1
        else:
        ### button is not checked ###
            if SDCK6b > 0:
                self.globalreg[76] = 0

    ##### tristates analog outputs with token, used in analog mode #####
    def glob_SDRV_callback(self, widget, data=None):
        SDRV = self.globalreg[77]
        if widget.get_active():
        ### button is checked ###
            if SDRV == 0:
                self.globalreg[77] = 1
        else:
        ### button is not checked ###
            if SDRV > 0:
                self.globalreg[77] = 0

    ##### timing outputs control 2 #####
    def glob_STPP_callback(self, widget, data=None):
        STPP = self.globalreg[78]
        if widget.get_active():
        ### button is checked ###
            if STPP == 0:
                self.globalreg[78] = 1
        else:
        ### button is not checked ###
            if STPP > 0:
                self.globalreg[78] = 0


    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #                                     <<===============
    #                      VMM __INIT__   <<=============== 
    #                                     <<===============
    #  Here we build the necessary variables and widgets
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    

    def __init__(self):
        #self.vmm_num = vmm_num
        ## array of 64 24-bit channel settings
        self.channel_settings = np.zeros((64, 24), dtype=int)
        ## vmm global configuration settings
        self.global_settings = np.zeros((96), dtype=int)
        #chanObjList = channel.chan_obj_list()
        self.chan_list = []
        self.reg = np.zeros((64, 24), dtype=int)
        self.msg = np.zeros((67), dtype=np.uint32)
        self.globalreg = np.zeros((96), dtype=int)
        #self.reg = np.zeros((64, 24), dtype=int)
        
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%%%%               %%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%%%%  VMM WIDGETS  %%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%%%%               %%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #          
        #                    64 CHANNELS 
        #
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #                  CHANNEL LABELS 
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        self.label_Chan_num_a = gtk.Label("    \n   ")
        self.label_Chan_SP_a = gtk.Label("     S \n     P ")
        self.label_Chan_SP_a.set_markup('<span color="blue"><b>  S \n  P </b></span>')
        self.label_Chan_SC_a = gtk.Label("S\nC")
        self.label_Chan_SC_a.set_markup('<span color="blue"><b> S \n C </b></span>')
        self.label_Chan_ST_a = gtk.Label("S\nL")
        self.label_Chan_ST_a.set_markup('<span color="blue"><b> S \n L</b></span>')
        self.label_Chan_SL_a = gtk.Label("S\nT")
        self.label_Chan_SL_a.set_markup('<span color="blue"><b>  S \n  T </b></span>')
        self.label_Chan_SM_a = gtk.Label("S\nM")
        self.label_Chan_SM_a.set_markup('<span color="blue"><b> S    \n M     </b></span>')
        self.label_Chan_SD_a = gtk.Label("SD")
        self.label_Chan_SD_a.set_markup('<span color="blue"><b>  SD     </b></span>')
        self.label_Chan_SMX_a = gtk.Label("S\nM\nX")
        self.label_Chan_SMX_a.set_markup('<span color="blue"><b> S  \n M  \n X  </b></span>')
        self.label_Chan_SZ10b_a = gtk.Label("SZ10b")
        self.label_Chan_SZ10b_a.set_markup('<span color="blue"><b>  SZ10b   </b></span>')
        self.label_Chan_SZ8b_a = gtk.Label("SZ8b")
        self.label_Chan_SZ8b_a.set_markup('<span color="blue"><b>  SZ8b    </b></span>')
        self.label_Chan_SZ6b_a = gtk.Label("SZ6b")        
        self.label_Chan_SZ6b_a.set_markup('<span color="blue"><b>  SZ6b    </b></span>')

        self.box_chan_labels_a = gtk.HBox()
        self.box_chan_labels_a.pack_start(self.label_Chan_num_a)
        self.box_chan_labels_a.pack_start(self.label_Chan_SP_a)
        self.box_chan_labels_a.pack_start(self.label_Chan_SC_a)
        self.box_chan_labels_a.pack_start(self.label_Chan_ST_a)
        self.box_chan_labels_a.pack_start(self.label_Chan_SL_a)
        self.box_chan_labels_a.pack_start(self.label_Chan_SM_a)
        self.box_chan_labels_a.pack_start(self.label_Chan_SD_a)
        self.box_chan_labels_a.pack_start(self.label_Chan_SMX_a)
        self.box_chan_labels_a.pack_start(self.label_Chan_SZ10b_a)
        self.box_chan_labels_a.pack_start(self.label_Chan_SZ8b_a)
        self.box_chan_labels_a.pack_start(self.label_Chan_SZ6b_a)

        self.label_Chan_num_b = gtk.Label("    \n   ")
        self.label_Chan_SP_b = gtk.Label("     S \n     P ")
        self.label_Chan_SP_b.set_markup('<span color="blue"><b>  S \n  P </b></span>')
        self.label_Chan_SC_b = gtk.Label(" S \n C ")
        self.label_Chan_SC_b.set_markup('<span color="blue"><b> S \n C </b></span>')
        self.label_Chan_ST_b = gtk.Label(" S \n L ")
        self.label_Chan_ST_b.set_markup('<span color="blue"><b> S \n L </b></span>')
        self.label_Chan_SL_b = gtk.Label(" S \n T ")
        self.label_Chan_SL_b.set_markup('<span color="blue"><b>  S \n  T </b></span>')
        self.label_Chan_SM_b = gtk.Label("S    \nM    ")
        self.label_Chan_SM_b.set_markup('<span color="blue"><b> S    \n M     </b></span>')
        self.label_Chan_SD_b = gtk.Label("  SD     ")
        self.label_Chan_SD_b.set_markup('<span color="blue"><b>  SD     </b></span>')
        self.label_Chan_SMX_b = gtk.Label(" S  \n M  \n X  ")
        self.label_Chan_SMX_b.set_markup('<span color="blue"><b> S  \n M  \n X  </b></span>')
        self.label_Chan_SZ10b_b = gtk.Label("  SZ10b   ")
        self.label_Chan_SZ10b_b.set_markup('<span color="blue"><b>  SZ10b   </b></span>')
        self.label_Chan_SZ8b_b = gtk.Label("  SZ8b    ")
        self.label_Chan_SZ8b_b.set_markup('<span color="blue"><b>  SZ8b    </b></span>')
        self.label_Chan_SZ6b_b = gtk.Label("  SZ6b    ")        
        self.label_Chan_SZ6b_b.set_markup('<span color="blue"><b>  SZ6b    </b></span>')

        self.box_chan_labels_b = gtk.HBox()
        self.box_chan_labels_b.pack_start(self.label_Chan_num_b)
        self.box_chan_labels_b.pack_start(self.label_Chan_SP_b)
        self.box_chan_labels_b.pack_start(self.label_Chan_SC_b)
        self.box_chan_labels_b.pack_start(self.label_Chan_ST_b)
        self.box_chan_labels_b.pack_start(self.label_Chan_SL_b)
        self.box_chan_labels_b.pack_start(self.label_Chan_SM_b)
        self.box_chan_labels_b.pack_start(self.label_Chan_SD_b)
        self.box_chan_labels_b.pack_start(self.label_Chan_SMX_b)
        self.box_chan_labels_b.pack_start(self.label_Chan_SZ10b_b)
        self.box_chan_labels_b.pack_start(self.label_Chan_SZ8b_b)
        self.box_chan_labels_b.pack_start(self.label_Chan_SZ6b_b)

        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #                     CHANNEL WIDGETS 
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
        for chan_num in range(64):
            self.chan_list.append(channel(chan_num))

        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #                   QUICK SET WIDGETS   
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


        self.button_quick_set = gtk.Button("QUICK SET")
        self.button_quick_set.connect("clicked",self.quick_set)
        self.button_quick_set.set_sensitive(True)

        self.check_button_SP_qs = gtk.CheckButton()
        self.check_button_SC_qs = gtk.CheckButton()
        self.check_button_SL_qs = gtk.CheckButton()
        self.check_button_ST_qs = gtk.CheckButton()
        self.check_button_SM_qs = gtk.CheckButton()
        self.check_button_SD_qs = gtk.CheckButton()
        self.check_button_SMX_qs = gtk.CheckButton()
        self.check_button_SZ10b_qs = gtk.CheckButton()
        self.check_button_SZ8b_qs = gtk.CheckButton()
        self.check_button_SZ6b_qs = gtk.CheckButton()

        self.toggle_button_SP = gtk.ToggleButton(label="n")
        self.toggle_button_SP.connect("toggled",self.SP_qs_callback)
        self.check_button_SC = gtk.CheckButton()
        self.check_button_SL = gtk.CheckButton()
        self.check_button_ST = gtk.CheckButton()
        self.check_button_SM = gtk.CheckButton()
        self.combo_SD_qs = gtk.combo_box_new_text()
        self.check_button_SMX = gtk.CheckButton()
        self.combo_SZ10b_qs = gtk.combo_box_new_text()
        self.combo_SZ8b_qs = gtk.combo_box_new_text()
        self.combo_SZ6b_qs = gtk.combo_box_new_text()

        #self.label_Chan_num_qs = gtk.Label(" \n ")
        self.label_Chan_SP_qs = gtk.Label("SP")
        self.label_Chan_SC_qs = gtk.Label("SC")
        self.label_Chan_SL_qs = gtk.Label("SL")
        self.label_Chan_ST_qs = gtk.Label("ST")
        self.label_Chan_SM_qs = gtk.Label("SM")
        self.label_Chan_SD_qs = gtk.Label("SD")
        self.label_Chan_SMX_qs = gtk.Label("SMX")
        self.label_Chan_SZ10b_qs = gtk.Label("SZ10b")
        self.label_Chan_SZ8b_qs = gtk.Label("SZ8b")
        self.label_Chan_SZ6b_qs = gtk.Label("SZ6b")

        for i in range(16):
            self.combo_SD_qs.append_text(str(i) + " mv")
        self.combo_SD_qs.set_active(0)
        for i in range(32):
            self.combo_SZ10b_qs.append_text(str(i) + " ns")
        self.combo_SZ10b_qs.set_active(0)
        for i in range(16):
            self.combo_SZ8b_qs.append_text(str(i) + " ns")
        self.combo_SZ8b_qs.set_active(0)
        for i in range(8):
            self.combo_SZ6b_qs.append_text(str(i) + " ns")
        self.combo_SZ6b_qs.set_active(0)

        self.check_button_SP_qs.set_sensitive(True)
        self.check_button_SC_qs.set_sensitive(True)
        self.check_button_SL_qs.set_sensitive(True)
        self.check_button_ST_qs.set_sensitive(True)
        self.check_button_SM_qs.set_sensitive(True)
        self.check_button_SD_qs.set_sensitive(True)
        self.check_button_SMX_qs.set_sensitive(True)
        self.check_button_SZ10b_qs.set_sensitive(True)
        self.check_button_SZ8b_qs.set_sensitive(True)
        self.check_button_SZ6b_qs.set_sensitive(True)

        self.toggle_button_SP.set_sensitive(True)
        self.check_button_SC.set_sensitive(True)
        self.check_button_SL.set_sensitive(True)
        self.check_button_ST.set_sensitive(True)
        self.check_button_SM.set_sensitive(True)
        self.combo_SD_qs.set_sensitive(True)
        self.check_button_SMX.set_sensitive(True)
        self.combo_SZ10b_qs.set_sensitive(True)
        self.combo_SZ8b_qs.set_sensitive(True)
        self.combo_SZ6b_qs.set_sensitive(True)


        self.qs_table = gtk.Table(rows=5, columns=10, homogeneous=False)
        self.qs_table.attach(self.label_Chan_SP_qs, left_attach=0, right_attach=1, top_attach=0, bottom_attach=1, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.check_button_SP_qs, left_attach=0, right_attach=1, top_attach=1, bottom_attach=2, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.toggle_button_SP, left_attach=0, right_attach=1, top_attach=2, bottom_attach=3, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.label_Chan_SC_qs, left_attach=1, right_attach=2, top_attach=0, bottom_attach=1, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.check_button_SC_qs, left_attach=1, right_attach=2, top_attach=1, bottom_attach=2, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.check_button_SC, left_attach=1, right_attach=2, top_attach=2, bottom_attach=3, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.label_Chan_SL_qs, left_attach=2, right_attach=3, top_attach=0, bottom_attach=1, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.check_button_SL_qs, left_attach=2, right_attach=3, top_attach=1, bottom_attach=2, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.check_button_SL, left_attach=2, right_attach=3, top_attach=2, bottom_attach=3, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.label_Chan_ST_qs, left_attach=3, right_attach=4, top_attach=0, bottom_attach=1, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.check_button_ST_qs, left_attach=3, right_attach=4, top_attach=1, bottom_attach=2, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.check_button_ST, left_attach=3, right_attach=4, top_attach=2, bottom_attach=3, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.label_Chan_SM_qs, left_attach=4, right_attach=5, top_attach=0, bottom_attach=1, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.check_button_SM_qs, left_attach=4, right_attach=5, top_attach=1, bottom_attach=2, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.check_button_SM, left_attach=4, right_attach=5, top_attach=2, bottom_attach=3, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.label_Chan_SD_qs, left_attach=5, right_attach=6, top_attach=0, bottom_attach=1, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.check_button_SD_qs, left_attach=5, right_attach=6, top_attach=1, bottom_attach=2, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.combo_SD_qs, left_attach=5, right_attach=6, top_attach=2, bottom_attach=3, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.label_Chan_SMX_qs, left_attach=6, right_attach=7, top_attach=0, bottom_attach=1, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.check_button_SMX_qs, left_attach=6, right_attach=7, top_attach=1, bottom_attach=2, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.check_button_SMX, left_attach=6, right_attach=7, top_attach=2, bottom_attach=3, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.label_Chan_SZ10b_qs, left_attach=7, right_attach=8, top_attach=0, bottom_attach=1, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.check_button_SZ10b_qs, left_attach=7, right_attach=8, top_attach=1, bottom_attach=2, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.combo_SZ10b_qs, left_attach=7, right_attach=8, top_attach=2, bottom_attach=3, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.label_Chan_SZ8b_qs, left_attach=8, right_attach=9, top_attach=0, bottom_attach=1, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.check_button_SZ8b_qs, left_attach=8, right_attach=9, top_attach=1, bottom_attach=2, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.combo_SZ8b_qs, left_attach=8, right_attach=9, top_attach=2, bottom_attach=3, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.label_Chan_SZ6b_qs, left_attach=9, right_attach=10, top_attach=0, bottom_attach=1, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.check_button_SZ6b_qs, left_attach=9, right_attach=10, top_attach=1, bottom_attach=2, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.combo_SZ6b_qs, left_attach=9, right_attach=10, top_attach=2, bottom_attach=3, xpadding=0, xoptions=gtk.SHRINK, ypadding=0)
        self.qs_table.attach(self.button_quick_set, left_attach=0, right_attach=10, top_attach=4, bottom_attach=5, xpadding=0,  ypadding=0)


        ####################################################
        #####################            ###################
        ##################### vmm Global ###################
        ##################### variables  ###################
        #####################            ###################
        ####################################################

        self.label_Global = gtk.Label("GLOBAL CONFIGURATION")
        self.label_Global.set_markup('<span color="blue" size="18000">      <b><u>GLOBAL CONFIGURATION</u></b></span>')
        self.label_Global.set_justify(gtk.JUSTIFY_CENTER)
        self.box_Global = gtk.HBox()
        self.box_Global.pack_start(self.label_Global, expand=False)

        self.check_button_SPG = gtk.CheckButton() 
        self.label_SPG = gtk.Label("Input Charge Polarity")
        self.label_SPG.set_markup('<span color="blue"><b>Input Charge Polarity   </b></span>')
        self.label_SPGa = gtk.Label(" spg")   
        self.check_button_SPG.connect("toggled", self.glob_SPG_callback)
        self.box_SPG = gtk.HBox()
        self.box_SPG.pack_start(self.label_SPG, expand=False) 
        self.box_SPG.pack_start(self.check_button_SPG, expand=False)
        self.box_SPG.pack_start(self.label_SPGa, expand=False)
            
        self.label_SBMX = gtk.Label("Route Analog Monitor to PDO Output")
        self.label_SBMX.set_markup('<span color="blue"><b>Route Analog Monitor to PDO Output   </b></span>')
        self.check_button_SBMX = gtk.CheckButton("")
        self.check_button_SBMX.connect("toggled", self.glob_SBMX_callback)
        self.check_button_SBMX.set_active(1) # default is checked on
        self.label_SBMXa = gtk.Label(" sbmx")
        self.box_SBMX = gtk.HBox()
        self.box_SBMX.pack_start(self.label_SBMX, expand=False)
        self.box_SBMX.pack_start(self.check_button_SBMX, expand=False)
        self.box_SBMX.pack_start(self.label_SBMXa, expand=False)

        self.label_SDP = gtk.Label("Disable-at-Peak")
        self.label_SDP.set_markup('<span color="blue"><b>Disable-at-Peak   </b></span>')
        self.check_button_SDP = gtk.CheckButton()
        self.check_button_SDP.connect("toggled", self.glob_SDPeak_callback)
        self.label_SDPa = gtk.Label(" sdp")
        self.box_SDP = gtk.HBox()
        self.box_SDP.pack_start(self.label_SDP, expand=False)
        self.box_SDP.pack_start(self.check_button_SDP, expand=False)
        self.box_SDP.pack_start(self.label_SDPa, expand=False)

        self.label_SBXX = gtk.Label("Analog Output Buffers:")
        self.label_SBXX.set_markup('<span color="blue"><b>Analog Output Buffers   </b></span>')
        self.check_button_SBFT = gtk.CheckButton("TDO")
        self.check_button_SBFT.connect("toggled", self.glob_SBFT_callback)
        self.check_button_SBFT.set_active(0)
        self.check_button_SBFP = gtk.CheckButton("PDO")
        self.check_button_SBFP.connect("toggled", self.glob_SBFP_callback)
        self.check_button_SBFP.set_active(0)
        self.check_button_SBFM = gtk.CheckButton("MO")
        self.check_button_SBFM.connect("toggled", self.glob_SBFM_callback)
        self.check_button_SBFM.set_active(0)
        self.box_SBXX = gtk.HBox()
        self.box_SBXX.pack_start(self.label_SBXX, expand=False)
        self.box_SBXX.pack_start(self.check_button_SBFT, expand=False)
        self.box_SBXX.pack_start(self.check_button_SBFP, expand=False)
        self.box_SBXX.pack_start(self.check_button_SBFM, expand=False)
        
        self.check_button_SLG = gtk.CheckButton() 
        self.label_SLG = gtk.Label("Leakage Current Disable")
        self.label_SLG.set_markup('<span color="blue"><b>Leakage Current Disable   </b></span>')   
        self.check_button_SLG.connect("toggled", self.glob_SLG_callback)
        self.label_SLGa = gtk.Label(" slg")
        self.box_SLG = gtk.HBox()
        self.box_SLG.pack_start(self.label_SLG, expand=False) 
        self.box_SLG.pack_start(self.check_button_SLG, expand=False)
        self.box_SLG.pack_start(self.label_SLGa, expand=False)

        self.label_SM = gtk.Label("   Monitor")
        self.label_SM.set_markup('<span color="blue"><b>   Monitor   </b></span>')
        self.combo_SM = gtk.combo_box_new_text()
        self.combo_SM.connect("changed", self.glob_SM_value)
        self.combo_SM.append_text("CHN 1")
        self.combo_SM.append_text("CHN 2 | pulser DAC")
        self.combo_SM.append_text("CHN 3 | threshold DAC")
        self.combo_SM.append_text("CHN 4 | band-gap ref")
        self.combo_SM.append_text("CHN 5 | temp")
        for i in range(5, 64):
            self.combo_SM.append_text("CHN " + str(i+1))
        self.combo_SM.set_active(8)
        self.label_SCMX = gtk.Label(" scmx")
        self.label_SCMX.set_markup('<span color="blue"><b>SCMX   </b></span>')
        self.check_button_SCMX = gtk.CheckButton()   
        self.check_button_SCMX.connect("toggled", self.glob_SCMX_callback)
        self.check_button_SCMX.set_active(1)
        self.box_SCMX = gtk.HBox()
        self.box_SCMX.pack_start(self.label_SCMX, expand=False)
        self.box_SCMX.pack_start(self.check_button_SCMX, expand=False)
        self.box_SCMX.pack_start(self.label_SM, expand=False) 
        self.box_SCMX.pack_start(self.combo_SM, expand=False)

        self.label_SFA = gtk.Label("ART Enable")
        self.label_SFA.set_markup('<span color="blue"><b>ART Enable   </b></span>')    
        self.check_button_SFA = gtk.CheckButton()
        self.check_button_SFA.connect("toggled",self.glob_SFA_callback)
        self.check_button_SFA.set_active(True)
        self.label_SFAa = gtk.Label(" sfa")
        self.label_mode_SFAM = gtk.Label("  Mode    ")
        self.label_mode_SFAM.set_markup('<span color="blue"><b>  Mode    </b></span>')
        self.combo_SFAM = gtk.combo_box_new_text()
        self.combo_SFAM.connect("changed",self.glob_SFAM_value)
        self.combo_SFAM.append_text("timing-at-threshold")      
        self.combo_SFAM.append_text("timing-at-peak")
        self.combo_SFAM.set_active(0)
        self.label_SFAM = gtk.Label(" sfam")
        self.box_SFAM = gtk.HBox()
        self.box_SFAM.pack_start(self.label_SFA, expand=False)
        self.box_SFAM.pack_start(self.check_button_SFA, expand=False)
        self.box_SFAM.pack_start(self.label_SFAa, expand=False)
        self.box_SFAM.pack_start(self.label_mode_SFAM, expand=False)
        self.box_SFAM.pack_start(self.combo_SFAM, expand=False)
        self.box_SFAM.pack_start(self.label_SFAM, expand=False)

        self.label_Var_ST = gtk.Label("Peaking Time")
        self.label_Var_ST.set_markup('<span color="blue"><b>Peaking Time   </b></span>')
        self.combo_ST = gtk.combo_box_new_text()
        self.combo_ST.connect("changed",self.glob_ST_value)
        self.combo_ST.append_text("200 ns")
        self.combo_ST.append_text("100 ns")
        self.combo_ST.append_text("50 ns")
        self.combo_ST.append_text("25 ns")
        self.combo_ST.set_active(0)
        self.label_ST = gtk.Label(" st")
        self.box_ST = gtk.HBox()
        self.box_ST.pack_start(self.label_Var_ST, expand=False)
        self.box_ST.pack_start(self.combo_ST, expand=False)
        self.box_ST.pack_start(self.label_ST, expand=False)

        # self.label_Var_DC = gtk.Label("Delay Counts")
        # self.label_Var_DC.set_markup('<span color="blue"><b> Delay Counts   </b></span>')
        # self.combo_DC = gtk.combo_box_new_text()
        # self.combo_DC.connect("changed",self.glob_DC_value)
        # self.combo_DC.append_text("0")
        # self.combo_DC.append_text("1")
        # self.combo_DC.append_text("2")
        # self.combo_DC.append_text("3")
        # self.combo_DC.append_text("4")
        # self.combo_DC.set_active(0)
        # self.label_DC = gtk.Label(" st")
        # self.box_DC = gtk.HBox()
        # self.box_DC.pack_start(self.label_Var_DC, expand=False)
        # self.box_DC.pack_start(self.combo_DC, expand=False)
        # self.box_DC.pack_start(self.label_DC, expand=False)

        self.check_button_SFM = gtk.CheckButton()
        self.label_SFM = gtk.Label("SFM")
        self.label_SFM.set_markup('<span color="blue"><b>SFM   </b></span>')   
        self.check_button_SFM.connect("toggled", self.glob_SFM_callback)
        self.check_button_SFM.set_active(1)
        self.label_SFMb = gtk.Label("  Doubles the Leakage Current")
        self.label_SFMb.set_markup('<span color="blue"><b>  (Doubles the Leakage Current)</b></span>')        
        self.box_SFM = gtk.HBox()
        self.box_SFM.pack_start(self.label_SFM, expand=False) 
        self.box_SFM.pack_start(self.check_button_SFM, expand=False)
        self.box_SFM.pack_start(self.label_SFMb, expand=False)

        self.label_Var_SG = gtk.Label("Gain")
        self.label_Var_SG.set_markup('<span color="blue"><b>Gain   </b></span>')
        self.combo_SG = gtk.combo_box_new_text()
        self.combo_SG.connect("changed",self.glob_SG_value)
        self.combo_SG.append_text("0.5 (000)")     
        self.combo_SG.append_text("1 (001)")
        self.combo_SG.append_text("3 (010)")
        self.combo_SG.append_text("4.5 (011)")
        self.combo_SG.append_text("6 (100)")
        self.combo_SG.append_text("9 (101)")
        self.combo_SG.append_text("12 (110)")
        self.combo_SG.append_text("16 (111)")
        self.combo_SG.set_active(5)
        self.label_SG = gtk.Label(" (mV/fC)    sg")
        self.box_SG = gtk.HBox()
        self.box_SG.pack_start(self.label_Var_SG, expand=False)
        self.box_SG.pack_start(self.combo_SG, expand=False)
        self.box_SG.pack_start(self.label_SG, expand=False)

        self.check_button_SNG = gtk.CheckButton() 
        self.label_SNG = gtk.Label("Neighbor Triggering")
        self.label_SNG.set_markup('<span color="blue"><b>Neighbor Triggering   </b></span>')    
        self.check_button_SNG.connect("toggled",self.glob_SNG_callback)
        self.label_SNGa = gtk.Label(" sng")
        self.box_SNG = gtk.HBox()
        self.box_SNG.pack_start(self.label_SNG, expand=False) 
        self.box_SNG.pack_start(self.check_button_SNG,expand=False)
        self.box_SNG.pack_start(self.label_SNGa, expand=False) 

        self.label_STTT = gtk.Label("Timing Outputs")
        self.label_STTT.set_markup('<span color="blue"><b>Timing Outputs </b></span>')
        self.check_button_STTT = gtk.CheckButton()
        self.check_button_STTT.connect("toggled",self.glob_STTT_callback)
        self.label_STTTa = gtk.Label(" sttt")
        self.label_mode_STOT = gtk.Label("  Mode    ")
        self.label_mode_STOT.set_markup('<span color="blue"><b>  Mode  </b></span>')
        self.combo_STOT = gtk.combo_box_new_text()
        self.combo_STOT.connect("changed",self.glob_STOT_value)      
        self.combo_STOT.append_text("threshold-to-peak")
        self.combo_STOT.append_text("time-over-threshold")
        self.combo_STOT.set_active(0)        
        self.label_STOT = gtk.Label(" stot")
        self.box_STXX = gtk.HBox()
        self.box_STXX.pack_start(self.label_STTT, expand=False)                
        self.box_STXX.pack_start(self.check_button_STTT, expand=False)
        self.box_STXX.pack_start(self.label_STTTa, expand=False)
        self.box_STXX.pack_start(self.label_mode_STOT, expand=False)
        self.box_STXX.pack_start(self.combo_STOT, expand=False)
        self.box_STXX.pack_start(self.label_STOT, expand=False)

        self.label_SSH = gtk.Label("Sub-Hysteresis\nDiscrimination")    
        self.label_SSH.set_markup('<span color="blue"><b>Sub-Hysteresis   \nDiscrimination</b></span>')
        self.check_button_SSH = gtk.CheckButton()
        self.check_button_SSH.connect("toggled", self.glob_SSH_callback)
        self.label_SSHa = gtk.Label(" ssh")
        self.box_SSH = gtk.HBox()
        self.box_SSH.pack_start(self.label_SSH, expand=False)        
        self.box_SSH.pack_start(self.check_button_SSH, expand=False)
        self.box_SSH.pack_start(self.label_SSHa, expand=False)

        self.label_STPP = gtk.Label("Timing Outputs Control 2")    
        self.label_STPP.set_markup('<span color="blue"><b>Timing Outputs Control 2   </b></span>')
        self.check_button_STPP = gtk.CheckButton()
        self.check_button_STPP.connect("toggled", self.glob_STPP_callback)
        self.label_STPPa = gtk.Label(" stpp")
        self.box_STPP = gtk.HBox()
        self.box_STPP.pack_start(self.label_STPP, expand=False)        
        self.box_STPP.pack_start(self.check_button_STPP, expand=False)
        self.box_STPP.pack_start(self.label_STPPa, expand=False)

        self.label_Var_STC = gtk.Label("TAC Slope")
        self.label_Var_STC.set_markup('<span color="blue"><b>TAC Slope   </b></span>')              
        self.combo_STC = gtk.combo_box_new_text()
        self.combo_STC.connect("changed", self.glob_STC_value)
        self.combo_STC.append_text("125 ns (00)")        
        self.combo_STC.append_text("250 ns (01)")
        self.combo_STC.append_text("500 ns (10)")
        self.combo_STC.append_text("1000 ns (11)")
        self.combo_STC.set_active(0) # default 125 ns
        self.label_STC = gtk.Label(" stc")
        self.box_STC = gtk.HBox()
        self.box_STC.pack_start(self.label_Var_STC, expand=False)
        self.box_STC.pack_start(self.combo_STC, expand=False)
        self.box_STC.pack_start(self.label_STC, expand=False)

        self.label_Var_SDT = gtk.Label("Threshold DAC")
        self.label_Var_SDT.set_markup('<span color="blue"><b>Threshold DAC   </b></span>')
        self.entry_SDT = gtk.Entry(max=4)
        self.entry_SDT.set_text("300")
        self.entry_SDT.connect("focus-out-event", self.glob_SDT_entry)
        self.entry_SDT.connect("activate", self.glob_SDT_entry, self.entry_SDT)
        #self.label_Var_SDTb = gtk.Label("Press Enter to SET")
        #self.label_Var_SDTb.set_markup('<span color="red"><b>  <u>PRESS &lt;ENTER&gt;</u> to SET</b></span>')        
        # self.combo_SDT = gtk.combo_box_new_text()
        # for i in range(1024):
            # self.combo_SDT.append_text(str(i))
        # self.combo_SDT.set_active(0)
        self.label_SDT = gtk.Label()
        self.box_SDT = gtk.HBox()
        self.box_SDT.pack_start(self.label_Var_SDT, expand=False)
        self.box_SDT.pack_start(self.entry_SDT, expand=False)
        #self.box_SDT.pack_start(self.combo_SDT)
        self.box_SDT.pack_start(self.label_SDT, expand=False)
        #self.box_SDT.pack_start(self.label_Var_SDTb, expand=False)

        self.label_Var_SDP_ = gtk.Label("Test Pulse DAC")
        self.label_Var_SDP_.set_markup('<span color="blue"><b>Test Pulse DAC   </b></span>')
        self.entry_SDP_ = gtk.Entry(max=4)
        self.entry_SDP_.set_text("300")
        self.entry_SDP_.connect("focus-out-event", self.glob_SDP_entry ) #,self.entry_SDP_
        self.entry_SDP_.connect("activate", self.glob_SDP_entry, self.entry_SDP_)

        #self.label_Var_SDP_b = gtk.Label("Press Enter to SET")
        #self.label_Var_SDP_b.set_markup('<span color="red"><b>  <u>PRESS &lt;ENTER&gt;</u> to SET</b></span>') 
        self.label_SDP_ = gtk.Label()
        self.box_SDP_ = gtk.HBox()
        self.box_SDP_.pack_start(self.label_Var_SDP_,expand=False)
        self.box_SDP_.pack_start(self.entry_SDP_,expand=False)
        self.box_SDP_.pack_start(self.label_SDP_,expand=False)
        #self.box_SDP_.pack_start(self.label_Var_SDP_b,expand=False)

        self.label_variable1 = gtk.Label("  \n   ")
        self.label_variable2 = gtk.Label("  \n   ")
        self.label_variable3 = gtk.Label("  \n   ")
        self.label_variable4 = gtk.Label("  \n   ") 
        self.label_variable5 = gtk.Label("   ")
        self.label_variable6 = gtk.Label("Values for Threshold and Test Pulse :") 
        self.label_variable6.set_markup('<span color="purple"><b>Values for Threshold and Test Pulse :</b></span>') 
        self.label_variable7 = gtk.Label("  \n  ")
        self.label_variable9 = gtk.Label("  \n  ") 
        self.label_variable10 = gtk.Label("  0 <= x <= 1023")
        self.label_variable11 = gtk.Label(" ")
        self.label_variable12 = gtk.Label("to Set the Values for SDT and SDP_")
        self.label_variable12.set_markup('<span color="purple">to <b>Set</b> the Values for <b>SDT</b> and <b>SDP_</b></span>')
        self.box_SDP_SDT = gtk.HBox()
        self.box_SDP_SDT.pack_start(self.label_variable6,expand=False)
        self.box_SDP_SDT.pack_start(self.label_variable10,expand=False)

        self.label_Var_SC10b = gtk.Label("10-bit Conversion Time")
        self.label_Var_SC10b.set_markup('<span color="blue"><b>10-bit Conversion Time   </b></span>')
        self.combo_SC10b = gtk.combo_box_new_text()
        self.combo_SC10b.connect("changed", self.glob_SC10b_value)
        self.combo_SC10b.append_text("0 ns (00)")
        self.combo_SC10b.append_text("1 ns (10)")
        self.combo_SC10b.append_text("2 ns (01)")
        self.combo_SC10b.append_text("3 ns (11)")
        self.combo_SC10b.set_active(0)
        self.label_SC10b = gtk.Label(" sc10b")
        self.box_SC10b = gtk.HBox()
        self.box_SC10b.pack_start(self.label_Var_SC10b, expand=False)
        self.box_SC10b.pack_start(self.combo_SC10b, expand=False)
        self.box_SC10b.pack_start(self.label_SC10b, expand=False)

        self.label_Var_SC8b = gtk.Label("8-bit Conversion Time")
        self.label_Var_SC8b.set_markup('<span color="blue"><b>8-bit Conversion Time   </b></span>')
        self.combo_SC8b = gtk.combo_box_new_text()
        self.combo_SC8b.connect("changed", self.glob_SC8b_value)
        self.combo_SC8b.append_text("0 ns (00)")
        self.combo_SC8b.append_text("1 ns (10)")
        self.combo_SC8b.append_text("2 ns (01)")
        self.combo_SC8b.append_text("3 ns (11)")
        self.combo_SC8b.set_active(3) # default is 3 ns
        self.label_SC8b = gtk.Label(" sc8b")
        self.box_SC8b = gtk.HBox()
        self.box_SC8b.pack_start(self.label_Var_SC8b, expand=False)
        self.box_SC8b.pack_start(self.combo_SC8b, expand=False)
        self.box_SC8b.pack_start(self.label_SC8b, expand=False)

        self.label_Var_SC6b = gtk.Label("6-bit Conversion Time")
        self.label_Var_SC6b.set_markup('<span color="blue"><b>6-bit Conversion Time   </b></span>')
        self.combo_SC6b = gtk.combo_box_new_text()
        self.combo_SC6b.connect("changed", self.glob_SC6b_value)
        self.combo_SC6b.append_text("0 ns (000)")
        self.combo_SC6b.append_text("1 ns (100)")
        self.combo_SC6b.append_text("2 ns (010)")
        self.combo_SC6b.append_text("3 ns (110)")
        self.combo_SC6b.append_text("4 ns (001)")
        self.combo_SC6b.append_text("5 ns (101)")
        self.combo_SC6b.append_text("6 ns (011)")
        self.combo_SC6b.append_text("7 ns (111)")
        self.combo_SC6b.set_active(0)
        self.label_Var_SC6ba = gtk.Label(" sc6b")
        self.box_SC6b = gtk.HBox()
        self.box_SC6b.pack_start(self.label_Var_SC6b, expand=False)
        self.box_SC6b.pack_start(self.combo_SC6b, expand=False)
        self.box_SC6b.pack_start(self.label_Var_SC6ba, expand=False)

        self.label_S6b = gtk.Label("6-bit ADC Enable")
        self.label_S6b.set_markup('<span color="blue"><b>6-bit ADC Enable   </b></span>')
        self.check_button_S6b = gtk.CheckButton()   
        self.check_button_S6b.connect("toggled", self.glob_S6b_callback)
        self.check_button_S6b.set_active(False)
        self.label_S6ba = gtk.Label("Disables 8 & 10 bit ADC")
        self.label_S6ba.set_markup('<span color="blue"><b>  (Disables 8 &amp; 10 bit ADC)</b></span>')
        self.label_S6bb = gtk.Label(" s6b")
        self.box_S6b = gtk.HBox()
        self.box_S6b.pack_start(self.label_S6b, expand=False)
        self.box_S6b.pack_start(self.check_button_S6b, expand=False)
        self.box_S6b.pack_start(self.label_S6ba, expand=False)
        self.box_S6b.pack_start(self.label_S6bb, expand=False)

        self.label_Var_S8b = gtk.Label("8-bit ADC Mode")
        self.label_Var_S8b.set_markup('<span color="blue"><b>8-bit ADC Mode   </b></span>')
        self.combo_S8b = gtk.CheckButton()
        self.combo_S8b.connect("toggled", self.glob_S8b_callback)
        self.combo_S8b.set_active(1)
        self.label_Var_S8ba = gtk.Label(" s8b")
        self.box_S8b = gtk.HBox()
        self.box_S8b.pack_start(self.label_Var_S8b, expand=False)
        self.box_S8b.pack_start(self.combo_S8b, expand=False)
        self.box_S8b.pack_start(self.label_Var_S8ba, expand=False)

        self.label_Var_SPDC = gtk.Label("ADCs Enable")
        self.label_Var_SPDC.set_markup('<span color="blue"><b>ADCs Enable   </b></span>')
        self.button_SPDC = gtk.CheckButton()
        self.button_SPDC.connect("toggled", self.glob_SPDC_callback)
        self.button_SPDC.set_active(1)
        self.label_Var_SPDCa = gtk.Label(" spdc")
        self.box_SPDC = gtk.HBox()
        self.box_SPDC.pack_start(self.label_Var_SPDC, expand=False)
        self.box_SPDC.pack_start(self.button_SPDC, expand=False)
        self.box_SPDC.pack_start(self.label_Var_SPDCa, expand=False)

        self.label_SDCKS = gtk.Label("Dual Clock Edge\nSerialized Data Enable\n")    
        self.label_SDCKS.set_markup('<span color="blue"><b>Dual Clock Edge\nSerialized Data Enable\n   </b></span>')
        self.check_button_SDCKS = gtk.CheckButton()
        self.check_button_SDCKS.connect("toggled", self.glob_SDCKS_callback)
        self.label_SDCKSa = gtk.Label(" sdcks")
        self.box_SDCKS = gtk.HBox()
        self.box_SDCKS.pack_start(self.label_SDCKS, expand=False)        
        self.box_SDCKS.pack_start(self.check_button_SDCKS, expand=False)
        self.box_SDCKS.pack_start(self.label_SDCKSa, expand=False)

        self.label_SDCKA = gtk.Label("Dual Clock Edge\nSerialized ART Enable\n")    
        self.label_SDCKA.set_markup('<span color="blue"><b>Dual Clock Edge\nSerialized ART Enable\n   </b></span>')
        self.check_button_SDCKA = gtk.CheckButton()
        self.check_button_SDCKA.connect("toggled", self.glob_SDCKA_callback)
        self.label_SDCKAa = gtk.Label(" sdcka")
        self.box_SDCKA = gtk.HBox()
        self.box_SDCKA.pack_start(self.label_SDCKA, expand=False)        
        self.box_SDCKA.pack_start(self.check_button_SDCKA, expand=False)
        self.box_SDCKA.pack_start(self.label_SDCKAa, expand=False)

        self.label_SDCK6b = gtk.Label("Dual Clock Edge\nSerialized 6-bit Enable\n")    
        self.label_SDCK6b.set_markup('<span color="blue"><b>Dual Clock Edge\nSerialized 6-bit Enable\n    </b></span>')
        self.check_button_SDCK6b = gtk.CheckButton()
        self.check_button_SDCK6b.connect("toggled", self.glob_SDCK6b_callback)
        self.label_SDCK6ba = gtk.Label(" sdck6b")
        self.box_SDCK6b = gtk.HBox()
        self.box_SDCK6b.pack_start(self.label_SDCK6b, expand=False)        
        self.box_SDCK6b.pack_start(self.check_button_SDCK6b, expand=False)
        self.box_SDCK6b.pack_start(self.label_SDCK6ba, expand=False)

        self.label_SDRV = gtk.Label("Tristates Analog Outputs")    
        self.label_SDRV.set_markup('<span color="blue"><b>Tristates Analog Outputs   </b></span>')
        self.check_button_SDRV = gtk.CheckButton()
        self.check_button_SDRV.connect("toggled", self.glob_SDRV_callback)
        self.check_button_SDRV.set_active(0)
        self.label_SDRVa = gtk.Label(" sdrv")
        self.box_SDRV = gtk.HBox()
        self.box_SDRV.pack_start(self.label_SDRV, expand=False)        
        self.box_SDRV.pack_start(self.check_button_SDRV, expand=False)
        self.box_SDRV.pack_start(self.label_SDRVa, expand=False)

        self.box_var_labels = gtk.VBox()
        self.box_var_labels.set_border_width(10)
        self.box_var_labels.pack_start(self.label_variable1)
        self.box_var_labels.pack_start(self.label_variable2)
        self.box_var_labels.pack_start(self.label_variable3)
        self.frame_qs = gtk.Frame()
        self.frame_qs.set_shadow_type(gtk.SHADOW_OUT)
        self.frame_qs.set_label("QUICK SET")
        self.frame_qs.set_label_align(0.5,0.0)
        self.box_quick_set = gtk.VBox(homogeneous=False,spacing=0)
        self.box_quick_set.set_border_width(20)
        self.qs_label = gtk.Label("QUICK SET")
        self.qs_label.set_markup('<span color="blue"><b>Tristates Analog Outputs   </b></span>')
        self.box_quick_set.pack_start(self.qs_table)
        #self.box_quick_set.pack_end(self.button_quick_set)                
        self.frame_qs.add(self.box_quick_set)

        self.label_But_Space6 = gtk.Label(" ")
        self.label_But_Space7 = gtk.Label(" ")

        self.box_variables = gtk.VBox()
        self.box_variables.set_border_width(5)
        self.box_variables.pack_start(self.box_Global, expand=False)
        self.box_variables.pack_start(self.label_But_Space6, expand=False)
        self.box_variables.pack_start(self.label_But_Space7, expand=False)
        self.box_variables.pack_start(self.box_SPG, expand=False)
        self.box_variables.pack_start(self.box_SDP, expand=False)
        self.box_variables.pack_start(self.box_SBMX, expand=False)
        self.box_variables.pack_start(self.box_SBXX, expand=False)
        self.box_variables.pack_start(self.box_SLG, expand=False)
        self.box_variables.pack_start(self.box_SCMX, expand=False)
        self.box_variables.pack_start(self.box_SFAM, expand=False)
        self.box_variables.pack_start(self.box_ST, expand=False)
#        self.box_variables.pack_start(self.box_DC, expand=False)
        self.box_variables.pack_start(self.box_SFM, expand=False)

        self.box_variables.pack_start(self.box_SG, expand=False)
        self.box_variables.pack_start(self.box_SNG, expand=False)
        self.box_variables.pack_start(self.box_STXX, expand=False)

        self.box_variables.pack_start(self.box_SSH, expand=False)
        self.box_variables.pack_start(self.box_STC, expand=False)

        self.box_variables.pack_start(self.box_SC10b, expand=False)
        self.box_variables.pack_start(self.box_S8b, expand=False)
        self.box_variables.pack_start(self.box_SC8b, expand=False)
        self.box_variables.pack_start(self.box_S6b, expand=False)
        self.box_variables.pack_start(self.box_SC6b, expand=False)
        self.box_variables.pack_start(self.box_SPDC, expand=False)
        
        self.box_variables.pack_start(self.box_SDCKS, expand=False)
        self.box_variables.pack_start(self.box_SDCKA, expand=False)
        self.box_variables.pack_start(self.box_SDCK6b, expand=False)
        self.box_variables.pack_start(self.box_SDRV, expand=False)
        self.box_variables.pack_start(self.box_STPP, expand=False)

        self.box_variables.pack_start(self.label_variable5,expand=False)
        self.box_variables.pack_start(self.label_variable11,expand=False)
        self.box_variables.pack_start(self.box_SDT,expand=False)
        self.box_variables.pack_start(self.box_SDP_,expand=False)
        self.box_variables.pack_start(self.box_SDP_SDT,expand=False)
        #self.box_variables.pack_start(self.label_variable12,expand=False)
        self.box_variables.pack_start(self.label_variable9)
        self.box_variables.pack_end(self.frame_qs,expand=False) 



                                
        #################################################
        ###################                 #############
        ################### CHANNELS FRAMES #############   
        ###################                 #############   
        #################################################
        
        self.frame_2_a = gtk.Frame()
        self.frame_2_a.set_border_width(4)
        self.frame_2_a.set_shadow_type(gtk.SHADOW_IN)   
        self.box_channels_1a = gtk.VBox(homogeneous=False,spacing=0)
        self.box_channels_a = gtk.VBox(homogeneous=True,spacing=0)
        for ch_num in range(32):
            self.box_channels_a.pack_start(self.chan_list[ch_num].channel_box)

        self.box_channels_1a.pack_start(self.box_chan_labels_a,expand=False)        
        self.box_channels_1a.pack_start(self.box_channels_a,expand=False)
        self.frame_2_a.add(self.box_channels_1a)

        self.frame_2_b = gtk.Frame()
        self.frame_2_b.set_border_width(4)
        self.frame_2_b.set_shadow_type(gtk.SHADOW_IN)

        self.box_channels_1b = gtk.VBox(homogeneous=False,spacing=0)

        self.box_channels_b = gtk.VBox(homogeneous=True,spacing=0)

        for ch_num in range(32, 64):
            self.box_channels_b.pack_start(self.chan_list[ch_num].channel_box)

        self.box_channels_1b.pack_start(self.box_chan_labels_b,expand=False)        
        self.box_channels_1b.pack_start(self.box_channels_b,expand=False)
        self.frame_2_b.add(self.box_channels_1b)

        self.box_all_channels = gtk.HBox()
        self.box_all_channels.pack_start(self.frame_2_a)
        self.box_all_channels.pack_start(self.frame_2_b)

