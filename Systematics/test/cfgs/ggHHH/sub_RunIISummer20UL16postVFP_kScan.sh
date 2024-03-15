version=v7
tag=ggHHH_kScan
STAGE_DIR=/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/athachay/an/trippleHiggs/flashggNtuples/RunIISummer20UL16postVFP/$version/$tag/
set -x
mkdir -p $STAGE_DIR
set +x
fggRunJobs.py \
	--load cfgs/ggHHH/RunIISummer20UL16postVFP_kappaLambdaScan.json \
    -d RunIISummer20UL16postVFP_${version}_${tag} \
    workspaceHHH_MC_withSyst.py \
    maxEvents=-1  \
    -n 450 \
    -q workday \
	--no-copy-proxy \
    --no-use-tarball \
	--stage-to=${STAGE_DIR}  
