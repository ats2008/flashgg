import glob,os
import argparse

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



def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-i',"--inputFolder", help="Input direcotory path")
    parser.add_argument('-n',"--nMax", help="max job count",default=-1,type=int)
    parser.add_argument('-s',"--cstr", help="check string",default=None)
    args = parser.parse_args()
    #sstr=args.inputFolder+"*.root"
    sstr=args.inputFolder.replace("@@","*")
    

    allDirsToProcess={}
    
    dirs,flist=getFilesAndDirs(sstr)
    allDirsToProcess[sstr] = flist
    for d in dirs:
        _,allDirsToProcess[d]=getFilesAndDirs(d+'/*.root')
    
    for ky in allDirsToProcess:
        print("\nProcessing the input search string : ",ky)
        flist=allDirsToProcess[ky]
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
        
        print("Number of processed files : ")
        for ky in procDict:
            print("\t",ky,"\t : \t",len(procDict[ky]))
        
        if args.nMax > 0 :
            printSubText(procDict,args.nMax)

if __name__=='__main__':
    main()

