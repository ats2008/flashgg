version=v6
tag=gjet
STAGE_DIR=/eos/home-a/athachay/workarea/trippleHiggs/flashggNtuples/Era2016_legacyPostVFP_v1_Summer19UL/$version/$tag/
set -x
mkdir -p $STAGE_DIR
set +x
fggRunJobs.py \
	--load cfgs/gjet/Era2016_legacyPostVFP_v1_Summer20UL.json \
    -d Era2016_legacyPostVFP_v1_Summer20UL_${version}_${tag} \
    workspaceHHH_MC.py \
    maxEvents=-1  \
    -n 800 \
    -q workday \
	--no-copy-proxy \
    --no-use-tarball \
	--stage-to=${STAGE_DIR}  
