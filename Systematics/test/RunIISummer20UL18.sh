fggRunJobs.py \
	--load RunIISummer20UL18.json \
    -d RunIISummer20UL18_v3  \
    workspaceHHH_MC.py \
    maxEvents=-1  \
    --no-use-tarball \
    -n 400 \
    -q workday \
	--no-copy-proxy \
	--stage-to=/eos/home-a/athachay/workarea/trippleHiggs/flashggNtuples/v2/RunIISummer19UL18/MC_v3/  \
    --summary
