import os,argparse,subprocess,sys,tempfile,ROOT,json

parser = argparse.ArgumentParser()
parser.add_argument("--inDsTxt",default="",
        help=" A text file with list of all input datasets")
parser.add_argument("--id_text",default="",
        help="identifier text for your output container user.<userid>.<gn1_str>.<timestamp>.gn2_<ID_TEXT> Example: --id_text mc16a_v01. The version number is not tracked by the script. Please give that explicitly")
parser.add_argument("--nickname",default="",
        help="In case your grid user name is different from your CERN login id use this option to tell the script your gridnickname")
parser.add_argument("--site",default="ANALY_CERN",
        help="Site where the jobs are submitted. If you are not sure, use the defaults")
parser.add_argument("--lsf",action='store_true',
        help='submit jobs from a batch node')
parser.add_argument("--isData",action='store_true',
        help='for data jobs set this flag to avoid computing the sumWeights')
parser.add_argument("--isSys",action='store_true',
        help='for data jobs set this flag to avoid computing the sumWeights')
parsed = parser.parse_args()

# Check if we have the submission tools in the environment
def toolExists(name):
    try:
        devnull = open(os.devnull)
        subprocess.Popen([name], stdout=devnull, stderr=devnull).communicate()
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            return False
    return True

##
#Experimental: Merging selected contents of TFile
def saveTObject(infileTxt,outFile,pattern):
    inFileList = open(infileTxt,'r')
    fm = ROOT.TFileMerger()
    fm.OutputFile(outFile)
    fm.AddObjectNames(pattern)
    [fm.AddFile(f.rstrip()) for f in inFileList.read().rsplit()]

    default_mode = ROOT.TFileMerger.kAll | ROOT.TFileMerger.kIncremental
    mode = default_mode | ROOT.TFileMerger.kOnlyListed;
    fm.PartialMerge(mode)

##Extract the hists from root files located on grid sites via xrootd
def extract_and_saveWeightHists(inDs, isSys):
    rooFileListPath='%s.txt'%(inDs.split(".")[2])
    print 'Input :%s'%inDs
    print 'Caching file list on : %s '%rooFileListPath
    #os.system('for file in $(rucio list-file-replicas --protocol root --pfns %s|grep "eosatlas.cern.ch"|rev | awk -F "/" \'!seen[$1]++\'| rev);do\ echo $file;done  > %s'%(inDs,rooFileListPath))
    os.system('for file in $(rucio list-file-replicas --protocol root --pfns  --sort geoip %s|rev | sort -t / -k1,2 -u|rev); do echo $file ;done  > %s'%(inDs,rooFileListPath))
    
    import calcScaleNom
    if isSys:
        totw,xs,scaleVars = calcScaleNom.totWandXS(rooFileListPath, isSys)
        scaleVars = json.dumps(scaleVars)
        scaleVars = scaleVars.replace('\'','\"')
        return (rooFileListPath,totw,xs,scaleVars)
    else:
        totw,xs = calcScaleNom.totWandXS(rooFileListPath, isSys)
        return (rooFileListPath,totw,xs)

