#!/bin/bash

# Copy wcsim production output from grid scratch to persistent storage,
# sorting each file type into the corresponding persistent subdirectory.
#
# Usage:
#   ./copy_wcsim_output.sh <scratch_path> <persistent_path>
#
# Example:
#   ./copy_wcsim_output.sh \
#       /pnfs/annie/scratch/users/doran/output/WCSim_production/run01 \
#       /pnfs/annie/persistent/users/doran/GENIE-016-empirical-model/wcsim/
#
# Expects <persistent_path> to contain (or be able to create) the
# subdirectories: annie  logs
#
# Running with nohup:
# nohup bash copy_wcsim_output.sh /pnfs/annie/scratch/users/doran/output/WCSim_production/run01 /pnfs/annie/persistent/users/doran/GENIE-016-empirical-model/wcsim >> copy_wcsim_output.log 2>&1 &
#

scratch_path=$1
persistent_path=$2

if [ -z "$scratch_path" ] || [ -z "$persistent_path" ]; then
    echo "Usage: $0 <scratch_path> <persistent_path>"
    exit 1
fi

WCSIM_DIR="${persistent_path}/pmts/"

# create destination folders and make them editable/writable
mkdir -p "$WCSIM_DIR"
chmod 777 "$WCSIM_DIR"

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

copy_filetype "wcsim_*.root"   "$WCSIM_DIR" "WCSIM"

echo ""
echo "Transfer complete."
echo ""
