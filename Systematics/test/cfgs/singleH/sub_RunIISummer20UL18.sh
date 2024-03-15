version=v6
tag=singleH
STAGE_DIR=/eos/home-a/athachay/workarea/trippleHiggs/flashggNtuples/RunIISummer20UL18/${version}/${tag}/
set -x
mkdir -p $STAGE_DIR
set +x
fggRunJobs.py \
	--load cfgs/singleH/RunIISummer20UL18.json \
    -d RunIISummer20UL18_${version}_${tag}  \
    workspaceHHH_MC_withSyst.py \
    maxEvents=-1  \
    -n 400 \
    -q workday --nCondorCpu 3 \
    --no-use-tarball \
	--no-copy-proxy \
	--stage-to=${STAGE_DIR}
