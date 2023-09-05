fggRunJobs.py \
	--load Era2018_legacy_v1_Summer19UL.json \
    -d jobs_Era2018_legacy_v1_Summer19UL \
    workspaceHHH_MC_GJet.py \
    maxEvents=-1  \
    -n 100 \
    -q workday \
	--no-copy-proxy \
    --no-use-tarball \
	--stage-to=/eos/home-a/athachay/workarea/trippleHiggs/flashggNtuples/v3/RunIISummer19UL18/MC_v3/
