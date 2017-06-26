# Calibration 2.0 #
An updated TDO calibration algorithm with helper scripts


## Motivation
Say you have a bunch of .root files created by the calibration GUI and you 
want to extract the calibration coefficients for every channel on every vmm on every board. This folder contains code which streamlines that process. 

These scripts use Chris Rogan's xADC/PDO calibration algorithm and Jonah's TDO calibration algorithm. All scripts in this folder have instructions which can be accessed via `python script.py -h`

## Scripts
`manager.py` - This is the main script I imagine people using. Run PDO or TDO calibration for a SINGLE board with this script. For instance, the command `python manager.py TDO TDO_output_direc/new_calib TDO_bench_data.root` will calibrate the channels in TDO_bench_data.root using Jonah's TDO algorithm, then store the results in TDO_output_direc/new_calib.root and TDO_output_direc/new_calib.dat. Similarly, `python manager.py PDO PDO_output_direc/new_calib xADC_bench_data.root PDO_bench_data.root` will calibrate the channels in `xADC_bench_data.root` and `PDO_bench_data.root` then store the results in `PDO_output_direc/new_calib.root` and `PDO_output_direc/new_calib.dat`.

`run_scripts.py` - An example of how to automate the procedure of running manager.py on several bench files (useful if you ever need to calibrate every board using every board's most recent bench data).

`TDO_PDO_calibration_scripts/` - This folder contains the scripts which run Jonah's TDO calibration algorithm and two helper scripts. The TDO calibration scripts are `Fit_TDO.py`, `Calibrate_TDO.py`, and `TDO_dat_to_root.py`. The first helper script is `PDOroot_to_PDOdat.py`. This script takes PDO calibration .root files to the .dat format Paulo likes. `plot_TDO.py` is a template script for how you can plot the TDO calibrations. It's function is to search through calibration data and identify noisy channels, then display the TDO calibration the algorithm found.

## Example Usage
1. Make Chris's calibration code: `cd ANALYSIS`, `make`
2. cd to Calibration2.0 and make a directory to store new calibration data: `cd ../Calibration2.0`, `mkdir first_calibrate` 
3. Calibrate PDO: `python manager.py PDO first_calibrate/board102_PDO_calib ../DATA/xADC_Jun9/board102_bench_xADC.root ../DATA/PDO_Jun9/board102_bench_PDO.root`
4. Calibrate TDO: `python manager.py TDO first_calibrate/board102_TDO_calib ../DATA/TDO_Jun9/board102_bench_TDO.root`
5. Check the outlier TDO calibrations: `python TDO_PDO_calibration_scripts/plot_TDO.py first_calibrate/board102_TDO_calib`

## Requirements and Notes
1. PDO calibration takes 1 minute / board. TDO calibration takes about 15 minutes / board .
2. manager.py probably only works on OS X. 
3. Your system's default python needs access to the `tensorflow` and `rootpy` packages. Both packages can be installed with pip. You also need `tqdm`! `tqdm` is a great package which displays progress bars. I include a progress bar in the Calibrate_TDO.py script since it takes so long.
4. The directory from which you run manager.py cannot have any files that start with 'ephem' in it. The reason is that a few "ephemeral" files are made during TDO and PDO calibration and they all start with "ephem". manager.py includes an assertion error to check for these cases.


-Jonah

]]></content>
  <tabTrigger>readme</tabTrigger>
</snippet>