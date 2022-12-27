fggRunJobs.py \
	--load Era2018_legacy_v1_Summer19_data.json \
    -d jobs_Era2018_legacy_v1_Summer19_data \
    workspaceHHH_Data.py \
    maxEvents=-1  \
    -n 400 \
    -q workday \
	--no-copy-proxy \
	--stage-to=/eos/home-a/athachay/workarea/trippleHiggs/flashggNtuples/v3/Era2018_legacy_v1_Summer19_data_v3p1
