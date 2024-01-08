version=v6
tag=data
STAGE_DIR=/eos/home-a/athachay/workarea/trippleHiggs/flashggNtuples/Era2016_legacyPostVFP_v1_Summer19UL/$version/$tag/
set -x
mkdir -p $STAGE_DIR
set +x
fggRunJobs.py \
	--load cfgs/data/Era2016_legacyPostVFP_v1_Summer19UL.json \
    -d Era2016_legacyPostVFP_v1_Summer19UL_${version}_${tag} \
    workspaceHHH_Data.py \
    maxEvents=-1  \
    -n 600 \
    -q workday \
	--no-copy-proxy \
    --no-use-tarball \
	--stage-to=${STAGE_DIR}  
