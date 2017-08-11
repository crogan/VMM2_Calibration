import os

base_dir = '/n/atlasfs/atlasdata/cosmic_ray/most_recent_calibrations_as_of_2017_08_10'  

with open(base_dir + '/AllBoards_PDO_recent_2017-08-11.dat', 'w') as writer:
    writer.write('MMFE8 VMM CH  Gain      Pedestal  (PDO = Q*G + P)\n')
    for file in os.listdir(base_dir):
        if 'PDO' in file and file[-4:] == '.dat' and not 'AllBoards' in file:
            print file
            with open(base_dir + '/' + file, 'r') as reader:
                reader.readline()
                for line in reader:
                    writer.write(line)

with open(base_dir + '/AllBoards_TDO_recent_2017-08-11.dat', 'w') as writer:
    writer.write('MMFE8 VMM CH  Gain      Pedestal  m         b         floor     n_samps   p_8       sigma     chi2      prob      delta_b   delta_m   delta_f\n')
    for file in os.listdir(base_dir):
        if 'TDO' in file and file[-4:] == '.dat' and not 'AllBoards' in file:
            print file
            with open(base_dir + '/' + file, 'r') as reader:
                reader.readline()
                for line in reader:
                    writer.write(line)

# with open(base_dir + '/AllBoards_recent_2017-08-11.dat', 'w') as writer:
#     boards = [101,102,105,111,118,119,120]
#     for i,board in enumerate(boards):
#         with open('TDOJun9_17/TDO_calib_' + str(board) + '.dat', 'r') as reader:
#             if i>0:
#                 reader.readline()
#             for line in reader:
#                 writer.write(line)

#     boards = [106,107,116,117]
#     for i,board in enumerate(boards):
#         with open('TDOApr22_17/TDO_calib_' + str(board) + '.dat', 'r') as reader:
#             reader.readline()
#             for line in reader:
#                 writer.write(line)
