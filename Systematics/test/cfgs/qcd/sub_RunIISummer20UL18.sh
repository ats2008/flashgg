version=v6
tag=qcd
STAGE_DIR=/eos/home-a/athachay/workarea/trippleHiggs/flashggNtuples/RunIISummer20UL18/${version}/${tag}/
set -x
mkdir -p $STAGE_DIR
set +x
fggRunJobs.py \
	--load cfgs/qcd/RunIISummer20UL18.json \
    -d RunIISummer20UL18_${version}_${tag}  \
    workspaceHHH_MC.py \
    maxEvents=-1  \
    -n 400 \
    -q workday \
    --no-use-tarball \
	--no-copy-proxy \
	--stage-to=${STAGE_DIR}
