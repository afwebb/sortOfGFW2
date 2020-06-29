using VecI = const ROOT::RVec<int>&;
using VecF = const ROOT::RVec<float>&;
using VecD = const ROOT::RVec<double>&;

/**
 * Get leading jet pt
 */
float getJetPt0(VecF jets_Pt)
{
  if (jets_Pt.size()>0) {return jets_Pt.at(0);}
  else return -1.0;
}
float getJetPt1(VecF jets_Pt)
{
  if(jets_Pt.size()>1) {return jets_Pt.at(1);}
  else return -1.0;
}

float getJetEta0(VecF jets_Eta)
{
  if (jets_Eta.size()>0) {return jets_Eta.at(0);}                                                                       
  else return -1.0;                                                                                               
}

float getJetEta1(VecF jets_Eta)
{                                                                                                                          
  if(jets_Eta.size()>1) {return jets_Eta.at(1);}                                                                         
  else return -1.0;                                                                                               
}

float getJetPhi0(VecF jets_Phi)
{
  if (jets_Phi.size()>0) {return jets_Phi.at(0);}
  else return -1.0;
}

float getJetPhi1(VecF jets_Phi)
{
  if(jets_Phi.size()>1) {return jets_Phi.at(1);}
  else return -1.0;
}

float getJetE0(VecF jets_e)
{
  if (jets_e.size()>0) {return jets_e.at(0);}
  else return -1.0;
}

float getJetE1(VecF jets_e)
{
  if(jets_e.size()>1) {return jets_e.at(1);}
  else return -1.0;
}

/** 
 * Get the minimum DeltaR between leptons and jets
 */
float getMindr(VecF phi, VecF eta, VecF pt, float lep_phi_0, float lep_eta_0, float lep_pt_0, float lep_phi_1, float lep_eta_1, float lep_pt_1, float lep_phi_2, float lep_eta_2, float lep_pt_2, int trilep_type)
{
  float minDeltaR_LJ_0     = 9999;
  float minDeltaR_LJ_1     = 9999;
  float minDeltaR_LJ_2     = 9999;
  float DeltaR_min_lep_jet = 9999;
  TVector3 jet;
  TVector3 lep0;
  TVector3 lep1;
  TVector3 lep2;
  lep0.SetPtEtaPhi(lep_pt_0, lep_eta_0, lep_phi_0);
  lep1.SetPtEtaPhi(lep_pt_1, lep_eta_1, lep_phi_1);
  lep2.SetPtEtaPhi(lep_pt_2, lep_eta_2, lep_phi_2);
  for (size_t i = 0; i < phi.size(); i++) {
    jet.SetPtEtaPhi(pt[i], eta[i], phi[i]);
    float  DR_LJ_0_tmp  = ROOT::Math::VectorUtil::DeltaR(lep0,jet);
    if (DR_LJ_0_tmp < minDeltaR_LJ_0) {
      minDeltaR_LJ_0 = DR_LJ_0_tmp;
    }
    
    float  DR_LJ_1_tmp  = ROOT::Math::VectorUtil::DeltaR(lep1,jet);
    if (DR_LJ_1_tmp < minDeltaR_LJ_1) {
      minDeltaR_LJ_1 = DR_LJ_1_tmp;
    }
    float  DR_LJ_2_tmp  = ROOT::Math::VectorUtil::DeltaR(lep2,jet);
    if (DR_LJ_2_tmp < minDeltaR_LJ_2) {
      minDeltaR_LJ_2 = DR_LJ_2_tmp;
    }
    
  }
  DeltaR_min_lep_jet = minDeltaR_LJ_0;
  if (minDeltaR_LJ_1 < DeltaR_min_lep_jet) DeltaR_min_lep_jet = minDeltaR_LJ_1;
  if (trilep_type && (minDeltaR_LJ_2 < DeltaR_min_lep_jet)) DeltaR_min_lep_jet = minDeltaR_LJ_2;
  return DeltaR_min_lep_jet;
}

/**
 * get lepton-bjet minimum DeltaR
 */
