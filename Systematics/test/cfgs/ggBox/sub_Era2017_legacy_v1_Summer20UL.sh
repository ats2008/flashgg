version=v6
tag=ggBox
STAGE_DIR=/eos/home-a/athachay/workarea/trippleHiggs/flashggNtuples/Era2017_legacy_v1_Summer20UL/$version/$tag/
set -x
mkdir -p $STAGE_DIR
set +x
fggRunJobs.py \
    --load cfgs/ggBox/Era2017_legacy_v1_Summer20UL.json \
    -d Era2017_legacy_v1_Summer20UL_${version}_${tag} \
    workspaceHHH_MC.py \
    maxEvents=-1  \
    -n 600 \
    -q workday \
    --no-copy-proxy \
    --no-use-tarball \
	--stage-to=${STAGE_DIR}  

