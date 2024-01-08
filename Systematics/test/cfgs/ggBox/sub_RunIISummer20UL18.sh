version=v6
tag=ggBox
STAGE_DIR=/eos/home-a/athachay/workarea/trippleHiggs/flashggNtuples/RunIISummer20UL18/${version}/${tag}/
set -x
mkdir -p $STAGE_DIR
set +x
fggRunJobs.py \
	--load cfgs/ggBox/RunIISummer20UL18.json \
    -d RunIISummer20UL18_${version}_${tag}  \
    workspaceHHH_MC.py \
    maxEvents=-1  \
    -n 600 \
    -q workday \
    --no-use-tarball \
	--no-copy-proxy \
	--stage-to=${STAGE_DIR}
