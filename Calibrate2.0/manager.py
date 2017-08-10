"""This is a manager script intended to streamline the calibration process.
To calibrate the TDO, tell the script what it
should call its output then give the script a bench TDO file. To calibrate the PDO, tell the
script what to call its output then give the script xADC and PDO files from the bench.

Examples: 
                    
            python manager.py TDO output_direc/board_111_TDO_calib board111_bench_TDO.root

            python manager.py PDO output_direc/board_111_PDO_calib board111_bench_xADC.root board111_bench_PDO.root

-Jonah
"""

import argparse
import sys
import subprocess
import os
import pickle

parser = argparse.ArgumentParser()
parser.add_argument("command", help="The variable to be calibrated", 
                        choices=["PDO", "TDO"])
parser.add_argument("output_file_name", help="""Send results to output_file_name.root and output_file_name.dat""")
parser.add_argument("input_file", help="""If "command" is TDO, then "input_file" must be
                a .root file made by the TDO Calibration GUI. If "command" is PDO, then "input_file" must be
                a .root file made by the xADC Calibration GUI, then a .root file made by the PDO Calibration GUI.""", nargs="+")

args = parser.parse_args()

#assert(not 'ephem' in [fi[:5] for fi in os.listdir('.')]), """remove any files that start with 'ephem' from the current working directory (this script generates temporary files with names that start with 'ephem')  """

if args.command == 'TDO':
    assert(len(sys.argv) == 4), """Improper number of arguments for TDO calibration. To get some guidance, type "python manager.py -h" for help or "head manager.py" for examples"""
    assert(sys.argv[-1][-5:] == '.root'), """Incorrect file type for TDO calibration. Type "python manager.py -h" for help or "head manager.py" for examples"""

    command = 'python TDO_PDO_calibration_scripts/Fit_TDO.py ' + sys.argv[-1] + ' ' + sys.argv[2] + '.p'
    subprocess.call(command, shell=True)
    board_num_dict = pickle.load( open(sys.argv[2] + '_boardnum.p' , "rb" ) )
    board_num = board_num_dict['board_num']
    os.remove(sys.argv[2] + '_boardnum.p')
    command = 'python TDO_PDO_calibration_scripts/Calibrate_TDO.py ' + sys.argv[2] + '.p ' + sys.argv[2] + '.dat ' + str(board_num)
    subprocess.call(command, shell=True)
    command = 'python TDO_PDO_calibration_scripts/TDO_dat_to_root.py ' + sys.argv[2] + '.dat'
    subprocess.call(command, shell=True)


if args.command == 'PDO':
    assert(len(sys.argv) == 5), """Improper number of arguments for PDO calibration. To get some guidance, type "python manager.py -h" for help or "head manager.py" for examples"""
    assert(sys.argv[-1][-5:] == '.root'), """Incorrect file type for PDO calibration. Type "python manager.py -h" for help or "head manager.py" for examples"""
    assert(sys.argv[-2][-5:] == '.root'), """Incorrect file type for PDO calibration. Type "python manager.py -h" for help or "head manager.py" for examples"""

    xADC_f_name = 'ephem_xADC_f' + sys.argv[-3].split('/')[-1] + '.root'
    xADC_c_name = 'ephem_xADC_c' + sys.argv[-3].split('/')[-1] + '.root'
    PDO_f_name = 'ephem_PDO_f' + sys.argv[-3].split('/')[-1] + '.root'

    command = '../ANALYSIS/Fit_xADC ' + sys.argv[-2] + ' -o ' + xADC_f_name
    subprocess.call(command, shell=True)
    command = '../ANALYSIS/Calibrate_xADC ' + xADC_f_name + ' -o ' + xADC_c_name
    subprocess.call(command, shell=True)
    os.remove(xADC_f_name)

    command = '../ANALYSIS/Fit_PDO ' + sys.argv[-1] + ' -o ' + PDO_f_name
    subprocess.call(command, shell=True)
    command = '../ANALYSIS/Calibrate_PDO ' + PDO_f_name + ' -x ' + xADC_c_name + ' -o ' + sys.argv[-3] + '.root'
    subprocess.call(command, shell=True)
    os.remove(xADC_c_name)
    os.remove(PDO_f_name)
    command = 'python TDO_PDO_calibration_scripts/PDOroot_to_PDOdat.py ' + sys.argv[-3] + '.root'
    subprocess.call(command, shell=True)

