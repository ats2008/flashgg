fggManageSamples.py list -C RunIISummer20UL18  | grep -A4 "Datasets in catalog"
echo 
echo  RunIISummer20UL18
echo 
fggManageSamples.py list -C RunIISummer20UL18  | grep -E "ttHJetToGG_M125|VHToGG_M125|VBFHToGG_M125|GluGluHToGG_M125"
echo 
echo  Era2017_legacy_v1_Summer20UL
echo 
fggManageSamples.py list -C Era2017_legacy_v1_Summer20UL | grep  -E "ttHJetToGG_M125|VHToGG_M125|VBFHToGG_M125|GluGluHToGG_M125"
echo 
echo  RunIISummer20UL16preVFP
echo 
fggManageSamples.py list -C RunIISummer20UL16preVFP |  grep  -E "ttHJetToGG_M125|VHToGG_M125|VBFHToGG_M125|GluGluHToGG_M125"
echo 
echo  RunIISummer20UL16postVFP
echo 
fggManageSamples.py list -C RunIISummer20UL16postVFP |  grep  -E "ttHJetToGG_M125|VHToGG_M125|VBFHToGG_M125|GluGluHToGG_M125"
echo 
echo  Era2016_legacyPreVFP_v1_Summer20UL
echo 
fggManageSamples.py list -C Era2016_legacyPreVFP_v1_Summer20UL |  grep  -E "ttHJetToGG_M125|VHToGG_M125|VBFHToGG_M125|GluGluHToGG_M125"
echo 
echo  Era2016_legacyPostVFP_v1_Summer20UL
echo 
fggManageSamples.py list -C Era2016_legacyPostVFP_v1_Summer20UL |  grep  -E "ttHJetToGG_M125|VHToGG_M125|VBFHToGG_M125|GluGluHToGG_M125"
