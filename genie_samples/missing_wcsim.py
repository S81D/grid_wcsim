import os, sys, re

# script to report which wcsim_N.root files are missing given the expected range of run numbers

'''
usage: python3 missing_wcsim.py <scratch_path> <run_start> <run_end>

example:
    python3 missing_wcsim.py \
        /pnfs/annie/scratch/users/doran/output/G4Dirt_production/run01 \
        0 3999

output:

Expected runs: 0 - 3999
Number of expected wcsim files:  4000
Number of present wcsim files:  3998
Number of missing wcsim files:  2
Missing wcsim files (run numbers):  [46, 47]
'''


def missing_wcsim(scratch_path, run_start, run_end):

    expected_runs = set(range(run_start, run_end + 1))

    pattern = re.compile(r'^wcsim_(\d+)\.root$')
    present_runs = set()
    for fname in os.listdir(scratch_path):
        match = pattern.match(fname)
        if match:
            present_runs.add(int(match.group(1)))

    missing_runs = sorted(expected_runs - present_runs)

    print("\nExpected runs: {} - {}".format(run_start, run_end))
    print("Number of expected wcsim files: ", len(expected_runs))
    print("Number of present wcsim files: ", len(present_runs))
    print("Number of missing wcsim files: ", len(missing_runs))
    print("Missing wcsim files (run numbers): ", missing_runs)
    print('\n')

    return missing_runs


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 missing_wcsim.py <scratch_path> <run_start> <run_end>")
        sys.exit(1)

    scratch_path = sys.argv[1]
    run_start = int(sys.argv[2])
    run_end = int(sys.argv[3])

    missing_wcsim(scratch_path, run_start, run_end)
