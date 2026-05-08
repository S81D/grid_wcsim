import os,sys
import time

#WCSim_loc = '/pnfs/annie/persistent/users/dajana/'
WCSim_loc = '/exp/annie/app/users/dajana/'

QE_tag = 'QE_1.50'

# AmBe
job_labels = [
    'port1_z0'      + str(QE_tag),
    'port1_z50' + str(QE_tag),
    'port1_zminus50' + str(QE_tag),
    'port1_z100' + str(QE_tag),
    'port1_zminus100' + str(QE_tag),
    'port4_z0' + str(QE_tag),
    'port4_z50' + str(QE_tag),
    'port4_zminus50' + str(QE_tag),
    'port4_z100' + str(QE_tag),
    'port4_zminus100' + str(QE_tag),
    'port5_z0' + str(QE_tag),
    'port5_z50' + str(QE_tag),
    'port5_zminus50' + str(QE_tag),
    'port5_z100' + str(QE_tag),
    'port5_zminus100' + str(QE_tag),
    'port2_z0' + str(QE_tag),
    'port2_z50' + str(QE_tag),
    'port2_zminus50' + str(QE_tag),
    'port2_z100' + str(QE_tag),
    'port2_zminus100' + str(QE_tag),
    'port3_z0' + str(QE_tag),
    'port3_z50' + str(QE_tag),
    'port3_zminus50' + str(QE_tag),
    'port3_z100' + str(QE_tag),
    'port3_zminus100' + str(QE_tag)
]

####################
events_per_job = 1000
####################
N_jobs = 20
####################
total_events = int(N_jobs*events_per_job)

print('\nYou have chosen:\n')
print(' - ' + str(events_per_job) + ' events per job\n')
print(' - ' + str(N_jobs) + ' total jobs to be submitted\n')
print(' - ' + str(total_events) + ' total events across all jobs\n')
print('\nQE_tag: ' + str(QE_tag) + '\n')
time.sleep(3)

