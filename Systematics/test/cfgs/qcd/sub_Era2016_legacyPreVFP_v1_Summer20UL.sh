version=v6
tag=qcd
STAGE_DIR=/eos/home-a/athachay/workarea/trippleHiggs/flashggNtuples/Era2016_legacyPreVFP_v1_Summer20UL/${version}/${tag}/
set -x
mkdir -p $STAGE_DIR
set +x
fggRunJobs.py \
    --load cfgs/qcd/Era2016_legacyPreVFP_v1_Summer20UL.json \
    -d Era2016_legacyPreVFP_v1_Summer20UL_${version}_${tag} \
    workspaceHHH_MC.py \
    maxEvents=-1  \
    -n 400 \
    -q workday \
	--no-copy-proxy \
    --no-use-tarball \
	--stage-to=${STAGE_DIR}  