import os

# -- Submit WCSim jobs that run over the GENIE + flux files
# -- Returns wcsim.root files created from GENIE samples
# -- Author: Steven Doran
# -- July 2025

# There are a total of 5k GENIE + flux files for the WORLD events

INPUT_PATH = '/pnfs/annie/scratch/users/doran/genie_wcsim_grid/'

print('\nPlease specify the range of genie files you would like to loop over')
min_g = input('\nmin genie file #:    ')    #          (min = 0)
max_g = input('\nmax genie file #:    ')    # 5k total (max = 4999)

files = []
for i in range(int(min_g), int(max_g)+1):
	files.append(i)

print('\nTotal number of jobs = ' + str(len(files)))

print('\nSending job(s)...\n')
for i in range(len(files)):
	print('\n########## ' + str(files[i]) + ' ###########\n')
	os.system('sh submit_wcsim_job.sh ' + str(files[i]))


print('\nJobs sent\n')