float getMindrBjet(VecF phi, VecF eta, VecF pt, VecI bTag, float lep_phi_0, float lep_eta_0, float lep_pt_0, float lep_phi_1, float lep_eta_1, float lep_pt_1, float lep_phi_2, float lep_eta_2, float lep_pt_2, int trilep_type)
{
  float minDeltaR_LJ_0     = 9999;
  float minDeltaR_LJ_1     = 9999;
  float minDeltaR_LJ_2     = 9999;
  float DeltaR_min_lep_jet = 9999;
  TVector3 jet;
  TVector3 lep0;
  TVector3 lep1;
  TVector3 lep2;
  lep0.SetPtEtaPhi(lep_pt_0, lep_eta_0, lep_phi_0);
  lep1.SetPtEtaPhi(lep_pt_1, lep_eta_1, lep_phi_1);
  lep2.SetPtEtaPhi(lep_pt_2, lep_eta_2, lep_phi_2);
  for (size_t i = 0; i < phi.size(); i++) {
    if (bTag.at(i))
      {
	jet.SetPtEtaPhi(pt[i], eta[i], phi[i]);
	float  DR_LJ_0_tmp  = ROOT::Math::VectorUtil::DeltaR(lep0,jet);
	if (DR_LJ_0_tmp < minDeltaR_LJ_0) {
	  minDeltaR_LJ_0 = DR_LJ_0_tmp;
	}
    
	float  DR_LJ_1_tmp  = ROOT::Math::VectorUtil::DeltaR(lep1,jet);
	if (DR_LJ_1_tmp < minDeltaR_LJ_1) {
	  minDeltaR_LJ_1 = DR_LJ_1_tmp;
	}
	float  DR_LJ_2_tmp  = ROOT::Math::VectorUtil::DeltaR(lep2,jet);
	if (DR_LJ_2_tmp < minDeltaR_LJ_2) {
	  minDeltaR_LJ_2 = DR_LJ_2_tmp;
	}
      }
  }
  DeltaR_min_lep_jet = minDeltaR_LJ_0;
  if (minDeltaR_LJ_1 < DeltaR_min_lep_jet) DeltaR_min_lep_jet = minDeltaR_LJ_1;
  if (trilep_type && (minDeltaR_LJ_2 < DeltaR_min_lep_jet)) DeltaR_min_lep_jet = minDeltaR_LJ_2;
  return DeltaR_min_lep_jet;
}


/**Get minimum deltaR between lepton_0 and jet**/
float getMindr0(VecF phi, VecF eta, VecF pt, float lep_phi_0, float lep_eta_0, float lep_pt_0)
{
  float minDeltaR_LJ_0     = 9999;
  TVector3 jet;
  TVector3 lep;
  lep.SetPtEtaPhi(lep_pt_0, lep_eta_0, lep_phi_0);
  for (size_t i = 0; i < phi.size(); i++) {
    jet.SetPtEtaPhi(pt[i], eta[i], phi[i]);
    float  DR_LJ_0_tmp  = ROOT::Math::VectorUtil::DeltaR(lep,jet);
    if (DR_LJ_0_tmp < minDeltaR_LJ_0) {
      minDeltaR_LJ_0 = DR_LJ_0_tmp;
    }
    
  }
  return minDeltaR_LJ_0;
}


/**Get Magnitude of leptons and MET**/
float getMLepMet(float lep_E_0, float lep_Phi_0, float lep_Eta_0, float lep_Pt_0, float lep_E_1, float lep_Phi_1, float lep_Eta_1, float lep_Pt_1, float lep_E_2, float lep_Phi_2, float lep_Eta_2, float lep_Pt_2, float lep_E_3, float lep_Phi_3, float lep_Eta_3, float lep_Pt_3, float lep_E_4, float lep_Phi_4, float lep_Eta_4, float lep_Pt_4, float met_met, float met_phi)
{
  TLorentzVector lep0, lep1, lep2, lep3, lep4, Met;
  lep0.SetPtEtaPhiE(lep_Pt_0, lep_Eta_0, lep_Phi_0, lep_E_0);
  lep1.SetPtEtaPhiE(lep_Pt_1, lep_Eta_1, lep_Phi_1, lep_E_1);
  lep2.SetPtEtaPhiE(lep_Pt_2, lep_Eta_2, lep_Phi_2, lep_E_2);
  lep3.SetPtEtaPhiE(lep_Pt_3, lep_Eta_3, lep_Phi_3, lep_E_3);
  lep4.SetPtEtaPhiE(lep_Pt_4, lep_Eta_4, lep_Phi_4, lep_E_4);
  Met.SetPtEtaPhiM(met_met, 0, met_phi, 0);

  float MLepMet = (lep0+lep1+lep2+lep3+lep4+Met).M(); // sqrt(E^2-Px^2-Py^2-Pz^2)
  return MLepMet; 
}


