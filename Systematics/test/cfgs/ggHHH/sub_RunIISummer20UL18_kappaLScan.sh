version=v7
tag=ggHHH_kScan
STAGE_DIR=/eos/home-a/athachay/workarea/trippleHiggs/flashggNtuples/RunIISummer20UL18/${version}/${tag}/
set -x
mkdir -p $STAGE_DIR
set +x
fggRunJobs.py \
	--load cfgs/ggHHH/RunIISummer20UL18_kappaLambdaScan.json \
    -d RunIISummer20UL18_${version}_${tag}  \
    workspaceHHH_MC_withSyst.py \
    maxEvents=-1  \
    -n 400 \
    -q workday \
    --no-use-tarball \
	--no-copy-proxy \
    --nCondorCpu 4 \
	--stage-to=${STAGE_DIR}
