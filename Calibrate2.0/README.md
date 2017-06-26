# Calibration 2.0 #
An updated TDO calibration algorithm + some calibration helper scripts


## Motivation
Say you have a bunch of .root files created by the calibration GUI and you 
want to extract the calibration coefficients for every channel on every VMM on every board. This folder contains code which streamlines that process. 

These scripts use Chris Rogan's xADC/PDO calibration algorithm and Jonah's TDO calibration algorithm. All scripts in this folder include guidance on how to use them that can be accessed via `python script.py -h`

## Scripts
*`manager.py` - This script runs the PDO and TDO calibration algorithms. For instance, the command `python manager.py TDO TDO_output_direc/new_calib TDO_bench_data.root` will calibrate the channels in TDO_bench_data.root using Jonah's TDO algorithm, then store the results in TDO_output_direc/new_calib.root and TDO_output_direc/new_calib.dat. Similarly, `python manager.py PDO PDO_output_direc/new_calib xADC_bench_data.root PDO_bench_data.root` will calibrate the channels in `xADC_bench_data.root` and `PDO_bench_data.root` then store the results in `PDO_output_direc/new_calib.root` and `PDO_output_direc/new_calib.dat`. The .dat and .root output files store the same information but in different formats.

*`run_scripts.py` - An example of how to automate the procedure of running manager.py on several bench files (useful if you ever need to calibrate every board using every board's most recent bench data).

*`TDO_PDO_calibration_scripts/` - This folder contains two helper scripts and three scripts which run the new TDO calibration algorithm.  
  *The TDO calibration scripts are `Fit_TDO.py`, `Calibrate_TDO.py`, and `TDO_dat_to_root.py`. `Fit_TDO.py` preprocesses the information from bench data to get ready for tensorflow, `Calibrate_TDO.py` runs the calibration algorithm, and finally `TDO_dat_to_root.py` writes the results from the algorithm in .root format.
  *The first helper script is `PDOroot_to_PDOdat.py`. This script translates PDO calibration .root files to the .dat format Paulo likes. 
  *The second helper is `plot_TDO.py`. `plot_TDO.py` is a template script for plotting TDO calibrations. In its current configuration, it searches through calibration data, identifies channels with high sigma, then displays the TDO calibration the algorithm found for those channels.

## Example Usage
1. Make Chris's calibration code:   
`cd ANALYSIS`  
`make`  
2. cd to Calibration2.0 and make a directory to house the new calibration data we're about to create:   
`cd ../Calibration2.0`  
`mkdir first_calibrate`  
3. Calibrate PDO (one command):  
`python manager.py PDO first_calibrate/board102_PDO_calib ../DATA/xADC_Jun9/board102_bench_xADC.root ../DATA/PDO_Jun9/board102_bench_PDO.root`  
4. Calibrate TDO (one command):   
`python manager.py TDO first_calibrate/board102_TDO_calib ../DATA/TDO_Jun9/board102_bench_TDO.root`  
5. Check the outlier TDO calibrations (press `Enter` to iterate):  
`python TDO_PDO_calibration_scripts/plot_TDO.py first_calibrate/board102_TDO_calib`  

## Requirements and Notes
1. PDO calibration takes 1 minute / board. TDO calibration takes about 15 minutes / board .
2. manager.py probably only works on OS X. 
3. Your system's default python needs access to the `tensorflow` and `rootpy` packages. Both packages can be installed with pip. You also need `tqdm`! `tqdm` is a great package which displays progress bars. I include a progress bar in the Calibrate_TDO.py script since the TDO algorithm takes so long.
4. The directory from which you run manager.py cannot have any files that start with 'ephem' in it. The reason is that a few "ephemeral" files are made during TDO and PDO calibration and they all start with "ephem". manager.py includes an assertion error to check for these cases.
5. Definitions for the variables output by the new TDO calibration are below:  


| Tables        | Are           | Cool  |
| ------------- |:-------------:| -----:|
| col 3 is      | right-a       | $1600 |
| col 2 is      | centered      |   $12 |
| zebra stripes | are neat      |    $1 |

\*
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
\*
---

Hopefully this all works!  
-Jonah
