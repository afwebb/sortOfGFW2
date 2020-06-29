import ROOT,sys
from array import array

#ROOT.ROOT.EnableImplicitMT()
def getXS(dsid):
    tdpFile = "/cvmfs/atlas.cern.ch/repo/sw/database/GroupData/dev/AnalysisTop/TopDataPreparation/XSection-MC15-13TeV.data"
    d       = dict([ (line.split()[0],line.split()[1:]) for line in open(tdpFile) if len(line.split())>0 and line.split()[0] !="#"])
    return float(d[str(dsid)][0])*float(d[str(dsid)][1])

fileName = sys.argv[1]
runYear = sys.argv[2]


inFiles = ROOT.vector('string')()
#for f in sys.argv[1:]:

oldTree = ROOT.TChain("nominal")
weightTree = ROOT.TChain("sumWeights")

for f in open(fileName):
    print f.rstrip()
    oldTree.AddFile(f.rstrip())
    weightTree.AddFile(f.rstrip())

if runYear!='data':                                                                                                         
    fileName = fileName.replace('replicaLists/files_'+runYear+'_','')
else:
    fileName = fileName.replace('replicaLists/files_','')
fileName = fileName.replace('.txt','')
#outName = '/eos/atlas/user/a/awebb/datasets/cern_ttW/v3/'+runYear+'/'+str(fileName)+".root"
outName = 'test.root'

#Create a new file + a clone of old tree in new file                                                                       
newFile = ROOT.TFile(outName, "update");
newTree = oldTree.CopyTree("trilep_type && abs(total_charge)==1 && lep_Pt_0>10e3 && lep_Pt_1>10e3 && lep_Pt_2>10e3");

if runYear!='data':
    weight = array('f', [0] )
    newTree.Branch("weight", weight, 'weight/F')

    #h = ROOT.TH1F("h", "h", 1, 0, 200000000);                                                    
    #weightTree.Draw("totalEventWeights>>h");                                                           
    #sum_weights = h.GetMean() * h.GetEntries(); 
    #weightTree.GetEntry(0)
    #dsid = weightTree.dsid
    #print(dsid)

    sdf     = ROOT.RDataFrame("sumWeights",inFiles)  #sumweights tree dataframe                                   
    totW    = sdf.Sum("totalEventsWeighted").GetValue()  #                                                         
    dsid    = int(sdf.Max("dsid").GetValue())            # Retieve DSID                                      
    xs      = getXS(dsid)

    nentries = newTree.GetEntries()
    for idx in range(nentries):
        if idx%10000==0:
            print(str(idx)+'/'+str(nEntries))
    
            newTree.GetEntry(i, 1)

            weight = (36074.6*(newTree.RunYear==2016)+43813.7*(newTree.RunYear==2017)+58450.1*(newTree.RunYear==2018))*newTree.weight_pileup*newTree.weight_jvt*newTree.weight_mc*xs/totW
            
            newTree.Fill()


newTree.Write();
newTree.AutoSave();

  treeVec = CxxUtils::make_unique<vector<string>>();
                                                                                                                                if(do_syst) {
    TFile* Rootfile = TFile::Open(samplePath.c_str(), "READ");

    TIter nextkey( Rootfile->GetListOfKeys() );
    TKey *key;
    while((key = (TKey*)nextkey())) {

      TObject *obj = key->ReadObj();
      if( obj->IsA()->InheritsFrom( TTree::Class())) {
        TTree* tree_data =  (TTree*)obj;
        treeVec->push_back(tree_data->GetName());
      }
    }
    Rootfile->Close();
    delete Rootfile;
  }
  else {
    treeVec->push_back("nominal");                                                                                              }
