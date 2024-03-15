version=v6
tag=gjet
STAGE_DIR=/eos/home-a/athachay/workarea/trippleHiggs/flashggNtuples/Era2018_legacy_v1_Summer19UL/${version}/${tag}/
set -x
mkdir -p $STAGE_DIR
set +x
fggRunJobs.py \
	--load cfgs/gjet/Era2018_legacy_v1_Summer19UL.json \
    -d Era2018_legacy_v1_Summer19UL_${version}_${tag}  \
    workspaceHHH_MC.py \
    maxEvents=-1  \
    -n 800 \
    -q workday \
    --no-use-tarball \
	--no-copy-proxy \
	--stage-to=${STAGE_DIR}
