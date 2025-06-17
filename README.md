# grid_wcsim
Submitting WCSim grid jobs. Tailored for the MC tuning analysis involving AmBe neutrons, Michel electrons, and throughgoing muons.

## Contents

- `AmBe_neutrons/` contains submission scripts for generating AmBe-like neutrons in WCSim. `send.py` will send jobs for 4 port positions (1, 5, 4, and 3, to match the 2024 AmBe calibration campaign) at all depths [-100:100cm, 50cm increments]. No AmBe housing is currently simulated. Neutron energy spectrum used is found in `AmBe_spectrum.dat`, pulled from Johann's work with RATPAC. 
- `dirt_muons/` is intended to simulate Michel electrons. Rather than simulating an electron swarm, simulating the mother dirt muons (though computationally more expensive and less efficient) will capture the correct vertex and energy distribution of the daughter electrons (which is modulated due to effects of negative muon decay in a water cherenkov detector). As mentioned, this is far less efficient: only ~0.5% of the mother dirt muons simulated will yield a Michel candidate after selection cuts are applied. `dirt_muons_genie.txt` is a list containing the vertex, energy, and direction information of genie muons from the WORLD samples originating in the dirt that pass through the FMV + tank (and miss the MRD geometry). Future TODO: improve efficiency by only simulated muons that SURVIVE selection cuts.
- `genie_muons/` is meant for simulating high energy muons that originate in the rock upstream the detector, and pass through all 3 detector components (FMV + tank + MRD). These throughgoing muons can be used to tune the simulation for CC events. Like the dirt muons, `thru_genie_muons.txt` is a list containing the vertex, direction, and energy of genie WORLD muons passing through all 3 detector components. This simulation is far more efficient than the dirt muons + Michels.

- `sourceme` must be included within the WCSim folder (and tarball) that is to be ran on the grid. It is needed to properly run the ./WCSim executable. 
