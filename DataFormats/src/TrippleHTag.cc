#include "flashgg/DataFormats/interface/TrippleHTag.h"

using namespace flashgg;

bool isAncestor(const reco::Candidate* ancestor, const reco::Candidate * particle)
{
//particle is already the ancestor
        if(ancestor == particle ) return true;

//otherwise loop on mothers, if any and return true if the ancestor is found
        for(size_t i=0;i< particle->numberOfMothers();i++)
        {   
                if(particle->mother(i)->pdgId() != ancestor->pdgId()) continue;
                if(isAncestor(ancestor,particle->mother(i))) return true;
        }
//if we did not return yet, then particle and ancestor are not relatives
        return false;
}

TrippleHTag::TrippleHTag() : DiPhotonTagBase::DiPhotonTagBase(), mva_(-2.) 
{  
}

TrippleHTag::~TrippleHTag() {}

TrippleHTag::TrippleHTag( edm::Ptr<flashgg::DiPhotonCandidate> diPho, 
                          edm::Ptr<flashgg::Jet> h1LeadJet , edm::Ptr<flashgg::Jet> h1SubleadJet ,
                          edm::Ptr<flashgg::Jet> h2LeadJet , edm::Ptr<flashgg::Jet> h2SubleadJet ,
                          int nGoodJetsSelected
                        )
    : mva_(-.2), 
      MX_(0.),genMhhh_(0.),
      genCosThetaStar_CS_(0.),
      h1LeadJet_(h1LeadJet), 
      h1SubleadJet_(h1SubleadJet),  
      h2LeadJet_(h2LeadJet), 
      h2SubleadJet_(h2SubleadJet)
{   
      nGoodJets=nGoodJetsSelected;

    dipho_ = diPho;
    
    if( (h1LeadJet_->p4() + h1SubleadJet_->p4()).pt() < (h2LeadJet_->p4() +h2SubleadJet_->p4()).pt() )
    {
         auto tmp=h1LeadJet_  ; h1LeadJet_=h2LeadJet_ ; h2LeadJet_=tmp;
              tmp=h1SubleadJet_  ; h1SubleadJet_=h2SubleadJet_ ; h2SubleadJet_=tmp;
    }

    quadjet_ = h1LeadJet_->p4() + h1SubleadJet_->p4() + h2LeadJet_->p4() + h2SubleadJet_->p4();

    diPhotonLV.SetPtEtaPhiE( diPho->pt() , diPho->eta(), diPho->phi() , diPho->energy() );
    
    h1LeadJetLV_.SetPtEtaPhiE( h1LeadJet_->pt() , h1LeadJet_->eta(), h1LeadJet_->phi() , (h1LeadJet_->p4()).E() );
    h1SubleadJetLV_.SetPtEtaPhiE( h1SubleadJet_->pt() , h1SubleadJet_->eta(), h1SubleadJet_->phi() , (h1SubleadJet_->p4()).E() );
    h2LeadJetLV_.SetPtEtaPhiE( h2LeadJet_->pt() , h2LeadJet_->eta(), h2LeadJet_->phi() , h2LeadJet_->p4().E() );
    h2SubleadJetLV_.SetPtEtaPhiE( h2SubleadJet_->pt() , h2SubleadJet_->eta(), h2SubleadJet_->phi() , (h2SubleadJet_->p4()).E() );
    
    higgsCandidateLV[0]=diPhotonLV;
    higgsCandidateLV[1]=h1LeadJetLV_+h1SubleadJetLV_;
    higgsCandidateLV[2]=h2LeadJetLV_+h2SubleadJetLV_;
    
    if( higgsCandidateLV[1].Pt() > higgsCandidateLV[2].Pt() )
    {
        dijet1_= h1LeadJet_->p4() + h1SubleadJet_->p4() ;
        dijet2_ = h2LeadJet_->p4() + h2SubleadJet_->p4();
    }
    else
    {
        dijet2_ = h1LeadJet_->p4() + h1SubleadJet_->p4() ;
        dijet1_ = h2LeadJet_->p4() + h2SubleadJet_->p4();
    }

    // sorting cands
    if ( higgsCandidateLV[2].Pt() > higgsCandidateLV[1].Pt() ) { auto x = higgsCandidateLV[2]; higgsCandidateLV[2] = higgsCandidateLV[1] ; higgsCandidateLV[1] = x ;  }
    if ( higgsCandidateLV[1].Pt() > higgsCandidateLV[0].Pt() ) { auto x = higgsCandidateLV[1]; higgsCandidateLV[1] = higgsCandidateLV[0] ; higgsCandidateLV[0] = x ;  }
    if ( higgsCandidateLV[2].Pt() > higgsCandidateLV[1].Pt() ) { auto x = higgsCandidateLV[2]; higgsCandidateLV[2] = higgsCandidateLV[1] ; higgsCandidateLV[1] = x ;  }
    
    hhhLV_ = higgsCandidateLV[0] + higgsCandidateLV[1] + higgsCandidateLV[2] ; 
    
    this->setP4( quadjet_ + diPhoton()->p4() );
    addAK4JetBranches();
    addGenObjectBranches();
    
    for(TString tag : {"promptG1","promptG2","promptG3","promptG4","promptG5","promptG6"} )
    {
      //std::cout<<" setting tag : "<<tag<<" \n";
      storageMapFloatArray["gen_"+tag+"_pt"][0]= -660.6 ;
      storageMapFloatArray["gen_"+tag+"_pdgId"][0]= -660.6 ;
      storageMapFloatArray["gen_"+tag+"_y"][0]= -660.6 ;
      storageMapFloatArray["gen_"+tag+"_eta"][0]= -660.6 ;
      storageMapFloatArray["gen_"+tag+"_phi"][0]= -660.6 ;
      storageMapFloatArray["gen_"+tag+"_e"][0]= -660.6 ;
      storageMapFloatArray["gen_"+tag+"_numberOfDaughters"][0]= -660.6 ;
      storageMapFloatArray["gen_"+tag+"_mother" ][0]  = -666.6 ;
      storageMapFloatArray["gen_"+tag+"_isPromptFS"][0]  = -666.6 ;
      storageMapFloatArray["gen_"+tag+"_isFHPFS"][0]  = -666.6 ;
      storageMapFloatArray["gen_"+tag+"_isHard" ][0]  = -666.6 ;
    }

}

