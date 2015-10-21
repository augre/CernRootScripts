#!/bin/bash
time_stamp=$(date +%Y_%m_%d_%H_%M_%S)
mkdir "${time_stamp}$1"
cd "${time_stamp}$1"
scp "$1"@xfer01-ext.palmetto.clemson.edu:/scratch1/"$1"/Root_step10/Dosimetry_Detector_* ./
hadd Dosimetry_Detector_tot.root Dosimetry_Detector_*
mkdir out && cd out
scp "$1"@user.palmetto.clemson.edu:/home/"$1"/geant4_workdir/spinotron/out/* ./
#ssh tkorokn@user.palmetto.clemson.edu 'rm /home/tkorokn/geant4_workdir/spinotron/out/*'
