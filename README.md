# VMM2 Calibration #

Provides a framework for calibrating the time and amplitude output of
VMM2 in the context of MMFE8 boards

## How to calibrate ##

There are several steps to calibrating the VMM's:

## Step 1: Take calibration data

First you must take calibration data for the VMM's, measuring the xADC
response to test pulses, and then varying the test pulse DAC/delay
time and looking at the corresponding PDO/TDO measurements. There are
three different types of calibration data you will need, all of which
can be collected by running the calibration gui contained in the `GUI`
folder. To launch it, run:

	cmd_line$> python GUI/mmfe8_CalibRoutine.py

From this gui you can take each of the three types of measurements,
each performing variations on different quantities and measuring the
VMM response:

### Step 1a: Collect xADC calibration data

### Step 1b: Collect PDO calibration data

### Step 1c: Collect TDO calibration data

## Step 2: Use the collected data to determine calibrations

Once you have collected calibration data for a MMFE8 board(s) you can
now use the code in the `ANALYSIS` folder to determine calibrations
for each of the VMM's and channels.

NOTE: since each MMFE8 is assigned
an ID which is written in the data, you can combine all of the
`*.root` files produced in step 1 together and process them all at
once. This is recommended so that all of the calibration information
is consolidated in the same place. For example, if you have several
files from the xADC calibration data step 1a named `xADC_board_0.root,
xADC_board_1.root, ...` etc., you can combine them into one file to
use for all the following steps:

	cmd_line$> hadd xADC_allboards.root xADC_board_*.root

You can perform this combination with any of the intermediate `*.root`
files produced in the following steps, or with the final `*.root`
files containing the final calibration information.

In order to run the following steps, you must first compile the
analysis code in the `ANALYSIS` folder. This can be done by doing:

	cmd_line$> cd ANALYSIS
	cmd_line$> make

This will produce the executables `Fit_xADC`, `Calibrate_xADC`,
`Fit_PDO`, `Calibrate_PDO`, `Fit_TDO`, and `Calibrate_TDO`, which
are used in the following steps.

### Step 2a: Calibrate the charge response of the test pulse

Using the `*.root` file(s) produced in step 1a, you must now convert
this raw data into a consolidated format which can be used by the
calibration classes (described in step 3) on actual data. An example
data file, in the same format as the output of step 1a, is provided at
`DATA/xADC/xADC_example.root` and is used an example below.

Processing this raw data is a two-step process (as are the PDO and TDO
calibrations described in steps 2b and 2c). First, fits are performed
for each of the xADC measurements with varying test pulse DAC values
in order to determine the injected charge. This is done by doing

	cmd_line$> ./Fit_xADC xADC_example.root -o xADC_fit.root

The executable will produce a new root file with the name
`xADC_fit.root`. Inside the output file are two folders with plots of
the input data and the fitted distribution for each of the
VMM's.

NOTE: you can graphically access the contents of this output
file (and all of the outputs from step 2a-2c) using the ROOT
`TBrowser` inferface. In order to have the correct/pretty plot
formatting you must initialize the same plotting style as was used
when making the plot canvases. You can do this by doing:

	cmd_line$> root
	root [0] .x include/setstyle.hh
	root [1] TBrowser b

You can then click on the `xADC_fit.root` file (or any file), and
click through the folders and canvases.

In `xADC_fit.root` there are two folders containing plots. `xADC_plots`
included plots of the measured xADC values for each of the test pulse
DAC values included in the input file, for each VMM
included. `xADCfit_plots` has the same distributions, except now with
the fitted functions overlayed on the plots.

In the output file, there are also two `TTree` objects, `xADC_data`
and `xADC_fit`. The first is a copy of the `TTree` provided in the
input file while the second contains the parameters extracted from the
fits which will be used below.

Next, the extracted charge values, as a function of test pulse DAC,
are fit to create a calibration curve which can be used to convert DAC values
to charges for each of the VMM's. This is done by doing:

	cmd_line$> ./Calibrate_xADC xADC_fit.root -o xADC_calib.root

Notice that now the input file is `xADC_fit.root`, the one produced
above. The new output file, `xADC_calib.root` should be saved - this
now contains all the calibration information for these VMM's.

Inside `xADC_calib.root` are three `TTree` objects: `xADC_data`
and `xADC_fit`, which are copies from the input file, and
`xADC_calib`, which contains function parameters containing the DAC to
charge calibration information. There are also two folders containing
plots, `xADCfit_plots` and `xADCcalib_plots`. The second contains
canvases of all of the fits produced by the `Calibrate_xADC`
executable.

You can use this file as input to a `DACToCharge` class object,
described in step 3, to provide charges as a function of DAC values in
your analysis. You will also need this file when calibrating the PDO
charge response in step 2b.

### Step 2b: Calibrate the PDO response

As with the on-board xADC calibration from step 2a, the PDO
calibration is a two-step process from the command line. For the
instructions below, and example input file is provided, 
`DATA/TP/PDO_example.root`, and corresponds to the output format of
the calibration gui in step 1b. NOTE: the PDO_example.root file
currently included in this package contains data collected with a
board connected to a chamber, which resulted in noise on VMM's 0 and
1, causing their ouput to be largely non-sensical - you should ignore these.

First, do:

	cmd_line$> ./Fit_PDO PDO_example.root -o PDO_fit.root

This creates the file `PDO_fit.root`, containing the extracted means
and spreads of the input PDO distributions, for each channel included
in input. You can look at these distributions in the `PDO_plots`
folder contained in the file. NOTE: this file will not contain
information for any channels that are missing (or dead).

Next, do:

	cmd_line$> ./Calibrate_PDO PDO_fit.root -x xADC_calib.root -o
    PDO_calib.root

Notice that you must also provide the xADC calibration information
contained in a file like `xADC_calib.root` through the `-x` flag. The
creation of such a file is described in step 2a.

The created output file `PDO_calib.root` contains several folders of
figures, summarizing the input data and fits performed. You should
save this file as it contains all the PDO calibration information for
use in data analysis (see step 3). 

### Step 2c: Calibrate the TDO response



## Step 3: Use your calibrations in analyses