void TrippleHTag::addGenObjectBranches()
{
    storageMapFloatArray["gen_isValid"] = new Float_t;
    for(TString tag : {"H1","H2","H3"} )
    {
      
          //std::cout<<" setting tag : "<<tag<<" \n";
          storageMapFloatArray["gen_"+tag+"_pt"] = new Float_t;
          storageMapFloatArray["gen_"+tag+"_pdgId"] = new Float_t;
          storageMapFloatArray["gen_"+tag+"_y"] = new Float_t;
          storageMapFloatArray["gen_"+tag+"_eta"] = new Float_t;
          storageMapFloatArray["gen_"+tag+"_phi"] = new Float_t;
          storageMapFloatArray["gen_"+tag+"_e"] = new Float_t;
          storageMapFloatArray["gen_"+tag+"_numberOfDaughters"] = new Float_t;
          storageMapFloatArray["gen_"+tag+"_mother" ]  = new Float_t ;
          storageMapFloatArray["gen_"+tag+"_isPromptFS"]  = new Float_t ;
          storageMapFloatArray["gen_"+tag+"_isFHPFS"]  = new Float_t ;
          storageMapFloatArray["gen_"+tag+"_isHard" ]  = new Float_t ;
    }

    for(TString tag : {"H1_dau1","H2_dau1","H3_dau1","H1_dau2","H2_dau2","H3_dau2"} )
    {
      //std::cout<<" setting tag : "<<tag<<" \n";
      storageMapFloatArray["gen_"+tag+"_pt"] = new Float_t;
      storageMapFloatArray["gen_"+tag+"_pdgId"] = new Float_t;
      storageMapFloatArray["gen_"+tag+"_y"] = new Float_t;
      storageMapFloatArray["gen_"+tag+"_eta"] = new Float_t;
      storageMapFloatArray["gen_"+tag+"_phi"] = new Float_t;
      storageMapFloatArray["gen_"+tag+"_e"] = new Float_t;
      storageMapFloatArray["gen_"+tag+"_numberOfDaughters"] = new Float_t;
      storageMapFloatArray["gen_"+tag+"_mother" ]  = new Float_t ;
      storageMapFloatArray["gen_"+tag+"_isPromptFS"]  = new Float_t ;
      storageMapFloatArray["gen_"+tag+"_isFHPFS"]  = new Float_t ;
      storageMapFloatArray["gen_"+tag+"_isHard" ]  = new Float_t ;
    }

    storageMapFloatArray["gen_isValid"] = new Float_t;
    for(TString tag : {
                        "promptG1","promptG2","promptG3","promptG4","promptG5","promptG6"
                      } )
    {
      //std::cout<<" setting tag : "<<tag<<" \n";
      storageMapFloatArray["gen_"+tag+"_pt"] = new Float_t;
      storageMapFloatArray["gen_"+tag+"_pdgId"] = new Float_t;
      storageMapFloatArray["gen_"+tag+"_y"] = new Float_t;
      storageMapFloatArray["gen_"+tag+"_eta"] = new Float_t;
      storageMapFloatArray["gen_"+tag+"_phi"] = new Float_t;
      storageMapFloatArray["gen_"+tag+"_e"] = new Float_t;
      storageMapFloatArray["gen_"+tag+"_numberOfDaughters"] = new Float_t;
      storageMapFloatArray["gen_"+tag+"_mother" ]  = new Float_t ;
      storageMapFloatArray["gen_"+tag+"_isHard" ]  = new Float_t ;
      storageMapFloatArray["gen_"+tag+"_isPromptFS"]  = new Float_t ;
      storageMapFloatArray["gen_"+tag+"_isFHPFS"]  = new Float_t ;
    }
    
    for(TString tag : {
                        "jet1","jet2","jet3","jet4","jet5","jet6","jet7","jet8","jet9","jet10","jet11","jet12"
                      } )
    {
      storageMapFloatArray["gen_"+tag+"_pt"] = new Float_t;
      storageMapFloatArray["gen_"+tag+"_y"] = new Float_t;
      storageMapFloatArray["gen_"+tag+"_eta"] = new Float_t;
      storageMapFloatArray["gen_"+tag+"_phi"] = new Float_t;
      storageMapFloatArray["gen_"+tag+"_mass"] = new Float_t;
    }

       storageMapFloatArray["genJet_isValid"]         = new Float_t[N_GEN_JET_MAX];
       storageMapFloatArray["genJet_pt"]         = new Float_t[N_GEN_JET_MAX];
       storageMapFloatArray["genJet_y"]        = new Float_t[N_GEN_JET_MAX];
       storageMapFloatArray["genJet_eta"]        = new Float_t[N_GEN_JET_MAX];
       storageMapFloatArray["genJet_phi"]        = new Float_t[N_GEN_JET_MAX];
       storageMapFloatArray["genJet_mass"]          = new Float_t[N_GEN_JET_MAX];

}
void TrippleHTag::fillGenPrticle(TString tag, const reco::Candidate* particle)
{
      storageMapFloatArray["gen_"+tag+"_pt"][0]   = particle->pt() ;
      storageMapFloatArray["gen_"+tag+"_pdgId"][0]   = particle->pdgId() ;
      storageMapFloatArray["gen_"+tag+"_y"][0]   = particle->y() ;
      storageMapFloatArray["gen_"+tag+"_eta"][0]   = particle->eta() ;
      storageMapFloatArray["gen_"+tag+"_phi"][0]   = particle->phi() ;
      storageMapFloatArray["gen_"+tag+"_e"][0]   = particle->energy() ;
      storageMapFloatArray["gen_"+tag+"_numberOfDaughters"][0]   = particle->numberOfDaughters() ;
      storageMapFloatArray["gen_"+tag+"_mother"][0]    = particle->mother()->pdgId()  ;
      storageMapFloatArray["gen_"+tag+"_isHard"][0]    = -2.0 ; //particle->isHardProcess() ;
      storageMapFloatArray["gen_"+tag+"_isPromptFS"][0]   = -2.0 ; //particle->fromHardProcessFinalState() ;
      storageMapFloatArray["gen_"+tag+"_isFHPFS"][0]   = -2.0 ; //particle->fromHardProcessFinalState() ;
    
 //     std::cout<<"\n 125 Adding  for prompt photon for "<<tag<<" !\n";
 //     std::cout<<storageMapFloatArray["gen_"+tag+"_pt"][0] <<"\n";
 //     std::cout<<storageMapFloatArray["gen_"+tag+"_pdgId"][0] <<"\n";
 //     std::cout<<storageMapFloatArray["gen_"+tag+"_y"][0] <<"\n";
 //     std::cout<<storageMapFloatArray["gen_"+tag+"_eta"][0] <<"\n";
 //     std::cout<<storageMapFloatArray["gen_"+tag+"_phi"][0] <<"\n";
 //     std::cout<<storageMapFloatArray["gen_"+tag+"_e"][0] <<"\n";
 //     std::cout<<storageMapFloatArray["gen_"+tag+"_numberOfDaughters"][0] <<"\n";
}

