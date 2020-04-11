import ROOT,sys
#ROOT.ROOT.EnableImplicitMT()
def getXS(dsid):
    tdpFile = "/cvmfs/atlas.cern.ch/repo/sw/database/GroupData/dev/AnalysisTop/TopDataPreparation/XSection-MC15-13TeV.data"
    d       = dict([ (line.split()[0],line.split()[1:]) for line in open(tdpFile) if len(line.split())>0 and line.split()[0] !="#"])
    return float(d[str(dsid)][0])*float(d[str(dsid)][1])

#print sys.argv[1][:-5]+"_select.root"

inFiles = ROOT.vector('string')()
for f in sys.argv[1:]:
    print f
    inFiles+={f}

df      = ROOT.RDataFrame("nominal",inFiles)     #nominal tree dataframe
allCols = df.GetColumnNames()
sdf     = ROOT.RDataFrame("sumWeights",sys.argv[1])  #sumweights tree dataframe
totW    = sdf.Sum("totalEventsWeighted").GetValue()  #
dsid    = int(sdf.Max("dsid").GetValue())            # Retieve DSID
xs      = getXS(dsid)#*1000                           # Cross-section x BR in fb
df      = df.Define("totalEventsWeighted",'float(TPython::Eval("totW"))').Define("xs",'float(TPython::Eval("xs"))') #Add totalEventWeights and XS  columns to nominal DF

##RunYear selection has been implemented using randomRunNumber
df = df.Define("weight","(36074.6*(randomRunNumber<=311481)+43813.7*(randomRunNumber>311481 && randomRunNumber <=341649)+58450.1*(randomRunNumber>341649))*weight_pileup*weight_jvt*weight_mc*xs/totalEventsWeighted")

df = df.Define("jet_flavor","nTaus_OR_Medium")
df = df.Define("MET_RefFinal_et", "met_met")

##Create a filtered dataframe with l2SS selection.
l2SSDF = df.Filter("dilep_type&&lep_ID_0*lep_ID_1&&nTaus_OR_Pt25==0&&nJets_OR>=4&&nJets_OR_DL1r_77&&lep_Pt_0>15e3&&lep_Pt_1>15e3&&(((abs(lep_ID_0) == 13 &&lep_isMedium_0) ||( abs( lep_ID_0 ) == 11&&abs( lep_Eta_0 ) <2.0)) && ((abs( lep_ID_1 ) == 11&&abs( lep_Eta_1 ) <2.0)||(abs(lep_ID_1) == 13 &&lep_isMedium_1)))")
#print l2SSDF.Count().GetValue()
l3DF = df.Filter("trilep_type && lep_Pt_0>10e3 && lep_Pt_1>20e3 && lep_Pt_2>20e3")

brnch = ROOT.vector('string')()
toSlim=['weight','jet_flavor','lep_Pt_0','lep_Pt_1','nJets_OR','nJets_OR_DL1r_77']  #Add the branch names that you want in your skimmed slimmed file
allCols+={'weight', 'MET_RefFinal_et', 'jet_flavor'}
[brnch.push_back(x) for x in allCols]

#l3DF.Snapshot('nominal',sys.argv[1].split('.')[-2]+"_select.root",brnch)
#l3DF.Snapshot('nominal',sys.argv[1][:-5]+"_select.root",brnch)
l3DF.Snapshot('nominal', '/eos/atlas/user/a/awebb/datasets/cern_ttW/mc16e/'+str(dsid)+".root",brnch)
