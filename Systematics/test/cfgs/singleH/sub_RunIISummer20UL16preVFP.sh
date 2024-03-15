version=v6
tag=singleH
STAGE_DIR=/eos/home-a/athachay/workarea/trippleHiggs/flashggNtuples/Era2016_legacyPreVFP_v1_Summer20UL/${version}/${tag}/
set -x
mkdir -p $STAGE_DIR
set +x
fggRunJobs.py \
    --load cfgs/singleH/RunIISummer20UL16preVFP.json \
    -d RunIISummer20UL16preVFP_${version}_${tag} \
    workspaceHHH_MC_withSyst.py \
    maxEvents=-1  \
    -n 400 \
    -q workday --nCondorCpu 3 \
	--no-copy-proxy \
    --no-use-tarball \
	--stage-to=${STAGE_DIR}  
