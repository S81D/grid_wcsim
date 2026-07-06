import os, sys, re

# script to report which gntp.N.ghep.root files are missing from a GENIE
# production scratch directory, given the expected range of run numbers

'''
usage: python3 missing_ghep.py <scratch_path> <run_start> <run_end>

example:
    python3 missing_ghep.py \
        /pnfs/annie/scratch/users/doran/output/GENIE_production/run01 \
        0 3999

output:

Expected runs: 0 - 3999
Number of expected ghep files:  4000
Number of present ghep files:  3998
Number of missing ghep files:  2
Missing GHEP files (run numbers):  [46, 47]
'''


def missing_ghep(scratch_path, run_start, run_end):

    expected_runs = set(range(run_start, run_end + 1))

    pattern = re.compile(r'^gntp\.(\d+)\.ghep\.root$')
    present_runs = set()
    for fname in os.listdir(scratch_path):
        match = pattern.match(fname)
        if match:
            present_runs.add(int(match.group(1)))

    missing_runs = sorted(expected_runs - present_runs)

    print("\nExpected runs: {} - {}".format(run_start, run_end))
    print("Number of expected ghep files: ", len(expected_runs))
    print("Number of present ghep files: ", len(present_runs))
    print("Number of missing ghep files: ", len(missing_runs))
    print("Missing GHEP files (run numbers): ", missing_runs)
    print('\n')

    return missing_runs


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 missing_ghep.py <scratch_path> <run_start> <run_end>")
        sys.exit(1)

    scratch_path = sys.argv[1]
    run_start = int(sys.argv[2])
    run_end = int(sys.argv[3])

    missing_ghep(scratch_path, run_start, run_end)