def submit_jobs():
    date    = os.popen("echo $(date +%y%m%d)").read().rstrip()
    user_id = parsed.nickname if parsed.nickname else os.popen("echo $USER").read().rstrip()

    jobNotSub = []
    os.system("touch upload.tgz; find . -size -5M |xargs tar -zcf upload.tgz  --exclude='.git*' --exclude=upload.tgz ")
    inDsList = open (parsed.inDsTxt,'r').read().rsplit()
    for ijob,f in enumerate(inDsList,1):
        print "\n\033[1mSubmitting %d/%d \033[0m"%(ijob,len(inDsList))
        infileList, totw,xs    = ('',0,0)
        if not parsed.isData: 
            if parsed.isSys:
                infileList, totw,xs, scaleVars    = extract_and_saveWeightHists(f, parsed.isSys)
            else:
                infileList, totw,xs  = extract_and_saveWeightHists(f, parsed.isSys)
        if not (os.path.exists(infileList) or parsed.isData):
            print "Warning %s Cannot be submittted. Couldn't cache weights"%f
            jobNotSub.append(f)
            continue

        ds_id   = os.popen("echo %s| rev |cut -d '.' -f3- |rev | cut -d ':' -f2 | cut -d '.' -f3,6"%f).read().rstrip()
        outds   = ""
        if 'phys' in user_id:
            outds   = "group.%s.%s.gn2_%s.%s"%(user_id,ds_id,parsed.id_text,date)
        else:
            outds   = "user.%s.%s.gn2_%s.%s"%(user_id,ds_id,parsed.id_text,date)


        print "outDS: %s"%outds
        pyCMD = ""
        if not parsed.lsf:
            if parsed.isSys:
                #pyCMD = "python skimGFW2.py %%IN output.root  %s %s"%(totw,xs)
                pyCMD = "python skimGFW2.py infile_list.txt output.root %s %s '%s'"%(totw,xs, scaleVars)
            else:
                pyCMD = "python skimGFW2.py infile_list.txt output.root %s %s "%(totw,xs)
            print(pyCMD)
        else:
            pyCMD = "python skimGFW2.py %s  %s.root  %s %s '%s'"%(infileList,infileList.split(".")[0],totw,xs, scaleVars)

        prun_CMD = ''
        if 'phys' in user_id:
            #prun_CMD='''prun --noEmail --rootVer=6.20/02 --cmtConfig=x86_64-centos7-gcc8-opt   --official  --voms atlas:/atlas/%s/Role=production --exec "%s" --inDS %s --outDS %s --outputs output.root  --match "*root*"  --noCompile --inTarBall upload.tgz \n'''%(user_id,pyCMD,f,outds)
             prun_CMD='''prun --noEmail --rootVer=6.20/02 --cmtConfig=x86_64-centos7-gcc8-opt   --official  --voms atlas:/atlas/%s/Role=production --exec "%s" --writeInputToTxt %s:infile_list.txt  --inDS %s --outDS %s --outputs output.root --nGBPerJob 20 --maxFileSize='20000000000000' --match "*root*"  --noCompile --inTarBall upload.tgz \n'''%(user_id,pyCMD,'%IN',f,outds)
        else:
            prun_CMD='''prun --noEmail --rootVer=6.20/02 --cmtConfig=x86_64-centos7-gcc8-opt  --site %s --exec "%s" --writeInputToTxt %s:infile_list.txt  --inDS %s --outDS %s --outputs output.root --nGBPerJob 10 --maxFileSize='20000000000000' --match "*root*"  --noCompile --inTarBall upload.tgz \n'''%(parsed.site,pyCMD,'%IN',f,outds)
        
        tmpRunFName =  "%s_%s_Run.sh"%(f.split(".")[2],parsed.id_text)
        tmpRun = open(tmpRunFName,"w")
        tmpRun.write('#!/bin/sh\n')
        if not parsed.lsf:
            tmpRun.write(prun_CMD)
        else :
            #tmpRun.write("#SBATCH -p htc\n")
            tmpRun.write("#SBATCH -p htc\n")
            tmpRun.write("#SBATCH --mem 4G\n")
            tmpRun.write("#SBATCH --time=09:00:00\n")
            tmpRun.write(pyCMD)
        tmpRun.close()
        os.system("chmod +x %s"%tmpRunFName)

        if parsed.lsf:
            os.system('sbatch %s'%tmpRunFName)
        elif os.system("sh %s"%tmpRunFName) != 0:
            jobNotSub.append(f)
        #if not parsed.lsf:
        #    os.system("rm tmpRun.sh")
        #else:
        #    os.system("mkdir -p jobs")
        #    os.system("mv tmpRun.sh jobs/%s_%s.sh"%(f.split(".")[2],parsed.id_text))
        #    os.system("chmod +x jobs/%s_%s.sh"%(f.split(".")[2],parsed.id_text))
        #    #os.system("bsub -q 8nm -o jobs/%s_%s.out jobs/%s_%s.sh "%(f.split(".")[2],parsed.id_text,f.split(".")[2], parsed.id_text))

    #clean area after submission
    if len(jobNotSub):
        print "\033[1;31m****************************************************************************************************\033[0m"
        print "\033[1;31mJOBS THAT COULD NOT BE SUBMITTED: %d \033[0m"%len(jobNotSub)
        for i,ds in enumerate(jobNotSub):
            print "%d : %s"%(i,ds)
        print "\033[1;31m****************************************************************************************************\033[0m"
    else:
        print "\033[92mAll jobs submitted (%d) \033[0m"%(len(inDsList) - len(jobNotSub))



if __name__ == "__main__":
    if parsed.inDsTxt =="" or parsed.id_text =="":
        sys.exit("ERROR: --inDsTxt or --id_text missing. Cannot proceed")

    #check if panda and rucio is setup by the user
    if not (toolExists('prun')):
        sys.exit("ERROR: Please setup panda ")
    if not (toolExists('rucio')):
        sys.exit("ERROR: Please setup rucio ")


    submit_jobs()