def create_macro(WCSim_loc, job_label, events_per_job):

    template_path = WCSim_loc + 'WCSim/WCSim/WCSim.mac'
    output_path   = WCSim_loc + 'WCSim/build/WCSim.mac'

    # port 1 (x = 0, z = -75)
    if job_label == 'port1_z0' + str(QE_tag):
        source_pos = '/gps/pos/centre 0 -14.46487518 93.1 cm'
    elif job_label == 'port1_z50' + str(QE_tag):
        source_pos = '/gps/pos/centre 0 35.53512482 93.1 cm'
    elif job_label == 'port1_z100' + str(QE_tag):
        source_pos = '/gps/pos/centre 0 85.53512482 93.1 cm'
    elif job_label == 'port1_zminus50' + str(QE_tag):
        source_pos = '/gps/pos/centre 0 -64.46487518 93.1 cm'
    elif job_label == 'port1_zminus100' + str(QE_tag):
        source_pos = '/gps/pos/centre 0 -114.46487518 93.1 cm'

    # port 4 (x = -75, z = 0)
    elif job_label == 'port4_z0' + str(QE_tag):
        source_pos = '/gps/pos/centre -75 -14.46487518 168.1 cm'
    elif job_label == 'port4_z50' + str(QE_tag):
        source_pos = '/gps/pos/centre -75 35.53512482 168.1 cm'
    elif job_label == 'port4_z100' + str(QE_tag):
        source_pos = '/gps/pos/centre -75 85.53512482 168.1 cm'
    elif job_label == 'port4_zminus50' + str(QE_tag):
        source_pos = '/gps/pos/centre -75 -64.46487518 168.1 cm'
    elif job_label == 'port4_zminus100' + str(QE_tag):
        source_pos = '/gps/pos/centre -75 -114.46487518 168.1 cm'

    # port 5 (x = 0, z = 0)
    elif job_label == 'port5_z0' + str(QE_tag):
        source_pos = '/gps/pos/centre 0 -14.46487518 168.1 cm'
    elif job_label == 'port5_z50' + str(QE_tag):
        source_pos = '/gps/pos/centre 0 35.53512482 168.1 cm'
    elif job_label == 'port5_z100' + str(QE_tag):
        source_pos = '/gps/pos/centre 0 85.53512482 168.1 cm'
    elif job_label == 'port5_zminus50' + str(QE_tag):
        source_pos = '/gps/pos/centre 0 -64.46487518 168.1 cm'
    elif job_label == 'port5_zminus100' + str(QE_tag):
        source_pos = '/gps/pos/centre 0 -114.46487518 168.1 cm'

    # port 2 (x = 0, z = 75)
    elif job_label == 'port2_z0' + str(QE_tag):
        source_pos = '/gps/pos/centre 0 -14.46487518 243.1 cm'
    elif job_label == 'port2_z50' + str(QE_tag):
        source_pos = '/gps/pos/centre 0 35.53512482 243.1 cm'
    elif job_label == 'port2_z100' + str(QE_tag):
        source_pos = '/gps/pos/centre 0 85.53512482 243.1 cm'
    elif job_label == 'port2_zminus50' + str(QE_tag):
        source_pos = '/gps/pos/centre 0 -64.46487518 243.1 cm'
    elif job_label == 'port2_zminus100' + str(QE_tag):
        source_pos = '/gps/pos/centre 0 -114.46487518 243.1 cm'

    # port 3 (x = 0, z = 102)
    elif job_label == 'port3_z0' + str(QE_tag):
        source_pos = '/gps/pos/centre 0 -14.46487518 270.1 cm'
    elif job_label == 'port3_z50' + str(QE_tag):
        source_pos = '/gps/pos/centre 0 35.53512482 270.1 cm'
    elif job_label == 'port3_z100' + str(QE_tag):
        source_pos = '/gps/pos/centre 0 85.53512482 270.1 cm'
    elif job_label == 'port3_zminus50' + str(QE_tag):
        source_pos = '/gps/pos/centre 0 -64.46487518 270.1 cm'
    elif job_label == 'port3_zminus100' + str(QE_tag):
        source_pos = '/gps/pos/centre 0 -114.46487518 270.1 cm'

    print('\n')
    print(job_label)
    print(source_pos)

    with open(template_path, 'r') as f:
        lines = f.readlines()

    out_lines = []
    for line in lines:
        if line.strip().startswith('# port'):
            out_lines.append('# ' + job_label + '\n')
        elif line.strip().startswith('/gps/pos/centre'):
            out_lines.append(source_pos + '\n')
        elif line.strip().startswith('/run/beamOn'):
            out_lines.append('/run/beamOn ' + str(events_per_job) + '\n')
        else:
            out_lines.append(line)

    with open(output_path, 'w') as f:
        f.writelines(out_lines)

    print('WCSim.mac edited\n')
    return


def submit_batch(WCSim_loc, job_label, events_per_job):

    create_macro(WCSim_loc, job_label, events_per_job)

    print('WCSim.mac details:')
    print('------------------')
    os.system('cat ' + WCSim_loc + 'WCSim/build/WCSim.mac')
    print('\n')
    time.sleep(5)
    #'''
    # tar WCSim — write directly to pnfs staging area (grid workers cannot reach /exp/)
    pnfs_hold = '/pnfs/annie/scratch/users/dajana/WCSim_grid/AmBe_neutrons/hold/'
    print('\ntar-ing WCSim for grid submission...\n')
    os.system('mkdir -p ' + pnfs_hold + job_label)
    os.system('rm -rf ' + pnfs_hold + job_label + '/WCSim.tar.gz')
    # only pack the build directory; exclude simulation output files but keep pulsecharacteristics.root
    os.system('tar -czvf WCSim.tar.gz -C ' + WCSim_loc + ' WCSim')
    os.system('mv WCSim.tar.gz ' + pnfs_hold + job_label + '/')
    time.sleep(1)
    #'''
    return


count = 0
for jl in job_labels:

    # uncomment for testing
    #if count > 1:
    #    continue
    #count += 1

    submit_batch(WCSim_loc, jl, events_per_job)  

    print('\nSending jobs for ' + jl + '...\n')
    for i in range(N_jobs):
        starting_event = i*events_per_job
        ending_event = (i+1)*events_per_job - 1
        print('\n########## ' + str(starting_event) + '_' + str(ending_event) + ' ###########\n')
        os.system('sh submit_wcsim_job.sh ' + str(starting_event) + '_' + str(ending_event) + ' ' + jl)

print('\nJobs sent\n')
