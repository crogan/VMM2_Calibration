# Calibration 2.0 #
__MMFE8 PDO/TDO calibration with an updated TDO calibration algorithm__


## Motivation
Say you have calibration data for several MMFE8s and you 
want to extract the calibration coefficients for every channel on every VMM on every board. This folder contains code which streamlines that process. 

These scripts use Chris Rogan's xADC/PDO calibration algorithm and Jonah's TDO calibration algorithm. All scripts in this folder include guidance on how to use them that can be accessed via `python script.py -h`

## Scripts
- `manager.py` - This script runs the PDO and TDO calibration algorithms. For instance, the command `python manager.py TDO TDO_output_direc/new_calib TDO_bench_data.root` will calibrate the channels in TDO_bench_data.root using Jonah's TDO algorithm, then store the results in TDO_output_direc/new_calib.root and TDO_output_direc/new_calib.dat. Similarly, `python manager.py PDO PDO_output_direc/new_calib xADC_bench_data.root PDO_bench_data.root` will calibrate the channels in `xADC_bench_data.root` and `PDO_bench_data.root` then store the results in `PDO_output_direc/new_calib.root` and `PDO_output_direc/new_calib.dat`. The .dat and .root output files store the same information but in different formats.

- `run_scripts.py` - An example of how to automate the procedure of running manager.py on several bench files (useful if you ever need to calibrate every board using every board's most recent bench data).

- `TDO_PDO_calibration_scripts/` - This folder contains two helper scripts and three scripts which run the new TDO calibration algorithm.  
  * The TDO calibration scripts are `Fit_TDO.py`, `Calibrate_TDO.py`, and `TDO_dat_to_root.py`. `Fit_TDO.py` preprocesses the information from bench data to get ready for tensorflow, `Calibrate_TDO.py` runs the calibration algorithm, and finally `TDO_dat_to_root.py` writes the results from the algorithm in .root format.
  * The first helper script is `PDOroot_to_PDOdat.py`. This script translates PDO calibration .root files to the .dat format Paulo likes. 
  * The second helper is `plot_TDO.py`. `plot_TDO.py` is a template script for plotting TDO calibrations. In its current configuration, it searches through calibration data, identifies channels with high sigma, then displays the TDO calibration the algorithm found for those channels.

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
5. Although the older TDO calibration scripts were able to operate on the `hadd` of several boards, __the new TDO calibration algorithm can only operate on one board's bench file at a time__. Do not `hadd` before feeding to manager.py. However, you should definitely `hadd` all of outputs of manager.py once you've ran it on every board individually. 
6. Definitions for the variables output by the new TDO calibration algorithm are below:  

| Variable | Description |
|:---------|:--------------------------------------------------------------------------------------|
|MMFE8    |Last three digits of the MMFE8's IP Address                                            |
|VMM      |VMM number, 0-indexed                                                                   |
|CH       |Channel number, 1-indexed                                                               |
|Gain     |TDO = time (ns) * Gain + Pedestal. Units: (TDO counts)/ns                      |
|Pedestal |TDO = time (ns) * Gain + Pedestal. Units: TDO counts                   |
|m        |Slope of fitted fitted sawtooth wave. Units: (TDO counts)/(Delay index)             |
|b        |Y-intercept of fitted sawtooth wave. Units: TDO counts                                 |
|floor    |The lower bound on TDO for this channel, AKA the TDO counts corresponding to 25/2 ns                |
|n_samps  |The number of data points available during training                                            |
|p_8      |The fraction of TDO on this channel which were a multiple of 8. This variable will hopefully lead us to a better understanding of the mysterious VMM Lower Bit Issue.|
|sigma    |Standard error for time prediction TDO = m*Delay + b on this channel. Noisy channels will have high sigma.|
|chi2     |Sum of squared differences. Included for compatibility with crogan's TDO_to_time function.                  |
|prob     |Probability of fit given above chi2. Not meaningful since we don't know the actual variance in our data. Included for compatibility with crogan's TDO_to_time function.|
|delta_b  |Standard error on the calibration value found for b                                    |
|delta_m  |Standard error on the calibration value found for m                                    |
|delta_f  |A value proportional to the standard error on the calibration value found for floor    |

---

Hopefully this works!  
-Jonah
