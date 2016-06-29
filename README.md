# VMM2_Calibration #

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

	cmd> python GUI/mmfe8_CalibRoutine.py

From this gui you can take each of the three types of measurements,
each performing variations on different quantities and measuring the
VMM response:

### Step 1a: Collect xADC calibration data

### Step 1b: Collect PDO calibration data

### Step 1c: Collect TDO calibration data

## Step 2: Calibrate the charge response of the test pulse


## Step 3: Calibrate the PDO response

## Step 4: Calibrate the TDO response

## Step 5: Use your calibrations in analysis

