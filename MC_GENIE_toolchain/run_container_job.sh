#!/bin/bash
# Steven Doran

RUN=$1

# logfile
touch /srv/logfile_${RUN}.txt
pwd >> /srv/logfile_${RUN}.txt
ls -v >> /srv/logfile_${RUN}.txt
echo "" >> /srv/logfile_${RUN}.txt

# enter ToolAnalysis directory (*** change accordingly ***)
cd MC_waveform_sim/

# run config script
cd configfiles/PMTWaveformSim
python3 config_GENIE.py ${RUN}
echo "PhaseIITreeMaker config:" >> /srv/logfile_${RUN}.txt
echo "------------------------" >> /srv/logfile_${RUN}.txt
cat PhaseIITreeMakerConfig >> /srv/logfile_${RUN}.txt
echo "" >> /srv/logfile_${RUN}.txt
echo "LoadWCSim config:" >> /srv/logfile_${RUN}.txt
echo "-----------------" >> /srv/logfile_${RUN}.txt
cat LoadWCSimConfig >> /srv/logfile_${RUN}.txt
echo "" >> /srv/logfile_${RUN}.txt
cd ../../

# set up paths and libraries
source Setup.sh

# Run the toolchain, and output verbose to log file
./Analyse configfiles/PMTWaveformSim/ToolChainConfig >> /srv/logfile_${RUN}.txt 2>&1 

# log files
echo "" >> /srv/logfile_${RUN}.txt
echo "**************************************************" >> /srv/logfile_${RUN}.txt
echo "" >> /srv/logfile_${RUN}.txt
echo "ToolAnalysis directory contents:" >> /srv/logfile_${RUN}.txt
ls -lrth >> /srv/logfile_${RUN}.txt

# copy any produced files to /srv for extraction (*** change accordingly ***)
cp tree.root /srv/MC_${RUN}.root

# make sure any output files you want to keep are put in /srv or any subdirectory of /srv

### END ###
