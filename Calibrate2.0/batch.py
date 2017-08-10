import subprocess
import datetime
from time import sleep

def make_script(command_string, ix):

    with open('batcher' + str(ix) + '.sh', 'w') as writer:
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

folder_name1 = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
folder_name = folder_name1 + '-Calibrate'
subprocess.Popen('mkdir ' + folder_name, shell=True)

print folder_name

commands_TDO = ['python manager.py TDO ' + folder_name + '/board109_TDO_calib ../DATA/2017-08-09/board109_bench_TDO.root',
			'python manager.py TDO ' + folder_name + '/board122_TDO_calib ../DATA/2017-08-09/board122_bench_TDO.root' ,
            'python manager.py TDO ' + folder_name + '/board123_TDO_calib ../DATA/2017-08-09/board123_bench_TDO.root',
            'python manager.py TDO ' + folder_name + '/board124_TDO_calib ../DATA/2017-08-09/board124_bench_TDO.root',
            'python manager.py TDO ' + folder_name + '/board125_TDO_calib ../DATA/2017-08-09/board125_bench_TDO.root']

commands_PDO = ['python manager.py PDO ' + folder_name + '/board109_PDO_calib ../DATA/2017-08-09/board109_bench_xADC.root ../DATA/2017-08-09/board109_bench_PDO.root',
			'python manager.py PDO ' + folder_name + '/board122_PDO_calib ../DATA/2017-08-09/board122_bench_xADC.root ../DATA/2017-08-09/board122_bench_PDO.root',
            'python manager.py PDO ' + folder_name + '/board123_PDO_calib ../DATA/2017-08-09/board123_bench_xADC.root ../DATA/2017-08-09/board123_bench_PDO.root',
            'python manager.py PDO ' + folder_name + '/board124_PDO_calib ../DATA/2017-08-09/board124_bench_xADC.root ../DATA/2017-08-09/board124_bench_PDO.root',
            'python manager.py PDO ' + folder_name + '/board125_PDO_calib ../DATA/2017-08-09/board125_bench_xADC.root ../DATA/2017-08-09/board125_bench_PDO.root']          

commands = commands_TDO + commands_PDO

for enum,command in enumerate(commands):
    make_script(command, enum)
    subprocess.Popen('sbatch batcher' + str(enum) + '.sh', shell=True)
    # sleep for a second to be polite to the sbatch scheduler
    sleep(1)










