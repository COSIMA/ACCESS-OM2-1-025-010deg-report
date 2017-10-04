#!/usr/bin/env sh

# set -e

nml_diff.py --format latex /Users/andy/Documents/COSIMA/github/OceansAus/access-om2/control/*jra*/ocean/input.nml > ocean_input_nml.tex

nml_diff.py --format latex /Users/andy/Documents/COSIMA/github/OceansAus/access-om2/control/*jra*/atmosphere/input_atm.nml > input_atm_nml.tex

nml_diff.py --format latex /Users/andy/Documents/COSIMA/github/OceansAus/access-om2/control/*jra*/ice/input_ice.nml > input_ice_nml.tex

nml_diff.py --format latex /Users/andy/Documents/COSIMA/github/OceansAus/access-om2/control/*jra*/ice/input_ice_gfdl.nml > input_ice_gfdl_nml.tex

nml_diff.py --format latex /Users/andy/Documents/COSIMA/github/OceansAus/access-om2/control/*jra*/ice/input_ice_monin.nml > input_ice_monin_nml.tex

nml_diff.py --format latex /Users/andy/Documents/COSIMA/github/OceansAus/access-om2/control/*jra*/ice/cice_in.nml > cice_in_nml.tex

exit 0