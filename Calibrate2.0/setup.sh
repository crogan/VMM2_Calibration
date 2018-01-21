#case 
# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

# User specific aliases and functions
source new-modules.sh

# module load gcc/4.9.3-fasrc01 tensorflow/1.0.0-fasrc01

# Load Anaconda
module load python/2.7.11-fasrc01

# Load playground environment
source activate /n/home14/jphilion/.conda/envs/playground

# #Load tensorflow
module load gcc/4.9.3-fasrc01 tensorflow/1.0.0-fasrc01

#Setup root
source atlasSetup.sh
lsetup root
