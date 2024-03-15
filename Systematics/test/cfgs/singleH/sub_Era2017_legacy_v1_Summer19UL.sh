version=v6
tag=singleH
STAGE_DIR=/eos/home-a/athachay/workarea/trippleHiggs/flashggNtuples/Era2017_legacy_v1_Summer19UL/$version/$tag/
set -x
mkdir -p $STAGE_DIR
set +x
fggRunJobs.py \
    --load cfgs/singleH/Era2017_legacy_v1_Summer20UL.json \
    -d Era2017_legacy_v1_Summer19UL_${version}_${tag} \
    workspaceHHH_MC_withSyst.py \
    maxEvents=-1  \
    -n 400 \
    -q workday --nCondorCpu 3 \
    --no-copy-proxy \
    --no-use-tarball \
	--stage-to=${STAGE_DIR}  

