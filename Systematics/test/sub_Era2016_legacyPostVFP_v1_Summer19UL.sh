version=v4
tag=ttX
STAGE_DIR=/eos/home-a/athachay/workarea/trippleHiggs/flashggNtuples/Era2016_legacyPostVFP_v1_Summer19UL/$version/$tag/
fggRunJobs.py \
	--load Era2016_legacyPostVFP_v1_Summer19UL.json \
    -d Era2016_legacyPostVFP_v1_Summer19UL_${version}_${tag} \
    workspaceHHH_MC.py \
    maxEvents=-1  \
    -n 400 \
    -q workday \
	--no-copy-proxy \
    --no-use-tarball \
	--stage-to=${STAGE_DIR}  
