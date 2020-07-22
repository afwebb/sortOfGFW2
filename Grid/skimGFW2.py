import sys,re
import json
sys.path.insert(0, "python")
import ROOT
ROOT.gInterpreter.Declare('#include <functions.h>')

#fileName = sys.argv[1]
outName = sys.argv[2]

isMC=False

#trees to skip over
skipTrees=['sumWeights','truth','particleLevel', 'AnalysisTracking', 'loose', 'triggers']
#outRoot = ROOT.TFile.Open(outName, "READ")
#for key in outRoot.GetListOfKeys():
#    kname = key.GetName()
#    skipTrees.append(kname)

print(skipTrees)
#branches to remove
blackList = ['weight_bTagSF_DL1_7.+','weight_bTagSF_DL1_6.+','weight_bTagSF_DL1_8.+','failJvt.+','taus_.+','m_truth.+','jets_.+','lep_.+_3','lep_.+4','jet_.+','ll.+3','ll.+4']
nomBlackList = ['bTagSF_weight_DL1r_Continuous_']

#inFiles = ROOT.vector('string')()
fName = sys.argv[1]

inList = ''#utils.get_files(sys.argv[1])
for f in open(fName):
    inList+=f.rstrip()
    #inFiles.append(f.rstrip())

inFiles = inList.split(',')

rootFile = ROOT.TFile.Open(inFiles[0], "READ")

#get list of trees
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

if len(treeVec)>2:
    inVars = sys.argv[5]
    inVars =inVars.replace('{s','{"s')
    inVars =inVars.replace(', s',', "s')
    inVars =inVars.replace('n:','n":')
    inVars =inVars.replace('p:','p":')
    scaleVars = json.loads(inVars)
    print scaleVars
    doSys = True
else:
    doSys = False

for treeName in treeVec:
    if 'TAUS' in treeName:
        continue

    print("On tree ",treeName)
    #print(h.heap())
    inChain     = ROOT.TChain(treeName)
    for f in inFiles:
        inChain.AddFile(f)

    #df      = ROOT.RDataFrame(treeName,inFiles)     #nominal tree dataframe
    df = ROOT.RDataFrame(inChain)
    df = df.Filter("trilep_type && lep_Pt_0>10e3 && lep_Pt_1>20e3 && lep_Pt_2>20e3 && abs(total_charge)==1 && total_leptons==3")
    ##Add new variables
    df = df.Define("jet_Pt_0","getJetPt0(jets_pt)")
    df = df.Define("jet_Eta_0","getJetEta0(jets_eta)")
    df = df.Define("jet_Phi_0","getJetPhi0(jets_phi)")
    df = df.Define("jet_E_0","getJetE0(jets_e)")
    df = df.Define("jet_Pt_1","getJetPt1(jets_pt)")
    df = df.Define("jet_Eta_1","getJetEta1(jets_eta)")
    df = df.Define("jet_Phi_1","getJetPhi1(jets_phi)")       
    df = df.Define("jet_E_1","getJetE1(jets_e)")
    df = df.Define("DeltaR_min_lep_jet", "getMindr(jets_phi,jets_eta,jets_pt,lep_Phi_0,lep_Eta_0,lep_Pt_0,lep_Phi_1,lep_Eta_1,lep_Pt_1,lep_Phi_2,lep_Eta_2,lep_Pt_2,trilep_type)")
    df = df.Define("minDeltaR_LJ_0","getMindr0(jets_phi,jets_eta,jets_pt,lep_Phi_0,lep_Eta_0,lep_Pt_0)")
    df = df.Define("minDeltaR_LJ_1","getMindr0(jets_phi,jets_eta,jets_pt,lep_Phi_1,lep_Eta_1,lep_Pt_1)")
    df = df.Define("minDeltaR_LJ_2","getMindr0(jets_phi,jets_eta,jets_pt,lep_Phi_2,lep_Eta_2,lep_Pt_2)")
    df = df.Define("DeltaR_min_lep_bjet","getMindrBjet(jets_phi,jets_eta,jets_pt,jets_btagFlag_DL1r_FixedCutBEff_70,lep_Phi_0,lep_Eta_0,lep_Pt_0,lep_Phi_1,lep_Eta_1,lep_Pt_1,lep_Phi_2,lep_Eta_2,lep_Pt_2,trilep_type)")
    df = df.Define("MLepMet","getMLepMet(lep_E_0,lep_Phi_0,lep_Eta_0,lep_Pt_0,lep_E_1,lep_Phi_1,lep_Eta_1,lep_Pt_1,lep_E_2,lep_Phi_2,lep_Eta_2,lep_Pt_2,lep_E_3,lep_Phi_3,lep_Eta_3,lep_Pt_3,lep_E_4,lep_Phi_4,lep_Eta_4,lep_Pt_4,met_met,met_phi)")
    df = df.Define("MtLepMet","getMtLepMet(lep_E_0,lep_Phi_0,lep_Eta_0,lep_Pt_0,lep_E_1,lep_Phi_1,lep_Eta_1,lep_Pt_1,lep_E_2,lep_Phi_2,lep_Eta_2,lep_Pt_2,lep_E_3,lep_Phi_3,lep_Eta_3,lep_Pt_3,lep_E_4,lep_Phi_4,lep_Eta_4,lep_Pt_4,met_met,met_phi)")
    df = df.Define("mjjMax_frwdJet","getdMaxMjjForwardJet(jets_pt, jets_eta, jets_phi, jets_e)")
    df = df.Define("hasTop", "abs(m_truth_pdgId)==6")
    df = df.Define("hasBjet", "abs(m_truth_pdgId)==5")

    #allCols = df.GetColumnNames()
    if isMC:
        df      = df.Define("totalEventsWeighted",'float(TPython::Eval("totW"))').Define("xs",'float(TPython::Eval("xs"))') #Add totalEventWeights and XS  columns to nominal DF
        df = df.Define("weight","(36074.6*(RunYear==2016)+43813.7*(RunYear==2017)+58450.1*(RunYear==2018))*weight_pileup*weight_jvt*weight_mc*xs/totalEventsWeighted")
        if doSys:
            for f in scaleVars:
                print(str(f), str(scaleVars[f]))
                df = df.Define(str(f), str(scaleVars[f]))

    allCols = df.GetColumnNames()

    ##Create a filtered dataframe with l2SS selection.
    #l3DF = df.Filter("trilep_type && lep_Pt_0>10e3 && lep_Pt_1>20e3 && lep_Pt_2>20e3 && abs(total_charge)==1 && total_leptons==3")

    brnch = ROOT.vector('string')()
    #if isMC:
    #    allCols+={'weight'}

    if treeName!='nominal':
        fullBlackList = blackList+nomBlackList
    else:
        fullBlackList = blackList
    for x in allCols:
        if 'jet_flavor' in x:
            brnch.push_back(x)
        #if True not in [b in x for b in fullBlackList]:
        reList = [re.search(b, x) for b in fullBlackList]
        if all(v is None for v in reList):
            brnch.push_back(x)
    
    jet_vars = ["jet_Pt_0","jet_Eta_0","jet_Phi_0","jet_E_0","jet_Pt_1","jet_Eta_1","jet_Phi_1","jet_E_1"]
    #jet_vars=["jet_Pt_0","jet_Pt_1"]
    [brnch.push_back(x) for x in jet_vars]

    snapshotOptions = ROOT.RDF.RSnapshotOptions()
    #snapshotOptions.fLazy = True
    snapshotOptions.fMode = "UPDATE"
    df.Snapshot(treeName, outName, brnch,snapshotOptions)
