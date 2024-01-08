import glob,os
import argparse
import json

def getFilesAndDirs(pth):
    
    dirs=[]
    fls=[]
    
    flist=glob.glob(pth)

    for f in flist:
        if os.path.isdir(f):
            dirs.append(f)
        else:
            fls.append(f)
    
    return dirs,fls
 
def printSubText(procDict,nMax):
    for process in procDict:
        listToPrint=[]
        for i in range(nMax):
            if i not in procDict[process]:
                listToPrint.append(i)
        print("Process ",process)
        print("( ",end="")
        for i in listToPrint:
            print(i,end=" ")
        print(")\n ")
        print("\nqueue ",len(listToPrint))
        print()

def getAllCampaigns(campaign):
    
    if campaign=='Era2017_legacy_v1_Summer20UL':
        return ['Era2017_legacy_v1_Summer20UL','Era2017_legacy_v1_Summer19UL']
    if campaign=='Era2017_legacy_v1_Summer19UL':
        return ['Era2017_legacy_v1_Summer19UL','Era2017_legacy_v1_Summer20UL']
    if campaign=='Era2016_legacyPreVFP_v1_Summer20UL' :
        return [ 'Era2016_legacyPreVFP_v1_Summer20UL' , 'RunIISummer20UL16preVFP' ]
    if campaign=='RunIISummer20UL16preVFP' :
        return [ 'RunIISummer20UL16preVFP' , 'Era2016_legacyPreVFP_v1_Summer20UL' ]
    if campaign=='Era2016_legacyPostVFP_v1_Summer20UL':
        return [ 'Era2016_legacyPostVFP_v1_Summer20UL','Era2016_legacyPostVFP_v1_Summer19UL','RunIISummer20UL16postVFP'  ]
    if campaign=='Era2016_legacyPostVFP_v1_Summer19UL':
        return [ 'Era2016_legacyPostVFP_v1_Summer19UL','RunIISummer20UL16postVFP' , 'Era2016_legacyPostVFP_v1_Summer20UL' ]
    if campaign=='RunIISummer20UL16postVFP':
        return [ 'RunIISummer20UL16postVFP' , 'Era2016_legacyPostVFP_v1_Summer20UL','Era2016_legacyPostVFP_v1_Summer19UL' ]
    if campaign=='Era2018_legacy_v1_Summer20UL':
        return ['Era2018_legacy_v1_Summer20UL' , 'RunIISummer20UL18']
    if campaign=='RunIISummer20UL18':
        return ['RunIISummer20UL18' , 'Era2018_legacy_v1_Summer20UL']

    return []


CMSSW_BASE='/afs/cern.ch/work/a/athachay/private/trippleHiggs/hhhTo4b2g/flashGG/CMSSW_10_6_29/'
def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-i',"--inputFolder", help="Input direcotory path")
    parser.add_argument('-n',"--nMax", help="max job count",default=-1,type=int)
    parser.add_argument('-s',"--cstr", help="check string",default=None)
    parser.add_argument('-c',"--campaign", help="campaign name",default=None)
    parser.add_argument('-p',"--printSubScript", help="print the missing job details",default=False , action='store_true')
    args = parser.parse_args()
    #sstr=args.inputFolder+"*.root"
    sstr=args.inputFolder.replace("@@","*")
    


