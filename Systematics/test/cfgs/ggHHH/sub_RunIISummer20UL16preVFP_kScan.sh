version=v7
tag=ggHHH_kScan
STAGE_DIR=/eos/home-a/athachay/workarea/trippleHiggs/flashggNtuples/RunIISummer20UL16preVFP/${version}/${tag}/
set -x
mkdir -p $STAGE_DIR
set +x
fggRunJobs.py \
    --load cfgs/ggHHH/RunIISummer20UL16preVFP_kappaLambdaScan.json \
    -d RunIISummer20UL16preVFP_${version}_${tag} \
    workspaceHHH_MC_withSyst.py \
    maxEvents=-1  \
    -n 400 \
    -q workday \
	--no-copy-proxy \
    --no-use-tarball \
	--stage-to=${STAGE_DIR}  
