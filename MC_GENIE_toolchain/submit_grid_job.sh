#!/bin/bash
# Author: Steven Doran

RUN=$1
INPUT_PATH=$2
OUTPUT_FOLDER=$3
WCSIM_FILE_PATH=$4
GENIE_FILE_PATH=$5

mkdir -p $OUTPUT_FOLDER

jobsub_submit --memory=2000MB --expected-lifetime=4h -G annie --disk=5GB --resource-provides=usage_model=OFFSITE --blacklist=Omaha,Swan,Wisconsin,RAL -f ${WCSIM_FILE_PATH} -f ${GENIE_FILE_PATH} -f ${INPUT_PATH}/run_container_job.sh -f ${INPUT_PATH}/MyToolAnalysis_grid.tar.gz -d OUTPUT $OUTPUT_FOLDER file://${INPUT_PATH}/grid_job.sh MC_toolchain_${RUN} 

echo "job name is: MC_toolchain_${RUN}"
echo "" 
