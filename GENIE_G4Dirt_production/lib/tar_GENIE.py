import os

# usage: python3 lib/tar_GENIE.py

# Script to tar GENIE directory for the grid

GENIE_loc = ''      # MODIFY (parent folder GENIE/ lives in)
GENIE_folder = ''   # name of GENIE directory

print('\ntar-ing GENIE for grid submission...\n')
os.system('rm -rf GENIE.tar.gz')   # remove old tar file
os.system('cd ' + GENIE_loc)
os.system('tar -czvf GENIE.tar.gz -C ' + GENIE_loc + ' ' + GENIE_folder)

print('\ndone!\n')