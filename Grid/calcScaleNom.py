import ROOT,sys
#ROOT.ROOT.EnableImplicitMT()
def getXS(dsid):
    tdpFile = "/cvmfs/atlas.cern.ch/repo/sw/database/GroupData/dev/AnalysisTop/TopDataPreparation/XSection-MC15-13TeV.data"
    d       = dict([ (line.split()[0],line.split()[1:]) for line in open(tdpFile) if len(line.split())>0 and line.split()[0] !="#"])
    return float(d[str(dsid)][0])*float(d[str(dsid)][1])

def totWandXS(fileName, isSys):

    sChain = ROOT.TChain("sumWeights")
    for f in open(fileName):
        sChain.AddFile(f.rstrip())

    sdf = ROOT.RDataFrame(sChain)
    totW    = sdf.Sum("totalEventsWeighted").GetValue()  #
    dsid    = int(sdf.Max("dsid").GetValue())            # Retieve DSID
    print dsid
    xs      = getXS(dsid)#*1000                           # Cross-section x BR in fb

    weightVec = sdf.AsNumpy(columns=['totalEventsWeighted_mc_generator_weights'])

    scaleVec = weightVec['totalEventsWeighted_mc_generator_weights'][0]
    for s in weightVec['totalEventsWeighted_mc_generator_weights'][1:]:
        scaleVec+=s

    nameVec = sdf.AsNumpy(columns=['names_mc_generator_weights'])
    names = [x for x in nameVec['names_mc_generator_weights'][0]]

    if isSys:
        scaleDict = {}
        if len(scaleVec)<7:
            scaleDict= {}

        elif dsid>364700 and dsid<364800:
            totW = scaleVec[names.index('')]
            scaleDict["scale_varRFdown"] = scaleVec[names.index(' MUR=0.5 MUF=0.5  ')]
            scaleDict["scale_varRdown"] = scaleVec[names.index(' MUF=0.5  ')]
            scaleDict["scale_varFdown"] = scaleVec[names.index(' MUF=0.5  ')]
            scaleDict["scale_varRFup"] = scaleVec[names.index(' MUR=2.0 MUF=2.0  ')]
            scaleDict["scale_varFup"] = scaleVec[names.index(' MUF=2.0  ')]
            scaleDict["scale_varRup"] = scaleVec[names.index(' MUR=2.0  ')]
        elif dsid<370000 and dsid>360000:
            scaleDict["scale_varRFdown"] = scaleVec[4]
            scaleDict["scale_varRdown"] = scaleVec[5]
            scaleDict["scale_varFdown"] = scaleVec[6]
            scaleDict["scale_varFup"] = scaleVec[8]
            scaleDict["scale_varRup"] = scaleVec[9]
            scaleDict["scale_varRFup"] = scaleVec[10]
        else:
            scaleDict["scale_varRdown"] = scaleVec[1]
            scaleDict["scale_varRup"] = scaleVec[2]
            scaleDict["scale_varFdown"] = scaleVec[3]
            scaleDict["scale_varRFdown"] = scaleVec[4]
            scaleDict["scale_varFup"] = scaleVec[6]
            scaleDict["scale_varRFup"] = scaleVec[8]
        return (totW, xs, scaleDict)

    else:
        return (totW, xs)


#print totWandXS(sys.argv[1], 1)