void TrippleHTag::fillGenPrticle(TString tag, const reco::GenParticle &particle)
{
      storageMapFloatArray["gen_"+tag+"_pt"][0]   = particle.pt() ;
      storageMapFloatArray["gen_"+tag+"_pdgId"][0]   = particle.pdgId() ;
      storageMapFloatArray["gen_"+tag+"_y"][0]   = particle.y() ;
      storageMapFloatArray["gen_"+tag+"_eta"][0]   = particle.eta() ;
      storageMapFloatArray["gen_"+tag+"_phi"][0]   = particle.phi() ;
      storageMapFloatArray["gen_"+tag+"_e"][0]   = particle.energy() ;
      storageMapFloatArray["gen_"+tag+"_numberOfDaughters"][0]   = particle.numberOfDaughters() ;
      storageMapFloatArray["gen_"+tag+"_mother"][0]    = particle.mother()->pdgId()  ;
      storageMapFloatArray["gen_"+tag+"_isHard"][0]    = particle.isHardProcess() ;
      storageMapFloatArray["gen_"+tag+"_isPromptFS"][0]    = particle.isPromptFinalState() ;
      storageMapFloatArray["gen_"+tag+"_isFHPFS"][0]   = particle.fromHardProcessFinalState() ;
      //std::cout<<"\nAdding  for prompt photon for "<<tag<<" !\n";
      //std::cout<<storageMapFloatArray["gen_"+tag+"_pt"][0] <<"\n";
      //std::cout<<storageMapFloatArray["gen_"+tag+"_pdgId"][0] <<"\n";
      //std::cout<<storageMapFloatArray["gen_"+tag+"_y"][0] <<"\n";
      //std::cout<<storageMapFloatArray["gen_"+tag+"_eta"][0] <<"\n";
      //std::cout<<storageMapFloatArray["gen_"+tag+"_phi"][0] <<"\n";
      //std::cout<<storageMapFloatArray["gen_"+tag+"_e"][0] <<"\n";
      //std::cout<<storageMapFloatArray["gen_"+tag+"_numberOfDaughters"][0] <<"\n";
}


float TrippleHTag::getGenDetails( std::string item_) const
{
    TString item(item_.c_str());
   // std::cout<<"Looking for "<<item<<"\n";
    auto itm=storageMapFloatArray.find("gen_isValid") ;
    if( itm == storageMapFloatArray.end() )
    {
        return -1.111e3;       
    }
    if( (itm->second[0] )< 0.0 )
    {
        return -1.111e3;       
    }

    itm=storageMapFloatArray.find(item) ;
    if( itm == storageMapFloatArray.end() )
    {
        std::cout<<"Item asked not found getGenDetails || "<<item<<" || \n";
    }
  //  std::cout<<" Found it ! ";
    return (itm->second[0]);
}

void TrippleHTag::fillGenJets(const edm::Handle<edm::View<reco::GenJet>> genJets )
{    
    for( unsigned int i = 0 ; i < N_GEN_JET_MAX ; i++ ) 
    {
      storageMapFloatArray["genJet_pt"][i]   = -1.0  ;
      storageMapFloatArray["genJet_eta"][i]  = -66.0 ;
      storageMapFloatArray["genJet_phi"][i]  = -66.0 ;
      storageMapFloatArray["genJet_mass"][i] = -1.0  ;
      storageMapFloatArray["genJet_y"][i]    = -66.0 ;
    }


                
     for( unsigned int gjLoop = 0 ; gjLoop < genJets->size() ; gjLoop++ ) {
        if ( gjLoop  >= N_GEN_JET_MAX ) break;
        edm::Ptr<reco::GenJet> gj = genJets->ptrAt( gjLoop );
      
        storageMapFloatArray["genJet_pt"][gjLoop]   =  gj->pt();
        storageMapFloatArray["genJet_y"][gjLoop]    =  gj->y();
        storageMapFloatArray["genJet_eta"][gjLoop]  =  gj->eta();
        storageMapFloatArray["genJet_phi"][gjLoop]  =  gj->phi();
        storageMapFloatArray["genJet_mass"][gjLoop] =  gj->mass();
        }

}




void TrippleHTag::fillPromptGenDetails( edm::Handle<edm::View<reco::GenParticle>> pruned  )
{    
    int nPromptPhotons=0;
    size_t promptPhotonIdx[10];
  //  std::cout<<"\nNew Event \n";
    for(size_t i=0; i< pruned->size();i++)
    {
        const reco::GenParticle * part_pru = (&(*pruned)[i]);
//          if(not (&(*pruned)[i])->isPromptFinalState()) continue;
//          if((&(*pruned)[i])->isHardProcess())
//           std::cout<<i<<" pdgid : "<< part_pru->pdgId() << "    status : " << part_pru->status() 
//                    << "   isHard " << part_pru->isHardProcess()  
//                    << "   mother " << part_pru->mother()->pdgId()   << std::endl
//                    << "   isPromptFinalState() " << part_pru->isPromptFinalState()   << std::endl;
          if( part_pru->pt() < 15.0 ) continue ;
          if( part_pru->pdgId()==22 )
          {
                promptPhotonIdx[nPromptPhotons]=i;
                //std::cout<<"[ "<<i<<" ]"<<" got prompt photon : "<<part_pru->pdgId()<<" , "
                //         <<promptPhotonIdx[nPromptPhotons]<<" , "
                //         <<part_pru->pt()<<" , "
                //         <<part_pru->numberOfDaughters()<<"\n";
                nPromptPhotons++;
          }

          if (nPromptPhotons>5)
            break;
    }
    
    if(nPromptPhotons > 0)
        fillGenPrticle("promptG1",pruned->at(promptPhotonIdx[0]));
    if(nPromptPhotons > 1)
        fillGenPrticle("promptG2",pruned->at(promptPhotonIdx[1]));
    if(nPromptPhotons > 2)
        fillGenPrticle("promptG3",pruned->at(promptPhotonIdx[2]));
    if(nPromptPhotons > 3)
        fillGenPrticle("promptG4",pruned->at(promptPhotonIdx[3]));
    if(nPromptPhotons > 4)
        fillGenPrticle("promptG5",pruned->at(promptPhotonIdx[4]));
    if(nPromptPhotons > 5)
        fillGenPrticle("promptG6",pruned->at(promptPhotonIdx[5]));

    storageMapFloatArray["gen_isValid"][0] =  1.0;
}

