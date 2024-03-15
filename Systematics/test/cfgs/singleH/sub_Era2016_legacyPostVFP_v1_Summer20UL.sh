version=v6
tag=singleH
STAGE_DIR=/eos/home-a/athachay/workarea/trippleHiggs/flashggNtuples/Era2016_legacyPostVFP_v1_Summer19UL/$version/$tag/
set -x
mkdir -p $STAGE_DIR
set +x
fggRunJobs.py \
	--load cfgs/singleH/Era2016_legacyPostVFP_v1_Summer20UL.json \
    -d Era2016_legacyPostVFP_v1_Summer20UL_${version}_${tag} \
    workspaceHHH_MC_withSyst.py \
    maxEvents=-1  \
    -n 450 \
    -q workday --nCondorCpu 3 \
	--no-copy-proxy \
    --no-use-tarball \
	--stage-to=${STAGE_DIR}  
