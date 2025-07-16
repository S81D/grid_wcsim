import os

# Script to tar-ball WCSim directory for the grid

WCSim_loc = '/exp/annie/app/users/doran/WCSim_SD81_branch/'

print('\ntar-ing WCSim for grid submission...\n')
os.system('rm -rf WCSim.tar.gz')   # remove old tar file
os.system('cd ' + WCSim_loc)
os.system('tar -czvf WCSim.tar.gz -C ' + WCSim_loc + ' WCSim')

print('\ndone!\n')
