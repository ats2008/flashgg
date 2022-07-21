#ifndef flashgg_TrippleHTag
#define flashgg_TrippleHTag

#include "TLorentzVector.h"

#include "flashgg/DataFormats/interface/DiPhotonTagBase.h"
#include "flashgg/DataFormats/interface/Jet.h"
#include "DataFormats/Candidate/interface/LeafCandidate.h"
#include "DataFormats/Math/interface/deltaR.h"

#include "flashgg/Taggers/interface/FunctionHelpers.h"

namespace flashgg {

    class TrippleHTag: public DiPhotonTagBase, public reco::LeafCandidate
    {
      public:
        TrippleHTag();
        ~TrippleHTag();

        TrippleHTag( edm::Ptr<DiPhotonCandidate>, edm::Ptr<flashgg::Jet>, edm::Ptr<flashgg::Jet>,edm::Ptr<flashgg::Jet>, edm::Ptr<flashgg::Jet>  );
        virtual TrippleHTag *clone() const override;
        
        float ttHScore_;
        float ntagMuons_, ntagElectrons_,nMuons2018_,nElectrons2018_;
        float sumET_, MET_, phiMET_, dPhi1_, dPhi2_, PhoJetMinDr_,PhoJetOtherDr_, njets_, Xtt0_, Xtt1_, pte1_, pte2_, ptmu1_, ptmu2_, ptdipho_, etae1_, etae2_, etamu1_, etamu2_, etadipho_, phie1_, phie2_, phimu1_, phimu2_, phidipho_, fabs_CosThetaStar_CS_, fabs_CosTheta_bb_, mjj_, ptjet1_, ptjet2_, etajet1_, etajet2_, phijet1_, phijet2_; 

        void setMVA(double x) { mva_ = x; }
        double MVA() const { return mva_; }
 
 //  void setMVAprob(std::vector<float> &x) const { mva_prob_ = x; }
 //  std::vector<float> MVAprob() const { return mva_prob_; }
 
        void setMX(double x) { MX_ = x; }
        double MX() const { return MX_; }
        void setGenMhh(double x) { genMhh_ = x; }
        double genMhh() const { return genMhh_; }
        void setGenCosThetaStar_CS(double x) { genCosThetaStar_CS_ = x; }
        double genCosThetaStar_CS() const { return genCosThetaStar_CS_; }
        float ttHScore() const { return ttHScore_; }
        float ntagMuons() const { return ntagMuons_; }
        float ntagElectrons() const { return ntagElectrons_; }
        float nMuons2018() const { return nMuons2018_; }
        float nElectrons2018() const { return nElectrons2018_; }
        double diphotonPtOverM() const {return diPhoton()->pt()/mass(); }
        double dijet1PtOverM() const {return dijet1().pt()/mass(); }
        double dijet2PtOverM() const {return dijet2().pt()/mass(); }

        const flashgg::Jet & leadJet() const { return h1LeadJet(); } 
        const flashgg::Jet & subleadJet() const { return h1SubleadJet(); } 
        
        const flashgg::Jet & h1LeadJet() const { return *h1LeadJet_; } 
        const flashgg::Jet & h1SubleadJet() const { return *h1SubleadJet_; } 
        const flashgg::Jet & h2LeadJet() const { return *h2LeadJet_; } 
        const flashgg::Jet & h2SubleadJet() const { return *h2SubleadJet_; } 
        
        const LorentzVector & dijet() const { return dijet1(); }
        const LorentzVector & dijet1() const { return dijet1_; }
        const LorentzVector & dijet2() const { return dijet2_; }

        float getCosThetaStar_CS() const;
        float getCosThetaStar_CS_old(float ebeam) const;
        std::vector<float> CosThetaAngles() const;
        float HelicityCosTheta( TLorentzVector Booster, TLorentzVector Boosted) const;
        float getPhoJetMinDr() const;
        float getPhoJetOtherDr() const;
        float getSigmaMDecorr() const;
        float getSigmaMOverMJets() const;
        void  setSigmaMDecorrTransf( DecorrTransform* transfEBEB, DecorrTransform* transfNotEBEB){ transfEBEB_= transfEBEB; transfNotEBEB_=transfNotEBEB;}
        LorentzVector getdiHiggsP4() const {return p4();}
        void setBenchmarkReweight(std::vector<float> x) { benchmark_reweights_ = x; }
        float getBenchmarkReweight(int targetNode) const { return benchmark_reweights_[targetNode]; }
        void setEventNumber(double x) { eventNumber_ = x; }
        double eventNumber() const { return eventNumber_; }

        float sumET() const {return sumET_;}
        float MET() const {return MET_;}
        float phiMET() const {return phiMET_;}
        float dPhi1() const {return dPhi1_;}
        float dPhi2() const {return dPhi2_;}
        float PhoJetMinDr() const {return PhoJetMinDr_;}
        float PhoJetOtherDr() const {return PhoJetOtherDr_;}
        float njets() const {return njets_;}
        float mjj() const {return mjj_;}
        float Xtt0() const {return Xtt0_;}
        float Xtt1() const {return Xtt1_;}
        float pte1() const {return pte1_;}
        float pte2() const {return pte2_;}
        float ptmu1() const {return ptmu1_;}
        float ptmu2() const {return ptmu2_;}
        float ptdipho() const {return ptdipho_;}
        float ptjet1() const {return ptjet1_;}
        float ptjet2() const {return ptjet2_;}
        float etajet1() const {return etajet1_;}
        float etajet2() const {return etajet2_;}
        float phijet1() const {return phijet1_;}
        float phijet2() const {return phijet2_;}
        float etae1() const {return etae1_;}
        float etae2() const {return etae2_;}
        float etamu1() const {return etamu1_;}
        float etamu2() const {return etamu2_;}
        float etadipho() const {return etadipho_;}
        float phie1() const {return phie1_;}
        float phie2() const {return phie2_;}
        float phimu1() const {return phimu1_;}
        float phimu2() const {return phimu2_;}
        float phidipho() const {return phidipho_;}
        float fabs_CosThetaStar_CS() const {return fabs_CosThetaStar_CS_;}
        float fabs_CosTheta_bb() const {return fabs_CosTheta_bb_;}
        
        void setDHH( float dHH_) {  dHH=dHH_  ;} 

    private:
        double mva_, MX_, genMhh_,genCosThetaStar_CS_;
        vector<float> benchmark_reweights_;
 //       std::vector<float> mva_prob_;
        long eventNumber_;
        edm::Ptr<flashgg::Jet> h1LeadJet_, h1SubleadJet_;
        edm::Ptr<flashgg::Jet> h2LeadJet_, h2SubleadJet_;
        
        TLorentzVector diPhotonLV;
        TLorentzVector h1LeadJetLV_, h1SubleadJetLV_;
        TLorentzVector h2LeadJetLV_, h2SubleadJetLV_;
        TLorentzVector higgsCandidateLV[3], hhhLV_;
        
        LorentzVector quadjet_,dijet1_,dijet2_;
        DecorrTransform* transfEBEB_;
        DecorrTransform* transfNotEBEB_;
        float dHH;
        
    };
}

#endif
// Local Variables:
// mode:c++
// indent-tabs-mode:nil
// tab-width:4
// c-basic-offset:4
// End:
// vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

