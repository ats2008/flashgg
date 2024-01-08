version=v4
tag=ttX
STAGE_DIR=/eos/home-a/athachay/workarea/trippleHiggs/flashggNtuples/Era2017_legacy_v1_Summer19UL/$version/$tag/
mkdir -p $STAGE_DIR
fggRunJobs.py \
    --load cfgs/ttX/Era2017_legacy_v1_Summer19UL.json \
    -d Era2017_legacy_v1_Summer19UL_${version}_${tag} \
    --no-use-tarball \
    workspaceHHH_MC.py \
    maxEvents=-1  \
    -n 400 \
    -q workday \
    --no-copy-proxy \
	--stage-to=${STAGE_DIR}  
