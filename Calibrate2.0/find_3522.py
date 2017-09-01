"""
This script searches through ../DATA for the most recent calibration data for boards with ip in range(100,130) but before 2017-05-11 (when 3522 began). 
It then generates .sh scripts called 3522_*.sh for some number * and sbatches them. TO get calibration data for a different run, the variables that need to change are the file outpute and the start date of the run. 
"""


import os
import datetime
import subprocess
import datetime
from time import sleep


def make_script(command_string, ix):

    with open('3522_' + str(ix) + '.sh', 'w') as writer:
        writer.write(
"""#!/bin/bash                                                                                                                                                                         
#                                                                                                                                                                                   
#SBATCH -n 1                 # Number of cores                                                                                                                                      
#SBATCH -N 1                 # Number of nodes for the cores                                                                                                                        
#SBATCH -c 32                                                                                                                                                                       
#SBATCH -t 0-06:00           # Runtime in D-HH:MM format                                                                                                                            
#SBATCH -p serial_requeue                                                                                                                                                           
#SBATCH --mem=100000            # Memory pool for all CPUs                                                                                                                           
#SBATCH -o """ + folder_name + """/ya-%j.out      # File to which standard out will be written                                                                                                             
#SBATCH -e """ + folder_name + """/ya-%j.err      # File to which standard err will be written                                                                                                             
#SBATCH --open-mode=append                                                                                                                                                          
#SBATCH --mail-type=ALL      # Type of email notification- BEGIN,END,FAIL,ALL                                                                                                       
#SBATCH --mail-user=jonahphilion@college.harvard.edu  #Email to which notifications will be sent

echo $SLURM_LOCALID
echo $SLURM_JOB_PARTITION
echo $SLURM_NODE_ALIASES
echo $SLURM_NODEID
echo $SLURMD_NODENAME

"""
 + command_string
)




name_to_date = {}
date_to_name = {}
with open('../DATA/name_to_date.txt') as f:
    for line in f:
        date_list = map(int, line.split('->')[-1].split('-'))
        name_to_date[line.split('->')[0]] = datetime.datetime(date_list[0], date_list[1], date_list[2])
        if datetime.datetime(date_list[0], date_list[1], date_list[2]) in date_to_name:
            date_to_name[datetime.datetime(date_list[0], date_list[1], date_list[2])].append(line.split('->')[0])
        else:
            date_to_name[datetime.datetime(date_list[0], date_list[1], date_list[2])] = [line.split('->')[0]]

name_to_date['2017-08-09'] = datetime.datetime(2017, 8, 9)
date_to_name[datetime.datetime(2017, 8, 9)] = '2017-08-09'

sorted_dates = list(reversed(sorted(date_to_name.keys())))

ips_to_look_for = [118,116,102,119,106,107,117,105]

ip_to_tdo = {ip:[] for ip in ips_to_look_for}
ip_to_pdo = {ip:[] for ip in ips_to_look_for}
ip_to_xadc = {ip:[] for ip in ips_to_look_for}
for ip in ips_to_look_for:
    for name in name_to_date:
        if name_to_date[name]<datetime.datetime(2017, 5, 11):
            for root_name in os.listdir('../DATA/' + name):
                if str(ip) in root_name and not 'Fit' in root_name and not 'calib' in root_name and not 'fit' in root_name and not 'Calib' in root_name and not '.dat' in root_name:
                    if 'TDO' in root_name:
                        ip_to_tdo[ip].append(['../DATA/' + name + '/' + root_name, name, name_to_date[name]])
                    elif 'PDO' in root_name:
                        ip_to_pdo[ip].append(['../DATA/' + name + '/' + root_name, name, name_to_date[name]])
                    elif 'xADC' in root_name:
                        ip_to_xadc[ip].append(['../DATA/' + name + '/' + root_name, name, name_to_date[name]])
recent_tdo = {}
recent_pdo = {}
recent_xadc = {} 

folder_name = 'Run3522-Calibrate'           

for ip in ips_to_look_for:
    if len(ip_to_tdo[ip]) > 0 and len(ip_to_pdo[ip]) > 0 and len(ip_to_xadc[ip]) > 0:
        recent_tdo[ip] = [so[:2] for so in list(reversed(sorted(ip_to_tdo[ip], key=lambda x: x[2])))][0][0]
        recent_pdo[ip] = [so[:2] for so in list(reversed(sorted(ip_to_pdo[ip], key=lambda x: x[2])))][0][0]
        recent_xadc[ip] = [so[:2] for so in list(reversed(sorted(ip_to_xadc[ip], key=lambda x: x[2])))][0][0]


# for enum,ip in enumerate(recent_xadc):
#     command = 'python manager.py TDO ' + folder_name + '/board' + str(ip) + '_TDO_calib ' + recent_tdo[ip]
#     make_script(command, 2*enum)
#     subprocess.Popen('sbatch 3522_' + str(2*enum) + '.sh', shell=True)
#     # sleep for a second to be polite to the sbatch scheduler
#     sleep(1)

#     command = 'python manager.py PDO ' + folder_name + '/board' + str(ip) + '_PDO_calib ' + recent_xadc[ip] + ' ' + recent_pdo[ip]
#     make_script(command, 2*enum+1)
#     subprocess.Popen('sbatch 3522_' + str(2*enum+1) + '.sh', shell=True)
#     # sleep for a second to be polite to the sbatch scheduler
#     sleep(1)



# dirs = [f for f in os.listdir('../DATA') if 'TDO' in f or 'PDO' in f or 'xADC' in f]

# writer = open('name_to_date.txt', 'wb')
# for d in dirs:
#     print d
#     writer.write(d + '->\n')

# writer.close()


    # for root_file in os.listdir('../DATA/' + d):
    #     with root_open('../DATA/' + d + '/' + root_file) as f:
    #         try:
    #             date_object = f.date
    #         except AttributeError:
    #             print 'nothing'
    #             continue
    #         for da in date_object:
    #             print da.Year, da.Month, da.Day
    #             print datetime.datetime(da.Year, da.Month, da.Day)
    # print ''


# with root_open('../') as f:
#   vm = f.date
