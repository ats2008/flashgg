fggRunJobs.py \
	--load Era2017_legacy_v1_Summer20UL_sig.json \
    -d jobs_Era2017_legacy_v1_Summer20UL_sig \
    workspaceHHH_MC.py \
    maxEvents=-1  \
    -n 400 \
    -q workday \
	--no-copy-proxy \
	--stage-to=/eos/home-a/athachay/workarea/trippleHiggs/flashggNtuples/v3/Era2017_legacy_v1_Summer20UL_sig
