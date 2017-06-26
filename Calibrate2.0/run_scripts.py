"""This is an example of how you might use manager.py on several files in various directories.
Since the TDO calibration takes about 15 minutes per board, making one of these
can save you some time."""


import subprocess

############################ PDO Calib ############################

# board_num = 118
# command = 'python manager.py PDO PDOApr22_17/PDO_calib_' + str(board_num) + ' ../DATA/xADC_Apr21/board' + str(board_num) + '_bench_xADC.root' + ' ../DATA/PDO_Apr21/board' + str(board_num) + '_bench_PDO.root'
# subprocess.call(command , shell=True)

# board_num = 120
# command = 'python manager.py PDO PDOApr22_17/PDO_calib_' + str(board_num) + ' ../DATA/xADC_Apr21/board' + str(board_num) + '_bench_xADC.root' + ' ../DATA/PDO_Apr21/board' + str(board_num) + '_bench_PDO.root'
# subprocess.call(command , shell=True)

# board_num = 117
# command = 'python manager.py PDO PDOApr22_17/PDO_calib_' + str(board_num) + ' ../DATA/xADC_Apr13/board' + str(board_num) + '_bench_xADC.root' + ' ../DATA/PDO_Apr13/board' + str(board_num) + '_bench_PDO.root'
# subprocess.call(command , shell=True)

# board_num = 102
# command = 'python manager.py PDO PDOApr22_17/PDO_calib_' + str(board_num) + ' ../DATA/xADC_Apr06/board' + str(board_num) + '_bench_xADC.root' + ' ../DATA/PDO_Apr06/board' + str(board_num) + '_bench_PDO.root'
# subprocess.call(command , shell=True)

# board_num = 105
# command = 'python manager.py PDO PDOApr22_17/PDO_calib_' + str(board_num) + ' ../DATA/xADC_Sep01/Board' + str(board_num) + '_xADC.root' + ' ../DATA/PDO_Sep01/Board' + str(board_num) + '_PDO_Aug24.root'
# subprocess.call(command , shell=True)

# board_num = 106
# command = 'python manager.py PDO PDOApr22_17/PDO_calib_' + str(board_num) + ' ../DATA/xADC_Apr06/board' + str(board_num) + '_bench_xADC.root' + ' ../DATA/PDO_Apr06/board' + str(board_num) + '_bench_PDO.root'
# subprocess.call(command , shell=True)

# board_num = 107
# command = 'python manager.py PDO PDOApr22_17/PDO_calib_' + str(board_num) + ' ../DATA/xADC_Sep01/Board' + str(board_num) + '_xADC.root' + ' ../DATA/PDO_Sep01/Board' + str(board_num) + '_PDO_Aug3.root'
# subprocess.call(command , shell=True)

# board_num = 111
# command = 'python manager.py PDO PDOApr22_17/PDO_calib_' + str(board_num) + ' ../DATA/xADC_Sep01/Board' + str(board_num) + '_bench_xADC.root' + ' ../DATA/PDO_Sep01/Board' + str(board_num) + '_bench_PDO.root'
# subprocess.call(command , shell=True)

# board_num = 116
# command = 'python manager.py PDO PDOApr22_17/PDO_calib_' + str(board_num) + ' ../DATA/xADC_Apr06/board' + str(board_num) + '_bench_xADC.root' + ' ../DATA/PDO_Apr06/board' + str(board_num) + '_bench_PDO.root'
# subprocess.call(command , shell=True)

# board_num = 119
# command = 'python manager.py PDO PDOApr22_17/PDO_calib_' + str(board_num) + ' ../DATA/xADC_Sep28/Board' + str(board_num) + '_xADC.root' + ' ../DATA/PDO_Sep28/Board' + str(board_num) + '_bench_PDO.root'
# subprocess.call(command , shell=True)



boards = [101,102,105,107,111,118,119,120]
for board in boards:
	command = 'python manager.py PDO PDOJun9_17/PDO_calib_' + str(board) + ' ../DATA/xADC_Jun9/board' + str(board) + '_bench_xADC.root' + ' ../DATA/PDO_Jun9/board' + str(board) + '_bench_PDO.root'
	subprocess.call(command, shell=True)







############################ TDO Calib ############################

# board_num = 118
# command = 'python manager.py TDO TDOApr22_17/TDO_calib_' + str(board_num) + ' ../DATA/TDO_Apr21/board' + str(board_num) + '_bench_TDO.root'
# subprocess.call(command , shell=True)

# board_num = 120
# command = 'python manager.py TDO TDOApr22_17/TDO_calib_' + str(board_num) + ' ../DATA/TDO_Apr21/board' + str(board_num) + '_bench_TDO.root'
# subprocess.call(command , shell=True)

# board_num = 117
# command = 'python manager.py TDO TDOApr22_17/TDO_calib_' + str(board_num) + ' ../DATA/TDO_Apr13/board' + str(board_num) + '_bench_TDO.root'
# subprocess.call(command , shell=True)

# board_num = 102
# command = 'python manager.py TDO TDOApr22_17/TDO_calib_' + str(board_num) + ' ../DATA/TDO_Apr06/board' + str(board_num) + '_bench_TDO.root'
# subprocess.call(command , shell=True)

# board_num = 105
# command = 'python manager.py TDO TDOApr22_17/TDO_calib_' + str(board_num) + ' ../DATA/TDO_Apr06/board' + str(board_num) + '_bench_TDO.root'
# subprocess.call(command , shell=True)

# board_num = 106
# command = 'python manager.py TDO TDOApr22_17/TDO_calib_' + str(board_num) + ' ../DATA/TDO_Apr06/board' + str(board_num) + '_bench_TDO.root'
# subprocess.call(command , shell=True)

# board_num = 107
# command = 'python manager.py TDO TDOApr22_17/TDO_calib_' + str(board_num) + ' ../DATA/TDO_Apr06/board' + str(board_num) + '_bench_TDO.root'
# subprocess.call(command , shell=True)

# board_num = 111
# command = 'python manager.py TDO TDOApr22_17/TDO_calib_' + str(board_num) + ' ../DATA/TDO_Apr06/board' + str(board_num) + '_bench_TDO.root'
# subprocess.call(command , shell=True)

# board_num = 116
# command = 'python manager.py TDO TDOApr22_17/TDO_calib_' + str(board_num) + ' ../DATA/TDO_Apr06/board' + str(board_num) + '_bench_TDO.root'
# subprocess.call(command , shell=True)

# board_num = 119
# command = 'python manager.py TDO TDOApr22_17/TDO_calib_' + str(board_num) + ' ../DATA/TDO_Apr06/board' + str(board_num) + '_bench_TDO.root'
# subprocess.call(command , shell=True)




