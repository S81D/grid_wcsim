#!/bin/bash
# Submit GENIE production jobs to the grid
# Steven Doran (based on James Minock's code and on other people's code as usual)

# ********************** INPUTS ********************** #
GRID_USER=doran
INPUT_FOLDER=/pnfs/annie/scratch/users/${GRID_USER}/grid_wcsim/GENIE_G4Dirt_production/
OUTPUT_FOLDER=/pnfs/annie/scratch/users/${GRID_USER}/output/GENIE_production/

# If using a local fork of GENIE
USE_LOCAL_GENIE=true  # enable
GENIE_TAR_NAME=GENIE.tar.gz       # these don't matter if you're not using a local fork
GENIE_FOLDER_NAME=GENIE-v3-O16

# MAKE SURE TO INCLUDE THE FOLLOWING FILES IN YOUR INPUT DIR (IF USING LOCAL FORK OF GENIE):
# - GENIE tar file
# - modified Setup_GENIE.sh (in lib/ folder)

# FOR ALL JOBS, MAKE SURE YOU HAVE THE FOLLOWING FILES IN YOUR INPUT/LIB DIR:
# - gxspl-FNALsmall.xml (too large to include in github)

# ---------------------------------------------------- #
# RUN PRODUCTION (enable ONE of the following)

RUNS=$(seq 0 1)     # consecutive (default)

#RUNS=(99)          # specific re-processing
# ---------------------------------------------------- #

# Job properties 
LIFETIME=4            # hr
DISK_SPACE=10         # GB
MEMORY_SPACE=4000     # MB
ONSITE_JOB=true       # FNAL / onsite (true) vs offsite (false)
# **************************************************** #

# Flux files for GENIE (4000 in total) --> each file was produced with a random combination of 50 official ANNIE gsimple flux files
# (to avoid the stripiness issue observed)
FLUX_FOLDER=/pnfs/annie/persistent/users/jminock/flux/

# Adjust if needed --> in case you want a different geometry file
GEO_FILE=annie_v07.gdml

mkdir -p "${OUTPUT_FOLDER}"
chmod +x "${INPUT_FOLDER}/lib/GENIE_grid.sh"

if [ "$USE_LOCAL_GENIE" = true ]; then
    echo ""
    echo "Will use a local fork of GENIE (${GENIE_FOLDER_NAME}, attached as a tar-file: ${GENIE_TAR_NAME})"
    echo ""
fi

EXTRA_FILES=""
EXTRA_ARGS="${USE_LOCAL_GENIE}"

if [ "$USE_LOCAL_GENIE" = true ]; then
    EXTRA_FILES="-f ${INPUT_FOLDER}/${GENIE_TAR_NAME}"
    EXTRA_ARGS="${USE_LOCAL_GENIE} ${GENIE_TAR_NAME} ${GENIE_FOLDER_NAME}"
fi

echo ""
echo "Sending jobs..."
echo ""

# Quick check to see if necessary files are present
for FILE in \
    "${INPUT_FOLDER}/lib/${GEO_FILE}" \
    "${INPUT_FOLDER}/lib/run_annie_genie.sh" \
    "${INPUT_FOLDER}/lib/gxspl-FNALsmall.xml" \
    "${INPUT_FOLDER}/lib/rub_the_lamp.sh" \
    "${INPUT_FOLDER}/lib/GENIE_grid.sh"
do
    [ -f "$FILE" ] || { echo "Missing $FILE"; exit 1; }
done

if [ "$USE_LOCAL_GENIE" = true ]; then
    [ -f "${INPUT_FOLDER}/${GENIE_TAR_NAME}" ] || {
        echo "Missing ${INPUT_FOLDER}/${GENIE_TAR_NAME}"
        exit 1
    }

    [ -f "${INPUT_FOLDER}/lib/Setup_GENIE.sh" ] || {
        echo "Missing ${INPUT_FOLDER}/lib/Setup_GENIE.sh"
        exit 1
    }
fi

if [ "$ONSITE_JOB" = true ]; then
    RESOURCE_ARGS="--resource-provides=usage_model=DEDICATED,OPPORTUNISTIC"
else
    RESOURCE_ARGS="--resource-provides=usage_model=OFFSITE --blacklist=Omaha,Swan,Wisconsin,SU-ITS,RAL"
fi

# If re-doing runs, include them in this list
#redoruns=(4661)
#for RUN in "${redoruns[@]}"

# Alternatively, send a batch
for RUN in {0..9}
do
    echo ""
    if [ ! -f "${FLUX_FOLDER}/gsimple_flux_${RUN}.root" ]; then
        echo "Could not find ${FLUX_FOLDER}/gsimple_flux_${RUN}.root! Skipping..."
        continue
    fi
    if [ -f "${OUTPUT_FOLDER}/gntp.${RUN}.ghep.root" ]; then
        echo "gntp.${RUN}.ghep.root already present in ${OUTPUT_FOLDER} directory! Skipping..."
        continue
    fi
    echo "Submitting job... ${RUN}"
    jobsub_submit --memory=${MEMORY_SPACE}MB \
            --expected-lifetime=${LIFETIME}h \
            -G annie \
            --disk=${DISK_SPACE}GB \
            ${RESOURCE_ARGS} \
            -f "${INPUT_FOLDER}/lib/${GEO_FILE}" \
            -f "${INPUT_FOLDER}/lib/run_annie_genie.sh" \
            -f "${INPUT_FOLDER}/lib/gxspl-FNALsmall.xml" \
            -f "${FLUX_FOLDER}/gsimple_flux_${RUN}.root" \
            -f "${INPUT_FOLDER}/lib/rub_the_lamp.sh" \
            -f "${INPUT_FOLDER}/lib/Setup_GENIE.sh" \
            "$EXTRA_FILES" \
            -d OUTPUT "${OUTPUT_FOLDER}" \
            file://"${INPUT_FOLDER}"/lib/GENIE_grid.sh \
            "$RUN" \
            "$GRID_USER" \
            "$GEO_FILE" \
            ${EXTRA_ARGS}
done

echo ""
echo "Done!"
echo ""