/**Get MT of leptons and MET**/
float getMtLepMet(float lep_E_0, float lep_Phi_0, float lep_Eta_0, float lep_Pt_0, float lep_E_1, float lep_Phi_1, float lep_Eta_1, float lep_Pt_1, float lep_E_2, float lep_Phi_2, float lep_Eta_2, float lep_Pt_2, float lep_E_3, float lep_Phi_3, float lep_Eta_3, float lep_Pt_3, float lep_E_4, float lep_Phi_4, float lep_Eta_4, float lep_Pt_4, float met_met, float met_phi)
{
  TLorentzVector lep0, lep1, lep2, lep3, lep4, Met;
  lep0.SetPtEtaPhiE(lep_Pt_0, lep_Eta_0, lep_Phi_0, lep_E_0);
  lep1.SetPtEtaPhiE(lep_Pt_1, lep_Eta_1, lep_Phi_1, lep_E_1);
  lep2.SetPtEtaPhiE(lep_Pt_2, lep_Eta_2, lep_Phi_2, lep_E_2);
  lep3.SetPtEtaPhiE(lep_Pt_3, lep_Eta_3, lep_Phi_3, lep_E_3);
  lep4.SetPtEtaPhiE(lep_Pt_4, lep_Eta_4, lep_Phi_4, lep_E_4);
  Met.SetPtEtaPhiM(met_met, 0, met_phi, 0);

  float MtLepMet = (lep0+lep1+lep2+lep3+lep4+Met).Mt(); // sqrt(E^2-Pz^2)
  return MtLepMet; 
}

/**Get elements of mc_generator_weights for EW corrections**/
ROOT::RVec<float> GetEW(VecF mc_gen_vec)
{
  ROOT::RVec<float> mc_EW;
  if (mc_gen_vec.size()>=300) {
    mc_EW.push_back(mc_gen_vec.at(292));
    mc_EW.push_back(mc_gen_vec.at(294));
    mc_EW.push_back(mc_gen_vec.at(296));
  }
  return mc_EW;
}

/**Get vector of total weighted events for EW corrections**/
ROOT::RVec<float> GetTotEW(float ew, float lo1, float lo2)
{
  ROOT::RVec<float> mc_EW = { ew, lo1, lo2 };
  return mc_EW;
}

/**Find the highest Mjj with the most forward jet**/
float getdMaxMjjForwardJet(VecF jet_pt, VecF jet_eta, VecF jet_phi, VecF jet_e)
{
  float maxJetEta =-10;
  float maxMjj    =-10;
  TLorentzVector frwdjet;
  ROOT::RVec<TLorentzVector> jet_lv;
  for(size_t i =0 ; i < jet_pt.size(); ++i)
    {
      TLorentzVector lv;
      lv.SetPtEtaPhiE(jet_pt.at(i),jet_eta.at(i),jet_phi.at(i),jet_e.at(i));
      jet_lv.push_back(lv);
    }
  for (auto j: jet_lv)
    {
      if (fabs(j.Eta()) > maxJetEta)
        {
	  maxJetEta = abs(j.Eta());
	  frwdjet   = j;
        }
    }
  for (auto j: jet_lv)
    {
      if (j != frwdjet)
	{
	  if ( (j+ frwdjet).M() > maxMjj) maxMjj = (j + frwdjet).M();
	}
    }
  return maxMjj;
}

/**Return lep_flavour**/
int getLepFlavour(float lep_ID_0, float lep_ID_1, int dilep_type)
{
  int lep_flavour = 9999;
  if (dilep_type) {
    if (fabs(lep_ID_0)==11&&fabs(lep_ID_1)==11) lep_flavour = 0; // ee pairs
    else if (fabs(lep_ID_0)==11&&fabs(lep_ID_1)==13) lep_flavour = 1; // em pairs
    else if (fabs(lep_ID_0)==13&&fabs(lep_ID_1)==11) lep_flavour = 2; // me pairs
    else if (fabs(lep_ID_0)==13&&fabs(lep_ID_1)==13) lep_flavour = 3; // mm pairs
  }
  return lep_flavour;
}

/**Return max_eta**/
float getMaxEta(float lep_Eta_0, float lep_Eta_1, int dilep_type)
{
  float max_eta = 9999;
  if (dilep_type) max_eta = fmax(fabs(lep_Eta_0), fabs(lep_Eta_1));
  return max_eta;
}

/**Return Delta lep_Eta**/
float getDEta(float lep_Eta_0, float lep_Eta_1, int dilep_type)
{
  float DEtall01 = 9999;
  if (dilep_type) DEtall01 = (lep_Eta_0 - lep_Eta_1 );
  return DEtall01;
}
