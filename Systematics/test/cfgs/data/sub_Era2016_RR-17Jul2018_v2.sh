version=v6
tag=doubleH
STAGE_DIR=/eos/home-a/athachay/workarea/trippleHiggs/flashggNtuples/Era2016_RR-17Jul2018_v2/$version/$tag/
set -x
mkdir -p $STAGE_DIR
set +x
fggRunJobs.py \
    --load cfgs/data/Era2016_RR-17Jul2018_v2.json \
    -d Era2016_RR-17Jul2018_v2_${version}_${tag} \
    workspaceHHH_MC_withSyst.py \
    maxEvents=-1  \
    -n 600 \
    -q workday \
    --no-copy-proxy \
    --no-use-tarball \
	--stage-to=${STAGE_DIR}  

