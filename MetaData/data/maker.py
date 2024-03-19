import os
import sys
import argparse
import json

dsetName=''
srcTxt=''
ext=''
evt='100'

parser = argparse.ArgumentParser()
parser.add_argument("--dSetName", help="Name of the dataset")
parser.add_argument("--fList", help="fileList")
parser.add_argument("--nEvent", help="nEvents to fill ",default='100')
parser.add_argument("--ext", help="extension",default=ext)

args = parser.parse_args()

dsetName=args.dSetName
srcTxt=args.fList
evt=int(args.nEvent)
ext=args.ext

fnames=[]
with  open(srcTxt) as f:
    lines=f.readlines()
    for l in lines:
        fnames.append(l[:-1])
print(" Number of files to be added : ",len(fnames))


outputDict={dsetName :{ 
                "dset_type" : "mc" , 
                'files' :[] ,
                "parent_n_units": None,
                "vetted": True,
                } }

txt=''
for fname in fnames:
    fDict={}
    fDict["name"]      = 'root://se01.indiacms.res.in:1094//cms'+fname
    fDict["nevents"]   = evt
    fDict["events"]    = evt
    fDict["totEvents"] = evt
    fDict["weights"]   = float(evt)
    outputDict[dsetName]["files"].append(fDict)

fout=open('dataset'+ext+'.json','w')
json.dump(outputDict,fout,indent=4)