#    campaign_base=CMSSW_BASE+'/src/flashgg/MetaData/data/'+args.campaign+'/*.json'
#    dataset_db={}
#    flist=glob.glob(campaign_base)
#    print(f"     Loading {len(flist)} from {campaign_base}")
#    for fl in flist:
#        with open(fl) as f:
#            dataset_db.update(json.load(f))


    allDirsToProcess={}
    
    dirs,flist=getFilesAndDirs(sstr)
    allDirsToProcess[sstr] = flist
    for d in dirs:
        _,allDirsToProcess[d]=getFilesAndDirs(d+'/*.root')
    
    for ky in allDirsToProcess:
        print("="*100)
        print("\nProcessing the input search string : ",ky)
        flist=allDirsToProcess[ky]
        if len(flist) < 1:
            continue
        campaign=ky.replace('//','').split('/')[-3].replace('Era2016_legacyPostVFP_v1_Summer19UL','Era2016_legacyPostVFP_v1_Summer20UL')    
        campaign=ky.replace('//','').split('/')[-3]    
        if args.campaign :
            campaign=args.campaign #CMSSW_BASE+'/src/flashgg/MetaData/data/'+args.campaign+'/*.json'

        campaignList=getAllCampaigns( campaign )
        print("      Setting the campaign as ",campaign)
        print(  )
        campaign_base=CMSSW_BASE+'/src/flashgg/MetaData/data/'+campaign+'/*.json'
        
        
        dataset_db_store={}
        for campai in campaignList:
            campaign_base=CMSSW_BASE+'/src/flashgg/MetaData/data/'+campai+'/*.json'
            dataset_db={}
            flistDB=glob.glob(campaign_base)
            print(f"     Loading {len(flistDB)} from {campaign_base}")
            for fl in flistDB:
                with open(fl) as f:
                    dataset_db.update(json.load(f))
            dataset_db_store[campai] = dataset_db
            
        procDict={}
        for fname in flist:
            fname=fname.split('/')[-1]
            process='_'.join(fname.replace('output_','').split("_")[:-1])+'.root'
            if args.cstr:
                if args.cstr not in process:
                    continue

            outId=int(fname.split("_")[-1].replace('.root',''))
            if process not in procDict:
                procDict[process]=[]
            procDict[process].append(outId)
        
        for ky in procDict:
            print("- "*50)
            dataset=None
            sample = ky.replace(".root","")
            print("Sample  : ",sample)
            for dataset_db_ky in dataset_db_store:
                dataset_db = dataset_db_store[dataset_db_ky]
                for i in dataset_db:
                    if sample in i:
                        print("     Obtained Dataset details for  ",'/'.join(i.split('/')[:-2]), " from ",dataset_db_ky)
                        dataset=dataset_db[i]           
                        break
                if dataset:
                    break

            if not dataset:
                print(sample , " not found in campaign ",campaign)
                print("Available campaign keys are ",campaignList)
                #for i in dataset_db:
                #    print("\t",i[:120])
                return

            fileIdxMaps=[ [ i   for i in range(jid, len(dataset['files']) , args.nMax)] for jid in range(args.nMax) ]
            procesedFileIds=[]
            for i in procDict[ky]:

                procesedFileIds+=fileIdxMaps[int(i)]

            sumWeights=0.0
            processedWeights=0.0
            nFilesTotal=0
            for idx in range(len(dataset['files'])):
                if dataset['files'][idx]['bad']:
                    continue
                
                if 'weights' not in dataset['files'][idx]:
                    print(json.dumps(dataset['files'][idx],indent=4))
                    continue

                nFilesTotal+=1    
                sumWeights+=dataset['files'][idx]['weights']
                if idx in procesedFileIds:
                    processedWeights+=dataset['files'][idx]['weights']

            scaleFactor = sumWeights / (processedWeights + 1e-15)
            if len(procDict[ky]) > nFilesTotal:
                print()
                print( "\t CHECK THIS !! PROBABLY WRONG CAMPAIGN GOT PICKED UP " )
                print()
            print(f"     Number of Output files : ",len(procDict[ky]))
            print(f"     Number of Input uAOD files : ",nFilesTotal )
            print(f"     Sum Weights : {sumWeights:.2f}")
            print(f"     Processed Weights : {processedWeights:.2f}")
            print(f"     Scale Factor to scale the processed events : {scaleFactor:.4f}")

            if args.printSubScript :
                printSubText(procDict,min(args.nMax, nFilesTotal) )

            print()

if __name__=='__main__':
    main()

