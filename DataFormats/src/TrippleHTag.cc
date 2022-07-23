#include "flashgg/DataFormats/interface/TrippleHTag.h"

using namespace flashgg;

TrippleHTag::TrippleHTag() : DiPhotonTagBase::DiPhotonTagBase(), mva_(-2.) 
{  
}

TrippleHTag::~TrippleHTag() {}

TrippleHTag::TrippleHTag( edm::Ptr<flashgg::DiPhotonCandidate> diPho, 
                          edm::Ptr<flashgg::Jet> h1LeadJet , edm::Ptr<flashgg::Jet> h1SubleadJet ,
                          edm::Ptr<flashgg::Jet> h2LeadJet , edm::Ptr<flashgg::Jet> h2SubleadJet )
    : mva_(-.2), 
      MX_(0.),genMhhh_(0.),
      genCosThetaStar_CS_(0.),
      h1LeadJet_(h1LeadJet), 
      h1SubleadJet_(h1SubleadJet),  
      h2LeadJet_(h2LeadJet), 
      h2SubleadJet_(h2SubleadJet)
{   

    dipho_ = diPho;
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
}

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

