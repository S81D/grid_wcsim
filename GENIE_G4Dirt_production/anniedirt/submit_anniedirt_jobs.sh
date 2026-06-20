#!/bin/bash
# Submit GENIE production jobs to the grid
# Steven Doran (based on James Minock's code and on other people's code as usual)

# ********************** INPUTS ********************** #
GRID_USER=doran
INPUT_FOLDER=/pnfs/annie/scratch/users/${GRID_USER}/grid_wcsim/GENIE_G4Dirt_production/anniedirt/
OUTPUT_FOLDER=/pnfs/annie/scratch/users/${GRID_USER}/output/G4Dirt_production/

# MODIFY AS NEEDED (genie file path)
GENIE_PATH=/pnfs/annie/persistent/users/${GRID_USER}/GENIE/

# ---------------------------------------------------- #
# RUN PRODUCTION (enable ONE of the following)

RUNS=$(seq 0 1)        # consecutive (default)

#RUNS="435 2282"       # specific re-processing
# ---------------------------------------------------- #

# Job properties 
LIFETIME=4            # hr
DISK_SPACE=10         # GB
MEMORY_SPACE=4000     # MB
ONSITE_JOB=true       # FNAL / onsite (true) vs offsite (false)
# **************************************************** #

# Adjust if needed --> in case you want a different geometry file
GEO_FILE=annie_v07.gdml

mkdir -p "${OUTPUT_FOLDER}"
chmod +x "${INPUT_FOLDER}/lib/g4dirt_grid.sh"

echo ""
echo "Sending jobs..."
echo ""

# Quick check to see if necessary files are present
for FILE in \
    "${INPUT_FOLDER}/lib/${GEO_FILE}" \
    "${INPUT_FOLDER}/lib/g4dirt_grid.sh" \
    "${INPUT_FOLDER}/lib/gdml.tar.gz" \
    "${INPUT_FOLDER}/lib/run_g4dirt_container.sh"
do
    [ -f "$FILE" ] || { echo "Missing $FILE"; exit 1; }
done

if [ "$ONSITE_JOB" = true ]; then
    RESOURCE_ARGS="--resource-provides=usage_model=DEDICATED,OPPORTUNISTIC"
else
    RESOURCE_ARGS="--resource-provides=usage_model=OFFSITE --blacklist=Omaha,Swan,Wisconsin,SU-ITS,RAL"
fi


for RUN in ${RUNS}
do
    echo ""
    if [ ! -f "${GENIE_PATH}/gntp.${RUN}.ghep.root" ]; then
        echo "Could not find ${GENIE_PATH}/gntp.${RUN}.ghep.root! Skipping..."
        continue
    fi
    if [ -f "${OUTPUT_FOLDER}/annie_tank_flux.${RUN}.root" ]; then
        echo "annie_tank_flux.${RUN}.root already present in ${OUTPUT_FOLDER} directory! Skipping..."
        continue
    fi
    echo "Submitting job... ${RUN}"
    jobsub_submit --memory=${MEMORY_SPACE}MB \
            --expected-lifetime=${LIFETIME}h \
            -G annie \
            --disk=${DISK_SPACE}GB \
            ${RESOURCE_ARGS} \
            -f "${INPUT_FOLDER}/lib/${GEO_FILE}" \
            -f "${GENIE_PATH}/gntp.${RUN}.ghep.root" \
            -f "${INPUT_FOLDER}/lib/gdml.tar.gz" \
            -f "${INPUT_FOLDER}/lib/run_g4dirt_container.sh" \
            -d OUTPUT "${OUTPUT_FOLDER}" \
            file://"${INPUT_FOLDER}"/lib/g4dirt_grid.sh \
            "$RUN" \
            "$GRID_USER" \
            "$GEO_FILE"
done

echo ""
echo "Done!"
echo ""
