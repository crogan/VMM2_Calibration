#!/usr/bin/env python26

#    by Charlie Armijo, Ken Johns, Bill Hart, Sarah Jones, James Wymer, Kade Gigliotti
#    Experimental Elementary Particle Physics Laboratory
#    Physics Department
#    University of Arizona    
#    armijo at physics.arizona.edu
#    johns at physics.arizona.edu
#
#    This is version 1 of the MMFE8 calibration routine GUI



import pygtk
pygtk.require('2.0')
import gtk
import gobject

############################################################################
############################################################################
##########################                     #############################
##########################   LOOP_PAIR CLASS   #############################
##########################                     #############################
############################################################################
############################################################################

class loop_pair(gobject.GObject):

    
    def button_block(self, widget, button):
        button.set_sensitive(False)
        if type(button) is gtk.Entry:
            button.set_visibility(False)

    def button_unblock(self, widget, button):
        button.set_sensitive(True)
        if type(button) is gtk.Entry:
            button.set_visibility(True)

    def button_gate_unblock(self, widget, gate, button):
        if gate.get_active():
            button.set_sensitive(True)
            if type(button) is gtk.Entry:
                button.set_visibility(True)
        else:
            button.set_sensitive(False)
            if type(button) is gtk.Entry:
                button.set_visibility(False)

    def toggle_active(self, widget, button):
        button.set_active(True)

    def toggle_inactive(self, widget, button):
        button.set_active(False)

    def send_fix(self, widget):
        self.emit("fix_signal")

    def send_loop(self, widget):
        self.emit("loop_signal")
        
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #             __init__  
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    def __init__(self, title, fix_buttons, loop_buttons):
        self.__gobject_init__()
        
        self.frame     = gtk.Frame()
        #self.frameFix  = gtk.Frame()
        #self.frameLoop = gtk.Frame()

        map = self.frame.get_colormap() 
        selected_color = map.alloc_color("DarkGreen")
        disabled_color = map.alloc_color("lavender")
        disabledtxt_color = map.alloc_color("RoyalBlue")
        hover_color = map.alloc_color("honeydew")
        frame_color = map.alloc_color("white")

        style_frame = self.frame.get_style().copy()
        style_frame.bg[gtk.STATE_PRELIGHT] = hover_color
        style_frame.bg[gtk.STATE_NORMAL]   = frame_color
        style_frame.fg[gtk.STATE_PRELIGHT] = selected_color
        style_frame.fg[gtk.STATE_NORMAL]   = disabledtxt_color
        style_frame.fg[gtk.STATE_ACTIVE]   = frame_color

        self.frame.set_style(style_frame)

        self.buttons_frame = gtk.VBox()
        self.buttons_frame.set_spacing(4)
        self.buttons_frame.set_border_width(4)
        self.box_frame = gtk.EventBox()
        self.box_frame.add(self.buttons_frame)
        self.buttons      = gtk.HBox()
        self.buttonsFix   = gtk.VBox()
        self.buttonsLoop  = gtk.VBox()
        self.buttonsFix.set_spacing(4)
        self.buttonsFix.set_border_width(2)
        self.buttonsLoop.set_spacing(4)
        self.buttonsLoop.set_border_width(2)
        
        self.buttonsLoop.set_style(style_frame)
        self.box_frame.set_style(style_frame)

        self.box_buttons = gtk.EventBox()
        self.box_buttons.add(self.buttons)
        self.box_buttons.set_style(style_frame)

        self.frame.add(self.box_frame)

        # frame title
        title = '<span color="navy" size="large"><b>'+title+'</b></span>'
        self.title_label = gtk.Label("Title")
        self.title_label.set_markup(title)
        self.title_label.set_justify(gtk.JUSTIFY_CENTER)
        self.title_box = gtk.EventBox()
        self.title_box.add(self.title_label)
        self.title_box.set_style(style_frame)

        self.buttons_frame.pack_start(self.title_box,expand=True)
        self.buttons_frame.pack_start(self.box_buttons,expand=True)
        self.buttons.pack_start(self.buttonsFix,expand=True)
        self.buttons.pack_end(self.buttonsLoop,expand=True)

        self.button_Fix  = gtk.ToggleButton(" Fix Parameter ")
        self.button_Loop = gtk.ToggleButton("Loop Parameter")
        self.button_Fix.connect("clicked", self.send_fix)
        self.connect('fix_signal', self.toggle_inactive, self.button_Loop)
        self.connect('fix_signal', self.button_block, self.button_Fix)
        self.button_Loop.connect("clicked", self.send_loop)
        self.connect('loop_signal', self.toggle_inactive, self.button_Fix)
        self.connect('loop_signal', self.button_block, self.button_Loop)
        self.connect('loop_signal', self.button_unblock, self.button_Fix)
        self.connect('fix_signal', self.button_unblock, self.button_Loop)
        self.button_Fix.clicked();
        
        self.box_Fix = gtk.EventBox()
        self.box_Loop = gtk.EventBox()
        self.box_Fix.add(self.button_Fix)
        self.box_Loop.add(self.button_Loop)
        self.box_Fix.set_size_request(225,-1)
        self.box_Loop.set_size_request(225,-1)

        style_toggle = self.button_Fix.get_style().copy()
        style_button = style_toggle.copy()
        style_toggle.bg[gtk.STATE_PRELIGHT]   = hover_color
        style_toggle.base[gtk.STATE_PRELIGHT]   = hover_color
        style_toggle.fg[gtk.STATE_PRELIGHT] = selected_color
        style_toggle.text[gtk.STATE_PRELIGHT] = selected_color
        style_toggle.bg[gtk.STATE_NORMAL]     = disabled_color
        style_toggle.base[gtk.STATE_NORMAL]     = disabled_color
        style_toggle.fg[gtk.STATE_NORMAL]   = disabledtxt_color
        style_toggle.text[gtk.STATE_NORMAL]   = selected_color
        style_toggle.bg[gtk.STATE_ACTIVE]     = selected_color
        style_toggle.base[gtk.STATE_ACTIVE]     = selected_color
        style_toggle.fg[gtk.STATE_ACTIVE]   = frame_color
        style_toggle.text[gtk.STATE_ACTIVE]   = frame_color
        style_toggle.bg[gtk.STATE_INSENSITIVE]     = selected_color
        style_toggle.base[gtk.STATE_INSENSITIVE]     = selected_color
        style_toggle.fg[gtk.STATE_INSENSITIVE]   = frame_color
        style_toggle.text[gtk.STATE_INSENSITIVE]   = frame_color
        style_button.bg[gtk.STATE_PRELIGHT]   = hover_color
        style_button.base[gtk.STATE_PRELIGHT]   = hover_color
        style_button.fg[gtk.STATE_PRELIGHT] = selected_color
        style_button.text[gtk.STATE_PRELIGHT] = selected_color
        style_button.bg[gtk.STATE_NORMAL]     = disabled_color
        style_button.base[gtk.STATE_NORMAL]     = hover_color
        style_button.fg[gtk.STATE_NORMAL]   = selected_color
        style_button.text[gtk.STATE_NORMAL]   = selected_color
        style_button.bg[gtk.STATE_ACTIVE]     = selected_color
        style_button.base[gtk.STATE_ACTIVE]     = selected_color
        style_button.fg[gtk.STATE_ACTIVE]   = frame_color
        style_button.text[gtk.STATE_ACTIVE]   = frame_color
        style_button.bg[gtk.STATE_INSENSITIVE]     = disabled_color
        style_button.base[gtk.STATE_INSENSITIVE]     = disabled_color
        style_button.fg[gtk.STATE_INSENSITIVE]   = disabledtxt_color
        style_button.text[gtk.STATE_INSENSITIVE]   = disabledtxt_color
        
        self.box_Fix.set_style(style_frame)
        self.box_Loop.set_style(style_frame)
        self.button_Fix.set_style(style_toggle)
        self.button_Loop.set_style(style_toggle)
        self.button_Fix.get_child().set_style(style_toggle)
        self.button_Loop.get_child().set_style(style_toggle)

        self.buttonsFix.pack_start(self.box_Fix,expand=False)
        self.buttonsLoop.pack_start(self.box_Loop,expand=False)

        fixlist = type(fix_buttons) is list
        if not fixlist:
            fix_buttons = [fix_buttons]
        else:
            self.fix_radio = []
        looplist = type(loop_buttons) is list
        if not looplist:
            loop_buttons = [loop_buttons]
        else:
            self.loop_radio = []
            
        i = 0
        for button in fix_buttons:
            button.set_style(style_button)
            if type(button) is gtk.Entry:
                button_label = gtk.Label("Label")
                label = '<span color="navy"><b> value (int) </b></span>'
                button_label.set_markup(label)
                button_box = gtk.HBox()
                button_box.set_style(style_button)
                button_box.pack_start(button_label,expand=True)
                button_box.pack_end(button,expand=True)
            else:
                button_box = gtk.EventBox()
                button_box.add(button)
                button_box.set_style(style_frame)
            self.connect('loop_signal', self.button_block, button)
            if fixlist:
                if i is 0:
                    self.fix_radio += [gtk.RadioButton()]
                else:
                    self.fix_radio += [gtk.RadioButton(self.fix_radio[0])]
                self.fix_radio[i].set_style(style_button)
                self.connect('loop_signal',self.button_block,self.fix_radio[i])
                self.connect('fix_signal',self.button_unblock,self.fix_radio[i])
                self.connect('fix_signal',self.button_gate_unblock,self.fix_radio[i],button)
                self.fix_radio[i].connect("clicked",self.button_gate_unblock,self.fix_radio[i],button)
                radio_box = gtk.HBox()
                radio_box.set_style(style_button)
                radio_box.pack_start(self.fix_radio[i],expand=False)
                radio_box.pack_start(button_box,expand=False)
                self.buttonsFix.pack_start(radio_box,expand=False)
                self.fix_radio[i].set_active(True)
            else:
                self.connect('fix_signal', self.button_unblock, button)
                self.buttonsFix.pack_start(button_box,expand=False)
            i += 1

        i = 0
        for button in loop_buttons:
            button.set_style(style_button)
            if type(button) is gtk.Entry:
                button_label = gtk.Label("Label")
                label = '<span color="navy"><b>values (int,int,...) </b></span>'
                button_label.set_markup(label)
                button_box = gtk.HBox()
                button_box.set_style(style_button)
                button_box.pack_start(button_label,expand=True)
                button_box.pack_end(button,expand=True)
            else:
                button_box = gtk.EventBox()
                button_box.add(button)
                button_box.set_style(style_frame)
            self.connect('fix_signal', self.button_block, button)
            if looplist:
                if i is 0:
                    self.loop_radio += [gtk.RadioButton()]
                else:
                    self.loop_radio += [gtk.RadioButton(self.loop_radio[0])]
                self.loop_radio[i].set_style(style_button)
                self.connect('fix_signal',self.button_block,self.loop_radio[i])
                self.connect('loop_signal',self.button_unblock,self.loop_radio[i])
                self.connect('loop_signal',self.button_gate_unblock,self.loop_radio[i],button)
    
                radio_box = gtk.HBox()
                radio_box.set_style(style_button)
                radio_box.pack_start(self.loop_radio[i],expand=False)
                radio_box.pack_start(button_box,expand=False)
                self.buttonsLoop.pack_start(radio_box,expand=False)
                self.loop_radio[i].set_active(True)
            else:
                self.connect('loop_signal', self.button_unblock, button)
                self.buttonsLoop.pack_start(button_box,expand=False)
            i += 1
        if looplist:
            i = 0
            for b in loop_buttons:
                for r in self.loop_radio:
                    r.connect("clicked",self.button_gate_unblock,self.loop_radio[i],b)
                i += 1
            
        self.button_Fix.clicked();
      
            
        
gobject.type_register(loop_pair)
gobject.signal_new("fix_signal", loop_pair, gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ())
gobject.signal_new("loop_signal", loop_pair, gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ())
