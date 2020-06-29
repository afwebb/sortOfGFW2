import ROOT,sys
#ROOT.ROOT.EnableImplicitMT()
def getXS(dsid):
    tdpFile = "/cvmfs/atlas.cern.ch/repo/sw/database/GroupData/dev/AnalysisTop/TopDataPreparation/XSection-MC15-13TeV.data"
    d       = dict([ (line.split()[0],line.split()[1:]) for line in open(tdpFile) if len(line.split())>0 and line.split()[0] !="#"])
    return float(d[str(dsid)][0])*float(d[str(dsid)][1])

def calcScaleNom():
    fileName = sys.argv[1]

    inFiles = ROOT.vector('string')()
    for f in open(fileName):
        inFiles+={f.rstrip()}

    sdf     = ROOT.RDataFrame("sumWeights",inFiles)  #sumweights tree dataframe
    totW    = sdf.Sum("totalEventsWeighted").GetValue()  #
    dsid    = int(sdf.Max("dsid").GetValue())            # Retieve DSID
    xs      = getXS(dsid)#*1000                           # Cross-section x BR in fb
    
    return (totW, dsid, xs)