void TrippleHTag::fillHHHGenDetails( edm::Handle<edm::View<reco::GenParticle>> pruned  )
{

    TLorentzVector b1;
    TLorentzVector b2;
    int nHiggs=0;
    size_t higgsIdx[10];
    Float_t higgsPt[10];
    for(size_t i=0; i< pruned->size();i++)
    {
        const reco::GenParticle * part_pru = (&(*pruned)[i]);
          if(not (&(*pruned)[i])->isHardProcess()) continue;
    //      if((&(*pruned)[i])->isHardProcess())
    //       std::cout<<i<<" pdgid : "<< part_pru->pdgId() << "    status : " << part_pru->status() 
    //                << "   isHard " << part_pru->isHardProcess()  
    //                << "   mother " << part_pru->mother()->pdgId()   << std::endl;
          if( part_pru->pdgId()==25 )
          {
                higgsPt[nHiggs]=part_pru->pt();
                higgsIdx[nHiggs]=i;
             //   std::cout<<" got higgs : "<<part_pru->pdgId()<<" , "
             //             <<higgsIdx[nHiggs]<<" , "<<higgsPt[nHiggs]<<" , "<<part_pru->numberOfDaughters()<<"\n";
                nHiggs++;
          }

    }
    bool isBad=false;
    if(nHiggs!=3)
    {
        std::cout<<"No Higgs found in event !\n";
        isBad=true;
    }

    size_t h1Idx(0),h2Idx(1),h3Idx(2);
    
    if(higgsPt[h1Idx] < higgsPt[h2Idx]) { auto x=h2Idx ; h2Idx=h1Idx ; h1Idx=x ;}
    if(higgsPt[h2Idx] < higgsPt[h3Idx]) { auto x=h3Idx ; h3Idx=h2Idx ; h2Idx=x ;}
    if(higgsPt[h1Idx] < higgsPt[h2Idx]) { auto x=h2Idx ; h2Idx=h1Idx ; h1Idx=x ;}
    
    h1Idx=higgsIdx[h1Idx];
    h2Idx=higgsIdx[h2Idx];
    h3Idx=higgsIdx[h3Idx];
    
    fillGenPrticle("H1",pruned->at(h1Idx));
    const reco::GenParticle *  hig= &(pruned->at(h1Idx));
    const reco::GenParticle * dau[2];
    Int_t dIdx(0);
    for(size_t i=0; i< pruned->size();i++)
    {
        const reco::GenParticle * part_pru = (&(*pruned)[i]);
        if(isAncestor(hig,part_pru) and  hig->pdgId()!=part_pru->pdgId())
        {
                dau[dIdx]=part_pru;
                dIdx++;
        }
    }
    if(dIdx ==2) {
        fillGenPrticle("H1_dau1",dau[0]);
        fillGenPrticle("H1_dau2",dau[1]);
    }
    else{
        isBad=true;
        std::cout<<" null here \n";
    }
    
    fillGenPrticle("H2",pruned->at(h2Idx));
    hig= &(pruned->at(h2Idx));
    dau[0]=nullptr; dau[1]=nullptr;
    dIdx=0;
    for(size_t i=0; i< pruned->size();i++)
    {
        const reco::GenParticle * part_pru = (&(*pruned)[i]);
        if(isAncestor(hig,part_pru) and  hig->pdgId()!=part_pru->pdgId())
        {
                dau[dIdx]=part_pru;
                dIdx++;
        }
    }
    if(dIdx ==2) {
        fillGenPrticle("H2_dau1",dau[0]);
        fillGenPrticle("H2_dau2",dau[1]);
    }
    else {
        isBad=true;
        std::cout<<" null here \n";
    }
    
    fillGenPrticle("H3",pruned->at(h3Idx));
    hig= &(pruned->at(h3Idx));
    dau[0]=nullptr; dau[1]=nullptr;
    dIdx=0;
    for(size_t i=0; i< pruned->size();i++)
    {
        const reco::GenParticle * part_pru = (&(*pruned)[i]);
        if(isAncestor(hig,part_pru) and  hig->pdgId()!=part_pru->pdgId())
        {
                dau[dIdx]=part_pru;
                dIdx++;
        }
    }
    if(dIdx ==2) {
        fillGenPrticle("H3_dau1",dau[0]);
        fillGenPrticle("H3_dau2",dau[1]);
    }
    else {
        isBad=true;
        std::cout<<" null here \n";
    }
    if(isBad)
        storageMapFloatArray["gen_isValid"][0] = -1.0;
    else 
        storageMapFloatArray["gen_isValid"][0] =  1.0;


}


void TrippleHTag::addAK4JetBranches()
{
       storageMapFloatArray["jet_isValid"]         = new Float_t[N_JET_MAX];
       storageMapFloatArray["jet_pt"]         = new Float_t[N_JET_MAX];
       storageMapFloatArray["jet_eta"]        = new Float_t[N_JET_MAX];
       storageMapFloatArray["jet_phi"]        = new Float_t[N_JET_MAX];
       storageMapFloatArray["jet_mass"]          = new Float_t[N_JET_MAX];
       storageMapFloatArray["jet_csvScore"]   = new Float_t[N_JET_MAX];
       storageMapFloatArray["jet_deepCSVScore"]    = new Float_t[N_JET_MAX];
       storageMapFloatArray["jet_deepJetScore"]    = new Float_t[N_JET_MAX];
       storageMapFloatArray["jet_deepJetScore_b"]    = new Float_t[N_JET_MAX];
       storageMapFloatArray["jet_deepJetScore_bb"]    = new Float_t[N_JET_MAX];
       storageMapFloatArray["jet_deepJetScore_lepb"]    = new Float_t[N_JET_MAX];
       storageMapFloatArray["jet_particleNetAK4_B"]  = new Float_t[N_JET_MAX];
       storageMapFloatArray["jet_particleNetAK4_CvsL"]  = new Float_t[N_JET_MAX];
       storageMapFloatArray["jet_particleNetAK4_CvsB"]  = new Float_t[N_JET_MAX];
       storageMapFloatArray["jet_particleNetAK4_QvsG"]  = new Float_t[N_JET_MAX];
       storageMapFloatArray["jet_particleNetAK4_puIdDisc"]  = new Float_t[N_JET_MAX];
       storageMapFloatArray["jet_flavour"]         = new Float_t[N_JET_MAX];
       storageMapFloatArray["jet_pFlavour"]        = new Float_t[N_JET_MAX];
       storageMapFloatArray["jet_bJetRegCorr"]     = new Float_t[N_JET_MAX];
       storageMapFloatArray["jet_bJetRegRes"]         = new Float_t[N_JET_MAX];
       storageMapFloatArray["jet_puJetIdMVA"]   = new Float_t[N_JET_MAX];
       storageMapFloatArray["jet_isLoose"]   = new Float_t[N_JET_MAX];
       storageMapFloatArray["jet_isTight"]  = new Float_t[N_JET_MAX];
       storageMapFloatArray["jet_isTight2017"]  = new Float_t[N_JET_MAX];
       storageMapFloatArray["jet_isTight2018"]  = new Float_t[N_JET_MAX];
}

float TrippleHTag::getAK4JetDetails(  std::string item_ ,  Int_t idx) const
{
    TString item(item_.c_str());
    if(  idx >= N_JET_MAX  )
    {
        return -1.111e3;       
    }
    auto itm=storageMapFloatArray.find("jet_isValid") ;
    if( itm == storageMapFloatArray.end() )
    {
        return -1.111e3;       
    }
    if( (itm->second)[idx]< 0.0 )
    {
        return -1.111e3;       
    }

    itm=storageMapFloatArray.find(item) ;
    return (itm->second)[idx];
}

float TrippleHTag::getGenJDetails(  std::string item_ ,  Int_t idx) const
{
    TString item(item_.c_str());
    if(  idx >= N_JET_MAX  )
    {
        return -1.111e3;       
    }
    auto itm=storageMapFloatArray.find("genJet_isValid") ;
    if( itm == storageMapFloatArray.end() )
    {
        return -1.111e3;       
    }
    if( (itm->second)[idx]< 0.0 )
    {
        return -1.111e3;       
    }

    itm=storageMapFloatArray.find(item) ;
    return (itm->second)[idx];
}



