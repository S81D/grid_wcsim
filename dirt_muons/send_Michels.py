import os
import time
import random

# Submit dirt muons to simulate beam-realistic Michel electrons
# The jobs will sample the dirt muon txt file which is pulled from GENIE muons that only pass the FMV + Tank (no MRD) geometry in the WORLD samples

WCSim_loc = '/exp/annie/app/users/doran/WCSim_SD81_branch/'
INPUT_PATH = '/pnfs/annie/scratch/users/doran/grid_wcsim/dirt_muons/'

job_label = 'pmt_tilting_dirt_QE_1.50/'        # This will also serve as the embedded output folder

# dirt muon count from GENIE files: 10000

# this only ends up yielding ~400 dirt muon candidates, and even less Michels. 
# We need to randomly sample the dirt muons to simulate way more events (~500k). 

####################
events_per_job = 500
####################
N_jobs = 1000
####################
total_events = int(N_jobs*events_per_job)

print('\nYou have chosen:\n')
print(' - ' + str(events_per_job) + ' events per job\n')
print(' - ' + str(N_jobs) + ' total jobs to be submitted\n')
print(' - ' + str(total_events) + ' total events across all jobs\n')
print('\n')


def load_genie():

    txt_file = 'dirt_muons_genie.txt'

    # Reading the .txt file
    with open(txt_file, 'r') as file:
        lines = file.readlines()

    # Processing each line
    data = []
    for line in lines:
        # Splitting each line into a list of floats
        entries = list(map(float, line.split()))
        data.append(entries)

    return data


def create_macro(start, end, energy, direction, position):

    job_number = str(start) + '_' + str(end)
    os.system('rm -rf submit/' + job_number)
    os.system('mkdir -p submit/' + job_number)
    file = open('submit/' + job_number + '/WCSim.mac', "w")

    preamble = """#!/bin/sh 

/run/verbose 0
/tracking/verbose 0
/hits/verbose 0
/process/em/verbose 0
/process/had/cascade/verbose 0
/process/verbose 0
/process/setVerbose 0
/run/initialize
/vis/disable

# QE Stacking
/WCSim/PMTQEMethod      Multi_Tank_Types
/WCSim/LAPPDQEMethod    Multi_Tank_Types

#turn on or off the collection efficiency
/WCSim/PMTCollEff on

# command to choose save or not save the pi0 info 07/03/10 (XQ)
/WCSim/SavePi0 false

#grab the DAQ options (digitizer type, thresholds, timing windows, etc.)
/control/execute macros/annie_daq.mac

# Select which time window(s) to add dark noise to
/DarkRate/SetDetectorElement tank
/DarkRate/SetDarkMode 1
/DarkRate/SetDarkHigh 100000
/DarkRate/SetDarkLow 0
/DarkRate/SetDarkWindow 4000

/DarkRate/SetDetectorElement mrd
/DarkRate/SetDarkMode 1
/DarkRate/SetDarkHigh 100000
/DarkRate/SetDarkLow 0
/DarkRate/SetDarkWindow 4000

/DarkRate/SetDetectorElement facc
/DarkRate/SetDarkMode 1
/DarkRate/SetDarkHigh 100000


# set the random seed
/control/execute macros/setRandomParameters.mac
    
"""

    root_file = '/WCSimIO/RootFile wcsim_' + job_number 

    file.write(preamble)
    file.write('\n')
    file.write('# root output file name\n')
    file.write(root_file)
    file.write('\n\n\n')

    file.write('#####################################\n')
    file.write('## PRIMARY SOURCES\n')
    file.write('#####################################\n')
    file.write('\n')

    for i in range(start, end+1):
        file.write('# ---- Event ' + str(i) + ' ---- #\n')
        file.write('/mygen/generator gps\n')
        file.write('/gps/particle mu-\n')
        file.write('/gps/energy ' + str(energy[i]) + ' MeV\n')
        file.write('/gps/direction ' + str(direction[0][i]) + ' ' + str(direction[1][i]) + ' ' + str(direction[2][i]) + '\n')
        file.write('/gps/pos/centre ' + str(position[0][i]) + ' ' + str(position[1][i]) + ' ' + str(position[2][i]) + ' cm\n')
        file.write('/gps/ang/rot1 -1 0 0\n')
        file.write('/gps/ang/rot2 0 1 0\n')
        file.write('/run/beamOn 1\n')
        file.write('\n')

    file.write('#####################################\n')
    file.write('## END OF PRIMARY SOURCES\n')
    file.write('#####################################\n')
    file.write('\n')

    file.write('exit\n')

    file.close()


energy = []; direction = [[], [], []]  # x, y, z
vertex = [[], [], []]     # x, y, z

# Load in GENIE information
genie_data = load_genie()
N_genie_events = len(genie_data) - 1

for i in range(total_events):

    # due to the limited number of events to chose from, randomly sample them for each job
    random_event = random.randint(0, N_genie_events)
    
    vertex[0].append(genie_data[random_event][0])
    vertex[1].append(genie_data[random_event][1])
    vertex[2].append(genie_data[random_event][2])

    direction[0].append(genie_data[random_event][3])
    direction[1].append(genie_data[random_event][4])
    direction[2].append(genie_data[random_event][5])

    energy.append(genie_data[random_event][6])


# Create macro file
print('\nCreating .mac files...\n')
for i in range(N_jobs):
    starting_event = i*events_per_job
    ending_event = (i+1)*events_per_job - 1
    print(str(starting_event) + '_' + str(ending_event))
    create_macro(starting_event, ending_event, energy, direction, vertex)

time.sleep(1)

# tar WCSim
print('\ntar-ing WCSim for grid submission...\n')
os.system('rm -rf WCSim.tar.gz')   # remove old tar file
os.system('cd ' + WCSim_loc)
os.system('tar -czvf WCSim.tar.gz -C ' + WCSim_loc + ' WCSim')
time.sleep(1)


print('\nSending jobs...\n')
for i in range(N_jobs):
    starting_event = i*events_per_job
    ending_event = (i+1)*events_per_job - 1
    print('\n########## ' + str(starting_event) + '_' + str(ending_event) + ' ###########\n')
    os.system('sh submit_wcsim_job.sh ' + str(starting_event) + '_' + str(ending_event) + ' ' + job_label)


print('\nJobs sent\n')
