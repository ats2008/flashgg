version=v4
tag=ttX
mkdir -p /eos/home-a/athachay/workarea/trippleHiggs/flashggNtuples/RunIISummer20UL18/$version/$tag/
fggRunJobs.py \
	--load cfgs/ttX/RunIISummer20UL18.json \
    -d RunIISummer20UL18_${version}_${tag}  \
    workspaceHHH_MC.py \
    maxEvents=-1  \
    --no-use-tarball \
    -n 400 \
    -q workday \
	--no-copy-proxy \
	--stage-to=/eos/home-a/athachay/workarea/trippleHiggs/flashggNtuples/RunIISummer20UL18/$version/$tag/  