void TrippleHTag::addAK4JetDetails( const std::vector<edm::Ptr<flashgg::Jet> > jets)
{   
    int idx=0;
    for( size_t ijet=0; ijet < N_JET_MAX; ++ijet ) 
    {
            storageMapFloatArray["jet_isValid"][idx]       = -1 ;
            storageMapFloatArray["jet_isValid"][idx]        = 0.0 ;
            storageMapFloatArray["jet_pt"][idx]        = -1.0 ;
            storageMapFloatArray["jet_eta"][idx]       = 0.0 ;
            storageMapFloatArray["jet_phi"][idx]       = 0.0 ;
            storageMapFloatArray["jet_mass"][idx]         = 0.0 ;
            storageMapFloatArray["jet_csvScore"][idx]  = 0.0 ;
            storageMapFloatArray["jet_deepCSVScore"][idx]   = 0.0 ;
            storageMapFloatArray["jet_deepJetScore"][idx]   = 0.0 ;
            storageMapFloatArray["jet_deepJetScore_b"][idx]   = 0.0 ;
            storageMapFloatArray["jet_deepJetScore_bb"][idx]   = 0.0 ;
            storageMapFloatArray["jet_deepJetScore_lepb"][idx]   = 0.0 ;
            storageMapFloatArray["jet_particleNetAK4_B"][idx] = 0.0 ;
            storageMapFloatArray["jet_particleNetAK4_CvsL"][idx] = 0.0 ;
            storageMapFloatArray["jet_particleNetAK4_CvsB"][idx] = 0.0 ;
            storageMapFloatArray["jet_particleNetAK4_QvsG"][idx] = 0.0 ;
            storageMapFloatArray["jet_particleNetAK4_puIdDisc"][idx] = 0.0 ;

            storageMapFloatArray["jet_flavour"][idx]        = 0.0 ;
            storageMapFloatArray["jet_pFlavour"][idx]       = 0.0 ;
            storageMapFloatArray["jet_bJetRegCorr"][idx]    = 0.0 ;
            storageMapFloatArray["jet_bJetRegRes"][idx]        = 0.0 ;

            storageMapFloatArray["jet_puJetIdMVA"][idx] = 0.0 ;
            storageMapFloatArray["jet_isLoose"][idx] = 0.0 ;
            storageMapFloatArray["jet_isTight"][idx] = 0.0 ;
            storageMapFloatArray["jet_isTight2017"][idx] = 0.0 ;
            storageMapFloatArray["jet_isTight2018"][idx] = 0.0 ;
            
            idx++;

    }
    idx=0;
    for( size_t ijet=0; ijet < jets.size(); ++ijet ) 
        {   
            // jets are ordered in pt
            auto recJet = jets[ijet];
            auto pt        = recJet->pt();
            storageMapFloatArray["jet_isValid"][idx]        = 1.0 ;
            storageMapFloatArray["jet_pt"][idx]        = recJet->pt();
            storageMapFloatArray["jet_eta"][idx]       = recJet->eta();
            storageMapFloatArray["jet_phi"][idx]       = recJet->phi();
            storageMapFloatArray["jet_mass"][idx]         = recJet->mass();
            storageMapFloatArray["jet_csvScore"][idx]  = recJet->bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags");
            storageMapFloatArray["jet_deepCSVScore"][idx]   = recJet->bDiscriminator("pfDeepCSVJetTags:probb") + recJet->bDiscriminator("pfDeepCSVJetTags:probbb");
            storageMapFloatArray["jet_deepJetScore"][idx]   = recJet->bDiscriminator("mini_pfDeepFlavourJetTags:probb")+
                                                              recJet->bDiscriminator("mini_pfDeepFlavourJetTags:probbb")+
                                                              recJet->bDiscriminator("mini_pfDeepFlavourJetTags:problepb");

            storageMapFloatArray["jet_deepJetScore_b"][idx]    = recJet->bDiscriminator("mini_pfDeepFlavourJetTags:probb")   ;
            storageMapFloatArray["jet_deepJetScore_bb"][idx]    = recJet->bDiscriminator("mini_pfDeepFlavourJetTags:probbb")  ;
            storageMapFloatArray["jet_deepJetScore_lepb"][idx]    = recJet->bDiscriminator("mini_pfDeepFlavourJetTags:problepb");

 //           std::cout<<"deepJets : "<<recJet->bDiscriminator("mini_pfDeepFlavourJetTags:probb")<<" | "
 //                                   <<recJet->bDiscriminator("mini_pfDeepFlavourJetTags:probbb")<<"  | "
 //                                   <<recJet->bDiscriminator("mini_pfDeepFlavourJetTags:problepb") << " | "
 //                                   <<std::endl;
            storageMapFloatArray["jet_particleNetAK4_B"][idx]    = pt>15   ? recJet->bDiscriminator("mini_pfParticleNetAK4DiscriminatorsJetTags:BvsAll"):-1 ;
            storageMapFloatArray["jet_particleNetAK4_CvsL"][idx] = pt > 15 ? recJet->bDiscriminator("mini_pfParticleNetAK4DiscriminatorsJetTags:CvsL"):-1 ; 
            storageMapFloatArray["jet_particleNetAK4_CvsB"][idx] = pt > 15 ? recJet->bDiscriminator("mini_pfParticleNetAK4DiscriminatorsJetTags:CvsB"):-1 ; 
            storageMapFloatArray["jet_particleNetAK4_QvsG"][idx] = pt > 15 ? recJet->bDiscriminator("mini_pfParticleNetAK4DiscriminatorsJetTags:QvsG"):-1 ; 
            storageMapFloatArray["jet_particleNetAK4_puIdDisc"][idx] = pt > 15 ? 1-recJet->bDiscriminator("mini_pfParticleNetAK4JetTags:probpu"):-1 ; 

            storageMapFloatArray["jet_flavour"][idx]        = recJet->hadronFlavour() ;
            storageMapFloatArray["jet_pFlavour"][idx]       = recJet->partonFlavour();
            storageMapFloatArray["jet_bJetRegCorr"][idx]    = recJet->userFloat("bRegNNCorr" );
            storageMapFloatArray["jet_bJetRegRes"][idx]        = recJet->userFloat("bRegNNResolution");

            storageMapFloatArray["jet_puJetIdMVA"][idx] = recJet->puJetIdMVA();
            storageMapFloatArray["jet_isLoose"][idx] = recJet->passesJetID( flashgg::Loose );
            storageMapFloatArray["jet_isTight"][idx] = recJet->passesJetID( flashgg::Tight );
            storageMapFloatArray["jet_isTight2017"][idx] = recJet->passesJetID( flashgg::Tight2017 );
            storageMapFloatArray["jet_isTight2018"][idx] = recJet->passesJetID( flashgg::Tight2018 );
            
            idx++;
            if (idx >= N_JET_MAX ) break;
        }
}

