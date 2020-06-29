import sys
sys.path.insert(0, "python")
import ROOT

#fileName = sys.argv[1]
outName = sys.argv[2]

isMC=False

skipTrees=['sumWeights','truth','particleLevel', 'AnalysisTracking', 'loose', 'triggers']

#inFiles = ROOT.vector('string')()
fName = sys.argv[1]

inList = ''#utils.get_files(sys.argv[1])
for f in open(fName):
    inList+=f.rstrip()
    #inFiles.append(f.rstrip())

inFiles = inList.split(',')

rootFile = ROOT.TFile.Open(inFiles[0], "READ")

treeVec=[]
for key in rootFile.GetListOfKeys():
    kname = key.GetName()
    if kname=='particleLevel':
        isMC=True

    if kname in skipTrees:
        continue

    treeVec.append(kname)

#treeVec=['nominal']
if isMC:
    totW    = float(sys.argv[3])
    xs      = float(sys.argv[4])

for treeName in treeVec:
    print("On tree ",treeName)
    #print(h.heap())
    inChain     = ROOT.TChain(treeName)
    for f in inFiles:
        inChain.AddFile(f)

    #df      = ROOT.RDataFrame(treeName,inFiles)     #nominal tree dataframe
    df = ROOT.RDataFrame(inChain)
    allCols = df.GetColumnNames()
    if isMC:
        df      = df.Define("totalEventsWeighted",'float(TPython::Eval("totW"))').Define("xs",'float(TPython::Eval("xs"))') #Add totalEventWeights and XS  columns to nominal DF
        df = df.Define("weight","(36074.6*(RunYear==2016)+43813.7*(RunYear==2017)+58450.1*(RunYear==2018))*weight_pileup*weight_jvt*weight_mc*xs/totalEventsWeighted")

    ##Create a filtered dataframe with l2SS selection.
    l3DF = df.Filter("trilep_type && lep_Pt_0>10e3 && lep_Pt_1>20e3 && lep_Pt_2>20e3 && abs(total_charge)==1")

    brnch = ROOT.vector('string')()
    if isMC:
        allCols+={'weight'}
    [brnch.push_back(x) for x in allCols]

    snapshotOptions = ROOT.RDF.RSnapshotOptions()
    #snapshotOptions.fLazy = True
    snapshotOptions.fMode = "UPDATE"
    l3DF.Snapshot(treeName, outName, brnch,snapshotOptions)
