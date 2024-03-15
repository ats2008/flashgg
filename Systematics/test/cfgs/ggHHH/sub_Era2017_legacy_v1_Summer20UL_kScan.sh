version=v7
tag=ggHHH_kScan
STAGE_DIR=/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/athachay/an/trippleHiggs/flashggNtuples/Era2017_legacy_v1_Summer20UL/$version/$tag/
set -x
mkdir -p $STAGE_DIR
set +x
fggRunJobs.py \
    --load cfgs/ggHHH/Era2017_legacy_v1_Summer20UL_kappaLScan.json \
    -d Era2017_legacy_v1_Summer20UL_${version}_${tag} \
    workspaceHHH_MC_withSyst.py \
    maxEvents=-1  \
    -n 400 \
    -q workday \
    --no-copy-proxy \
    --no-use-tarball \
	--stage-to=${STAGE_DIR}  