/*
void TrippleHTag::fillFatJetBranches()
{

    int idx=0;
    for( size_t ijet=0; ijet < N_FATJET_MAX; ++ijet ) 
    {
            storageMapFloatArray["fatJets_isValid"][idx]        = -1.0 ;
    }
    for( size_t ijet=0; ijet < jets->size(); ++ijet ) 
        {   
            // jets are ordered in pt
            auto &recJet = jets->ptrAt(ijet);
            storageMapFloatArray["fatJets_isValid"][idx]        = 1.0 ;
            storageMapFloatArray["fatJets_pt"][idx]        = recJet.pt();
            storageMapFloatArray["fatJets_eta"][idx]       = recJet.eta();
            storageMapFloatArray["fatJets_phi"][idx]       = recJet.phi();
            storageMapFloatArray["fatJets_mass"][idx]         = recJet.mass();
            storageMapFloatArray["fatJets_csvScore"][idx]  = recJet.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags");
            storageMapFloatArray["fatJets_deepCSVScore"][idx]   = recJet.bDiscriminator("pfDeepCSVJetTags:probb") + recJet.bDiscriminator("pfDeepCSVJetTags:probbb");
            storageMapFloatArray["fatJets_deepJetScore"][idx]   = recJet.bDiscriminator("pfDeepFlavourJetTags:probb")+
                                                               recJet.bDiscriminator("pfDeepFlavourJetTags:probbb")+
                                                               recJet.bDiscriminator("pfDeepFlavourJetTags:problepb");

            storageMapFloatArray["fatJets_flavour"][idx]        = recJet.hadronFlavour() ;
            storageMapFloatArray["fatJets_pFlavour"][idx]       = recJet.partonFlavour();
            storageMapFloatArray["fatJets_rawFactor"][idx] = 1.0 - recJet.jecFactor("Uncorrected");
            storageMapFloatArray["fatJets_msoftdrop"][idx] = recJet.groomedMass("SoftDropPuppi");
            storageMapFloatArray["fatJets_nConstituents"][idx] = recJet.numberOfDaughters();

            storageMapFloatArray["fatJets_btagDeepB"][idx] = (recJet.bDiscriminator("pfDeepCSVJetTags:probb")+recJet.bDiscriminator("pfDeepCSVJetTags:probbb")) >= 0 ?
                                               recJet.bDiscriminator("pfDeepCSVJetTags:probb")+recJet.bDiscriminator("pfDeepCSVJetTags:probbb") : -1 ; 
										//"DeepCSV b+bb tag discriminator"
            storageMapFloatArray["fatJets_btagCSVV2"][idx] = recJet.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags") ; 
										//" pfCombinedInclusiveSecondaryVertexV2 b-tag discriminator (aka CSVV2)"
            storageMapFloatArray["fatJets_btagHbb"][idx] = recJet.bDiscriminator("pfBoostedDoubleSecondaryVertexAK8BJetTags") ; 
										//"Higgs to BB tagger discriminator"
            storageMapFloatArray["fatJets_btagDDBvLV2"][idx] = recJet.bDiscriminator("pfMassIndependentDeepDoubleBvLV2JetTags:probHbb") ; 
										//"DeepDoubleX V2(mass-decorrelated) discriminator for H(Z)->bb vs QCD"
            storageMapFloatArray["fatJets_btagDDCvLV2"][idx] = recJet.bDiscriminator("pfMassIndependentDeepDoubleCvLV2JetTags:probHcc") ; 
										//"DeepDoubleX V2 (mass-decorrelated) discriminator for H(Z)->cc vs QCD"
            storageMapFloatArray["fatJets_btagDDCvBV2"][idx] = recJet.bDiscriminator("pfMassIndependentDeepDoubleCvBV2JetTags:probHcc") ; 
										//"DeepDoubleX V2 (mass-decorrelated) discriminator for H(Z)->cc vs H(Z)->bb"
            storageMapFloatArray["fatJets_deepTag_TvsQCD"][idx] = recJet.bDiscriminator("pfDeepBoostedDiscriminatorsJetTags:TvsQCD") ; 
										//"DeepBoostedJet tagger top vs QCD discriminator"
            storageMapFloatArray["fatJets_deepTag_WvsQCD"][idx] = recJet.bDiscriminator("pfDeepBoostedDiscriminatorsJetTags:WvsQCD") ; 
										//"DeepBoostedJet tagger W vs QCD discriminator"
            storageMapFloatArray["fatJets_deepTag_ZvsQCD"][idx] = recJet.bDiscriminator("pfDeepBoostedDiscriminatorsJetTags:ZvsQCD") ; 
										//"DeepBoostedJet tagger Z vs QCD discriminator"
            storageMapFloatArray["fatJets_deepTag_H"][idx] = recJet.bDiscriminator("pfDeepBoostedJetTags:probHbb")+recJet.bDiscriminator("pfDeepBoostedJetTags:probHcc")
                                                            + recJet.bDiscriminator("pfDeepBoostedJetTags:probHqqqq") ; 
										//"DeepBoostedJet tagger H(bb,cc,4q) sum"
            storageMapFloatArray["fatJets_deepTag_QCD"][idx] = recJet.bDiscriminator("pfDeepBoostedJetTags:probQCDbb")
                                                                +recJet.bDiscriminator("pfDeepBoostedJetTags:probQCDcc")
                                                                +recJet.bDiscriminator("pfDeepBoostedJetTags:probQCDb")
                                                                +recJet.bDiscriminator("pfDeepBoostedJetTags:probQCDc")
                                                                +recJet.bDiscriminator("pfDeepBoostedJetTags:probQCDothers") ; 
										//"DeepBoostedJet tagger QCD(bb,cc,b,c,others) sum"
            storageMapFloatArray["fatJets_deepTag_QCDothers"][idx] = recJet.bDiscriminator("pfDeepBoostedJetTags:probQCDothers") ; 
										//"DeepBoostedJet tagger QCDothers value"
            storageMapFloatArray["fatJets_deepTagMD_TvsQCD"][idx] = recJet.bDiscriminator("pfMassDecorrelatedDeepBoostedDiscriminatorsJetTags:TvsQCD") ; 
										//"Mass-decorrelated DeepBoostedJet tagger top vs QCD discriminator"
            storageMapFloatArray["fatJets_deepTagMD_WvsQCD"][idx] = recJet.bDiscriminator("pfMassDecorrelatedDeepBoostedDiscriminatorsJetTags:WvsQCD") ; 
										//"Mass-decorrelated DeepBoostedJet tagger W vs QCD discriminator"
            storageMapFloatArray["fatJets_deepTagMD_ZvsQCD"][idx] = recJet.bDiscriminator("pfMassDecorrelatedDeepBoostedDiscriminatorsJetTags:ZvsQCD") ; 
										//"Mass-decorrelated DeepBoostedJet tagger Z vs QCD discriminator"
            storageMapFloatArray["fatJets_deepTagMD_ZHbbvsQCD"][idx] = recJet.bDiscriminator("pfMassDecorrelatedDeepBoostedDiscriminatorsJetTags:ZHbbvsQCD") ; 
										//"Mass-decorrelated DeepBoostedJet tagger Z/H->bb vs QCD discriminator"
            storageMapFloatArray["fatJets_deepTagMD_ZbbvsQCD"][idx] = recJet.bDiscriminator("pfMassDecorrelatedDeepBoostedDiscriminatorsJetTags:ZbbvsQCD") ; 
										//"Mass-decorrelated DeepBoostedJet tagger Z->bb vs QCD discriminator"
            storageMapFloatArray["fatJets_deepTagMD_HbbvsQCD"][idx] = recJet.bDiscriminator("pfMassDecorrelatedDeepBoostedDiscriminatorsJetTags:HbbvsQCD") ; 
										//"Mass-decorrelated DeepBoostedJet tagger H->bb vs QCD discriminator"
            storageMapFloatArray["fatJets_deepTagMD_ZHccvsQCD"][idx] = recJet.bDiscriminator("pfMassDecorrelatedDeepBoostedDiscriminatorsJetTags:ZHccvsQCD") ; 
										//"Mass-decorrelated DeepBoostedJet tagger Z/H->cc vs QCD discriminator"
            storageMapFloatArray["fatJets_deepTagMD_H4qvsQCD"][idx] = recJet.bDiscriminator("pfMassDecorrelatedDeepBoostedDiscriminatorsJetTags:H4qvsQCD") ; 
										//"Mass-decorrelated DeepBoostedJet tagger H->4q vs QCD discriminator"
            storageMapFloatArray["fatJets_deepTagMD_bbvsLight"][idx] = recJet.bDiscriminator("pfMassDecorrelatedDeepBoostedDiscriminatorsJetTags:bbvsLight") ; 
										//"Mass-decorrelated DeepBoostedJet tagger Z/H/gluon->bb vs light flavour discriminator"
            storageMapFloatArray["fatJets_deepTagMD_ccvsLight"][idx] = recJet.bDiscriminator("pfMassDecorrelatedDeepBoostedDiscriminatorsJetTags:ccvsLight") ; 
										//"Mass-decorrelated DeepBoostedJet tagger Z/H/gluon->cc vs light flavour discriminator"
            storageMapFloatArray["fatJets_particleNet_TvsQCD"][idx] = recJet.bDiscriminator("pfParticleNetDiscriminatorsJetTags:TvsQCD") ; 
										//"ParticleNet tagger top vs QCD discriminator"
            storageMapFloatArray["fatJets_particleNet_WvsQCD"][idx] = recJet.bDiscriminator("pfParticleNetDiscriminatorsJetTags:WvsQCD") ; 
										//"ParticleNet tagger W vs QCD discriminator"
            storageMapFloatArray["fatJets_particleNet_ZvsQCD"][idx] = recJet.bDiscriminator("pfParticleNetDiscriminatorsJetTags:ZvsQCD") ; 
										//"ParticleNet tagger Z vs QCD discriminator"
            storageMapFloatArray["fatJets_particleNet_HbbvsQCD"][idx] = recJet.bDiscriminator("pfParticleNetDiscriminatorsJetTags:HbbvsQCD") ; 
										//"ParticleNet tagger H(->bb) vs QCD discriminator"
            storageMapFloatArray["fatJets_particleNet_HccvsQCD"][idx] = recJet.bDiscriminator("pfParticleNetDiscriminatorsJetTags:HccvsQCD") ; 
										//"ParticleNet tagger H(->cc) vs QCD discriminator"
            storageMapFloatArray["fatJets_particleNet_H4qvsQCD"][idx] = recJet.bDiscriminator("pfParticleNetDiscriminatorsJetTags:H4qvsQCD") ; 
										//"ParticleNet tagger H(->VV->qqqq) vs QCD discriminator"
            storageMapFloatArray["fatJets_particleNet_QCD"][idx] = recJet.bDiscriminator("pfParticleNetJetTags:probQCDbb")+recJet.bDiscriminator("pfParticleNetJetTags:probQCDcc")+recJet.bDiscriminator("pfParticleNetJetTags:probQCDb")+recJet.bDiscriminator("pfParticleNetJetTags:probQCDc")+recJet.bDiscriminator("pfParticleNetJetTags:probQCDothers") ; 
										//"ParticleNet tagger QCD(bb,cc,b,c,others) sum"
            storageMapFloatArray["fatJets_particleNet_mass"][idx] = recJet.bDiscriminator("pfParticleNetMassRegressionJetTags:mass") ; 
										//"ParticleNet mass regression"
            storageMapFloatArray["fatJets_particleNetMD_Xbb"][idx] = recJet.bDiscriminator("pfMassDecorrelatedParticleNetJetTags:probXbb") ; 
										//"Mass-decorrelated ParticleNet tagger raw X->bb score. For X->bb vs QCD tagging, use Xbb/(Xbb+QCD)"
            storageMapFloatArray["fatJets_particleNetMD_Xcc"][idx] = recJet.bDiscriminator("pfMassDecorrelatedParticleNetJetTags:probXcc") ; //"Mass-decorrelated ParticleNet tagger raw X->cc score. For X->cc vs QCD tagging, use Xcc/(Xcc+QCD)"
            storageMapFloatArray["fatJets_particleNetMD_Xqq"][idx] = recJet.bDiscriminator("pfMassDecorrelatedParticleNetJetTags:probXqq") ; //"Mass-decorrelated ParticleNet tagger raw X->qq (uds) score. For X->qq vs QCD tagging, use Xqq/(Xqq+QCD). For W vs QCD tagging, use (Xcc+Xqq)/(Xcc+Xqq+QCD)"
            storageMapFloatArray["fatJets_particleNetMD_QCD"][idx] = recJet.bDiscriminator("pfMassDecorrelatedParticleNetJetTags:probQCDbb")
                                                            +recJet.bDiscriminator("pfMassDecorrelatedParticleNetJetTags:probQCDcc")
                                                            +recJet.bDiscriminator("pfMassDecorrelatedParticleNetJetTags:probQCDb")
                                                            +recJet.bDiscriminator("pfMassDecorrelatedParticleNetJetTags:probQCDc")
                                                            +recJet.bDiscriminator("pfMassDecorrelatedParticleNetJetTags:probQCDothers") ; 
                                                            //"Mass-decorrelated ParticleNet tagger raw QCD score"
        idx++;

        if(idx > N_FATJET_MAX)
        {
            break;
        }
    }
}
*/

