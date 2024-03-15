version=v6
tag=ggBox
STAGE_DIR=/eos/home-a/athachay/workarea/trippleHiggs/flashggNtuples/RunIISummer20UL16postVFP/$version/$tag/
set -x
mkdir -p $STAGE_DIR
set +x
fggRunJobs.py \
	--load cfgs/ggBox/RunIISummer20UL16postVFP.json \
    -d RunIISummer20UL16postVFP_${version}_${tag} \
    workspaceHHH_MC.py \
    maxEvents=-1  \
    -n 600 \
    -q workday \
	--no-copy-proxy \
    --no-use-tarball \
	--stage-to=${STAGE_DIR}  
