import os

# -- Submit WCSim jobs that run over the GENIE + flux files
# -- Returns wcsim.root files created from GENIE samples
# -- Author: Steven Doran
# -- July 2025

# There are a total of 5k GENIE + flux files for the WORLD events

INPUT_PATH = '/pnfs/annie/scratch/users/doran/genie_wcsim_grid/'
GENIE_PATH = '/pnfs/annie/persistent/users/doran/GENIE-016-empirical-model/genie/ghep/'
DIRT_PATH = '/pnfs/annie/persistent/users/doran/GENIE-016-empirical-model/anniedirt/annie/'

# for standard submission
# - - - - - - - - - - - - - - - - - - -
print('\nPlease specify the range of genie files you would like to loop over')
min_g = input('\nmin genie file #:    ')    #          (min = 0)
max_g = input('\nmax genie file #:    ')    # 5k total (max = 4999)

files = []
for i in range(int(min_g), int(max_g)+1):
	files.append(i)
# - - - - - - - - - - - - - - - - - - -

# comment above block and uncomment block below if sending specific jobs
# - - - - - - - - - - - - - - - - - - -
#files = [0, 1, 2]
# - - - - - - - - - - - - - - - - - - -

print('\nTotal number of jobs = ' + str(len(files)))
print('\nSending job(s)...\n')
submitted = []; skipped = []
for i in range(len(files)):
	RUN = files[i]
	genie_file = os.path.join(GENIE_PATH, 'gntp.' + str(RUN) + '.ghep.root')
	flux_file = os.path.join(DIRT_PATH, 'annie_tank_flux.' + str(RUN) + '.root')
	missing = []
	if not os.path.isfile(genie_file):
			missing.append(genie_file)
	if not os.path.isfile(flux_file):
			missing.append(flux_file)

	if missing:
			print('\n########## ' + str(RUN) + ' (SKIPPED) ###########')
			for m in missing:
					print('  Missing: ' + m)
			skipped.append(RUN)
			continue

	print('\n########## ' + str(RUN) + ' ###########\n')
	os.system('sh submit_wcsim_job.sh ' + str(RUN))
	submitted.append(RUN)


print('\nJobs sent: ' + str(len(submitted)))
print('Jobs skipped (missing input): ' + str(len(skipped)))
if skipped:
        print('Skipped run numbers: ' + str(skipped))
print('')