TrippleHTag *TrippleHTag::clone() const
{
    TrippleHTag *result = new TrippleHTag( *this );
    return result;
}

float TrippleHTag::getCosThetaStar_CS() const {

    TLorentzVector h_1(higgsCandidateLV[0]);
    h_1.Boost(-1*hhhLV_.BoostVector());
    return h_1.CosTheta();

}

float TrippleHTag::getCosThetaStar_CS_old(float ebeam) const {

    // cos theta star angle in the Collins Soper frame
    // Copied directly from here: https://github.com/ResonantHbbHgg/Selection/blob/master/selection.h#L3367-L3385
    TLorentzVector p1, p2;
    p1.SetPxPyPzE(0, 0,  ebeam, ebeam);
    p2.SetPxPyPzE(0, 0, -ebeam, ebeam);

    LorentzVector hh_lor = diPhoton()->p4() + quadjet_;
    TLorentzVector hh;
    hh.SetPxPyPzE(hh_lor.Px(),hh_lor.Py(),hh_lor.Pz(),hh_lor.E()) ;

    TVector3 boost = - hh.BoostVector();
    p1.Boost(boost);
    p2.Boost(boost);
    LorentzVector h1_lor = diPhoton()->p4();
    TLorentzVector h_1;
    h_1.SetPxPyPzE(h1_lor.Px(),h1_lor.Py(),h1_lor.Pz(),h1_lor.E()) ; 
    h_1.Boost(boost);

    TVector3 CSaxis = p1.Vect().Unit() - p2.Vect().Unit();
    CSaxis.Unit();
    

    return cos(   CSaxis.Angle( h_1.Vect().Unit() )    );
}


