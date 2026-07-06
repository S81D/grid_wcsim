#!/bin/bash

# Copy GENIE production output from grid scratch to persistent storage,
# sorting each file type into the corresponding persistent subdirectory.
#
# Usage:
#   ./copy_genie_output.sh <scratch_path> <persistent_path>
#
# Example:
#   ./copy_genie_output.sh \
#       /pnfs/annie/scratch/users/doran/output/GENIE_production/run01 \
#       /pnfs/annie/persistent/users/doran/GENIE-016-empirical-model/genie
#
# Expects <persistent_path> to contain (or be able to create) the
# subdirectories: ghep  gst  logs  POT

scratch_path=$1
persistent_path=$2

if [ -z "$scratch_path" ] || [ -z "$persistent_path" ]; then
    echo "Usage: $0 <scratch_path> <persistent_path>"
    exit 1
fi

GHEP_DIR="${persistent_path}/ghep"
GST_DIR="${persistent_path}/gst"
LOG_DIR="${persistent_path}/logs"
POT_DIR="${persistent_path}/POT"

# create destination folders and make them editable/writable
mkdir -p "$GHEP_DIR" "$GST_DIR" "$LOG_DIR" "$POT_DIR"
chmod 777 "$GHEP_DIR" "$GST_DIR" "$LOG_DIR" "$POT_DIR"

# rsync flags:
#   -a                  archive mode (preserves perms/timestamps)
#   -v                  verbose, prints each file as it's copied
#   --ignore-existing   skip files already present at destination
#                       (replaces the old per-file file_exists check;
#                        does NOT overwrite/update existing files)
#   --info=progress2    running total progress for the whole batch
RSYNC_FLAGS="-av --ignore-existing --info=progress2"

copy_filetype() {
    local pattern=$1
    local dest=$2
    local label=$3

    echo ""
    echo "=== Copying ${label} files (${pattern}) ==="
    echo ""

    # quoting left off the pattern on purpose so the shell expands the glob
    # into individual filenames before rsync sees them (bulk single call)
    rsync ${RSYNC_FLAGS} ${scratch_path}/${pattern} "${dest}/"

    echo ""
    echo "=== ${label} files done ==="
    echo ""
}

# Order: ghep -> gst -> POT -> logs (ghep.log.gz, maxpl, BNBFlux)
copy_filetype "gntp.*.ghep.root"   "$GHEP_DIR" "GHEP"
copy_filetype "gntp.*.gst.root"    "$GST_DIR"  "GST"
copy_filetype "pot_*.csv"          "$POT_DIR"  "POT"
copy_filetype "gntp.*.ghep.log.gz" "$LOG_DIR"  "GHEP LOG"
copy_filetype "ANNIE-*.maxpl.xml"  "$LOG_DIR"  "MAXPL"
copy_filetype "BNBFlux*.xml"       "$LOG_DIR"  "BNBFlux"

echo ""
echo "All transfers complete."
echo ""
