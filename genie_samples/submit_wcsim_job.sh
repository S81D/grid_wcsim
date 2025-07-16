RUN=$1

# WORLD samples only run ~600 events per 20k GENIE file aka need low grid resources 

export INPUT_PATH=/pnfs/annie/scratch/users/doran/genie_wcsim_grid/  
export GENIE=/pnfs/annie/persistent/simulations/genie3/G1810a0211a/standardv1.0/world/
export DIRT=/pnfs/annie/persistent/simulations/g4dirt/G1810a0211a/standardv1.0/world/

echo ""
echo "submitting job..."
echo ""

OUTPUT_FOLDER=/pnfs/annie/scratch/users/doran/output/genie_wcsim
mkdir -p $OUTPUT_FOLDER                                                 

# wrapper script to submit your grid job
jobsub_submit --memory=2000MB --expected-lifetime=2h -G annie --disk=3GB --resource-provides=usage_model=OFFSITE --blacklist=Omaha,Swan,Wisconsin,SU-ITS,RAL -f ${INPUT_PATH}/WCSim.tar.gz -f ${INPUT_PATH}/wcsim_container.sh -f ${DIRT}/annie_tank_flux.${RUN}.root -f ${GENIE}/gntp.${RUN}.ghep.root -d OUTPUT $OUTPUT_FOLDER file://${INPUT_PATH}/run_job.sh ${RUN}