std::vector<float> TrippleHTag::CosThetaAngles() const {
    
    std::vector<float> helicityThetas;

    TLorentzVector BoostedHgg(0,0,0,0);
    BoostedHgg.SetPxPyPzE(diPhoton()->px(),diPhoton()->py(),diPhoton()->pz(),diPhoton()->energy()) ;
    
    TLorentzVector BoostedLeadingPhoton(0,0,0,0);
    BoostedLeadingPhoton.SetPxPyPzE(diPhoton()->leadingPhoton()->px(),diPhoton()->leadingPhoton()->py(),diPhoton()->leadingPhoton()->pz(),diPhoton()->leadingPhoton()->energy()) ;
    
    helicityThetas.push_back( HelicityCosTheta(BoostedHgg, BoostedLeadingPhoton) );
    
    TLorentzVector BoostedHbb(0,0,0,0);
    BoostedHbb.SetPxPyPzE(quadjet_.px(),quadjet_.py(),quadjet_.pz(),quadjet_.energy()) ;
    TLorentzVector BoostedLeadingJet(0,0,0,0);
    BoostedLeadingJet.SetPxPyPzE(h1LeadJet().px(),h1LeadJet().py(),h1LeadJet().pz(),h1LeadJet().energy()) ;

    helicityThetas.push_back( HelicityCosTheta(BoostedHbb, BoostedLeadingJet) );
    return helicityThetas;

}


float TrippleHTag::HelicityCosTheta( TLorentzVector Booster, TLorentzVector Boosted) const
{
    TVector3 BoostVector = Booster.BoostVector();
    Boosted.Boost( -BoostVector.x(), -BoostVector.y(), -BoostVector.z() );
    return Boosted.CosTheta();
}

float TrippleHTag::getPhoJetMinDr() const
{
    float PhoJetMinDr = min( min( deltaR( diPhoton()->leadingPhoton()->p4(), h1LeadJet().p4() ), deltaR( diPhoton()->leadingPhoton()->p4(), h1SubleadJet().p4() ) ), min( deltaR( diPhoton()->subLeadingPhoton()->p4(), h1LeadJet().p4() ), deltaR( diPhoton()->subLeadingPhoton()->p4(), h1SubleadJet().p4() ) ) );
    
    return PhoJetMinDr;
   //return 1e9;
}

float TrippleHTag::getPhoJetOtherDr() const
{
    float dR11 = deltaR( diPhoton()->leadingPhoton()->p4(), leadJet().p4() ); 
    float dR12 = deltaR( diPhoton()->leadingPhoton()->p4(), subleadJet().p4() );
    float dR21 = deltaR( diPhoton()->subLeadingPhoton()->p4(), leadJet().p4() ); 
    float dR22 = deltaR( diPhoton()->subLeadingPhoton()->p4(), subleadJet().p4() );

    float MinDr = min( min( dR11, dR12 ), min( dR21, dR22 ) );
    float PhoJetOtherDr = 0.0;     
    if( dR11 == MinDr ){ PhoJetOtherDr = dR22; }
    if( dR12 == MinDr ){ PhoJetOtherDr = dR21; }
    if( dR21 == MinDr ){ PhoJetOtherDr = dR12; }
    if( dR22 == MinDr ){ PhoJetOtherDr = dR11; }

    return PhoJetOtherDr;
}


float TrippleHTag::getSigmaMDecorr() const
{
    double mass_sigma[2]={0.,0.};
    double dummy[1]={0.};
    mass_sigma[0]=diPhoton()->mass();
    mass_sigma[1] = 0.5*sqrt((diPhoton()->leadingPhoton()->sigEOverE()*diPhoton()->leadingPhoton()->sigEOverE() + diPhoton()->subLeadingPhoton()->sigEOverE()*diPhoton()->subLeadingPhoton()->sigEOverE()));
    float sigmaMOverMDecorr=-99;
    //Splitting EBEB and !EBEB, using cuts as in preselection
    if(abs(diPhoton()->leadingPhoton()->superCluster()->eta())<1.4442 && abs(diPhoton()->subLeadingPhoton()->superCluster()->eta())<1.4442){
        sigmaMOverMDecorr = (*transfEBEB_)(mass_sigma,dummy);
    }
    else{
        sigmaMOverMDecorr = (*transfNotEBEB_)(mass_sigma,dummy);
    }
    return sigmaMOverMDecorr;
}

float TrippleHTag::getSigmaM1OverMJets() const
{
    float dijetSigmaMOverM = 1./pow(dijet1().M(),2)*sqrt(
                                         pow(h1LeadJet().userFloat("bRegNNResolution"),2)*pow(pow(h1LeadJet().p4().M(),2) + h1LeadJet().p4().Dot(h1SubleadJet().p4()) ,2)  + 
                                         pow(h1SubleadJet().userFloat("bRegNNResolution"),2)*pow( pow(h1SubleadJet().p4().M(),2) + h1SubleadJet().p4().Dot(h1LeadJet().p4()),2) 
                                                     );                                     
    return dijetSigmaMOverM;
}

float TrippleHTag::getSigmaM2OverMJets() const
{
    float dijetSigmaMOverM = 1./pow(dijet2().M(),2)*sqrt(
                                         pow(h2LeadJet().userFloat("bRegNNResolution"),2)*pow(pow(h2LeadJet().p4().M(),2) + h2LeadJet().p4().Dot(h2SubleadJet().p4()) ,2)  + 
                                         pow(h2SubleadJet().userFloat("bRegNNResolution"),2)*pow( pow(h2SubleadJet().p4().M(),2) + h2SubleadJet().p4().Dot(h2LeadJet().p4()),2) 
                                                     );                                     
    return dijetSigmaMOverM;
}

// Local Variables:
// mode:c++
// indent-tabs-mode:nil
// tab-width:4
// c-basic-offset:4
// End:
// vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

