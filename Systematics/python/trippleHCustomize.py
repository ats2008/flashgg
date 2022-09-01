import FWCore.ParameterSet.Config as cms
from  flashgg.Systematics.flashggJetSystematics_cfi import jetSystematicsCustomize

class TrippleHCustomize():
    """
    HH->bbgg process customizaton class
    """
    
    def __init__(self, process, customize, metaConditions):
        self.process = process
        self.customize = customize
        self.metaConditions = metaConditions
        self.tagList = [ ["TrippleHTag",12] ]
        self.customizeTagSequence()

    def vbfHHVariables(self):
        variables = [ 
        ]

        return variables

    def variablesToDump(self):
        var_workspace = []
        variables = []
        if(self.customize.trippleHTagsOnly):
            var_workspace += [
                "M1jj := dijet1().M()",
                "M2jj := dijet2().M()",
                "eventNumber := eventNumber()",
                "MX := MX()",
                "h1LeadingJet_pt := h1LeadJet().pt",
                "h1SubleadingJet_pt := h1SubleadJet().pt",
                "h2LeadingJet_pt := h2LeadJet().pt",
                "h2SubleadingJet_pt := h2SubleadJet().pt",
                "HHbbggMVA := MVA()"
            ]
            if self.customize.processId != "Data":
                var_workspace += [
                    "genMhh := genMhh()",
                    "genAbsCosThetaStar_CS := abs(genCosThetaStar_CS())",
                    'btagReshapeWeight := weight("JetBTagReshapeWeightCentral")',
                ]
                variables += [
                    "genMhhh := genMhhh()",
                    "genAbsCosThetaStar_CS := abs(genCosThetaStar_CS())",
                    
                    "h1LeadingJet_hflav := h1LeadJet().hadronFlavour()",
                    "h1LeadingJet_pflav := h1LeadJet().partonFlavour()",
                    "h1SubleadingJet_hflav := h1SubleadJet().hadronFlavour()",
                    "h1SubleadingJet_pflav := h1SubleadJet().partonFlavour()",
                    "h2LeadingJet_hflav := h2LeadJet().hadronFlavour()",
                    "h2LeadingJet_pflav := h2LeadJet().partonFlavour()",
                    "h2SubleadingJet_hflav := h2SubleadJet().hadronFlavour()",
                    "h2SubleadingJet_pflav := h2SubleadJet().partonFlavour()",

                    
                    'btagReshapeWeight := weight("JetBTagReshapeWeightCentral")',
                ]
            variables += [                
                "h1LeadingJet_bDis := h1LeadJet().bDiscriminator('pfCombinedInclusiveSecondaryVertexV2BJetTags')",#FIXME make the btag type configurable?
                "h1LeadingJet_DeepCSV := h1LeadJet().bDiscriminator('pfDeepCSVJetTags:probb')+h1LeadJet().bDiscriminator('pfDeepCSVJetTags:probbb')",#FIXME make the btag type configurable?
                "h1LeadingJet_DeepFlavour := h1LeadJet().bDiscriminator('mini_pfDeepFlavourJetTags:probb')+h1LeadJet().bDiscriminator('mini_pfDeepFlavourJetTags:probbb')+h1LeadJet().bDiscriminator('mini_pfDeepFlavourJetTags:problepb')",#FIXME make the btag type configurable?
                "h1LeadingJet_puJetIdMVA := h1LeadJet().puJetIdMVA()",
                "h1LeadingJet_QGL := h1LeadJet().QGL()",                

                "h1SubleadingJet_bDis := h1SubleadJet().bDiscriminator('pfCombinedInclusiveSecondaryVertexV2BJetTags')",
                "h1SubleadingJet_DeepCSV := h1SubleadJet().bDiscriminator('pfDeepCSVJetTags:probb')+h1SubleadJet().bDiscriminator('pfDeepCSVJetTags:probbb')",
                "h1SubleadingJet_DeepFlavour := h1SubleadJet().bDiscriminator('mini_pfDeepFlavourJetTags:probb')+h1SubleadJet().bDiscriminator('mini_pfDeepFlavourJetTags:probbb')+h1SubleadJet().bDiscriminator('mini_pfDeepFlavourJetTags:problepb')",#FIXME make the btag type configurable?
                "h1SubleadingJet_puJetIdMVA := h1SubleadJet().puJetIdMVA()",
                "h1SubleadingJet_QGL := h1SubleadJet().QGL()",


                "h2LeadingJet_bDis := h2LeadJet().bDiscriminator('pfCombinedInclusiveSecondaryVertexV2BJetTags')",#FIXME make the btag type configurable?
                "h2LeadingJet_DeepCSV := h2LeadJet().bDiscriminator('pfDeepCSVJetTags:probb')+h2LeadJet().bDiscriminator('pfDeepCSVJetTags:probbb')",#FIXME make the btag type configurable?
                "h2LeadingJet_DeepFlavour := h2LeadJet().bDiscriminator('mini_pfDeepFlavourJetTags:probb')+h2LeadJet().bDiscriminator('mini_pfDeepFlavourJetTags:probbb')+h2LeadJet().bDiscriminator('mini_pfDeepFlavourJetTags:problepb')",#FIXME make the btag type configurable?
                "h2LeadingJet_puJetIdMVA := h2LeadJet().puJetIdMVA()",
                "h2LeadingJet_QGL := h2LeadJet().QGL()", 
   
                "h2SubleadingJet_bDis := h2SubleadJet().bDiscriminator('pfCombinedInclusiveSecondaryVertexV2BJetTags')",
                "h2SubleadingJet_DeepCSV := h2SubleadJet().bDiscriminator('pfDeepCSVJetTags:probb')+h2SubleadJet().bDiscriminator('pfDeepCSVJetTags:probbb')",
                "h2SubleadingJet_DeepFlavour := h2SubleadJet().bDiscriminator('mini_pfDeepFlavourJetTags:probb')+h2SubleadJet().bDiscriminator('mini_pfDeepFlavourJetTags:probbb')+h2SubleadJet().bDiscriminator('mini_pfDeepFlavourJetTags:problepb')",#FIXME make the btag type configurable?
                "h2SubleadingJet_puJetIdMVA := h2SubleadJet().puJetIdMVA()",
                "h2SubleadingJet_QGL := h2SubleadJet().QGL()",                

                "absCosThetaStar_CS := abs(getCosThetaStar_CS())",
                "absCosThetaStar_CS_old := abs(getCosThetaStar_CS_old(6500))",
                "absCosTheta_bb := abs(CosThetaAngles()[1])",
                "absCosTheta_gg := abs(CosThetaAngles()[0])",
                "diphotonCandidatePtOverdiHiggsM := diphotonPtOverM()",
                "customLeadingPhotonIDMVA := diPhoton.leadingView.phoIdMvaWrtChosenVtx",
                "customSubLeadingPhotonIDMVA := diPhoton.subLeadingView.phoIdMvaWrtChosenVtx",
                "EGMLeadingPhotonIDMVA := diPhoton.leadingPhoton.userFloat('EGMPhotonMVA')",
                "EGMSubLeadingPhotonIDMVA := diPhoton.subLeadingPhoton.userFloat('EGMPhotonMVA')",
                "leadingPhotonSigOverE := diPhoton.leadingPhoton.sigEOverE",
                "subleadingPhotonSigOverE := diPhoton.subLeadingPhoton.sigEOverE",
                "sigmaMOverM := sqrt(0.5*(diPhoton.leadingPhoton.sigEOverE*diPhoton.leadingPhoton.sigEOverE + diPhoton.subLeadingPhoton.sigEOverE*diPhoton.subLeadingPhoton.sigEOverE))",
                "sigmaMOverMDecorr := getSigmaMDecorr()",
                "PhoJetMinDr := getPhoJetMinDr()",#up to here input variables to MVA
                "PhoJetOtherDr := getPhoJetOtherDr()",
                # "HHbbggMVA := MVA()",
                # "HHbbggMVAprob0 := MVAprob()[0]",
                
                "MX := MX()",
                
                "dije1CandidatePtOverdiHiggsM := dijet1PtOverM()",
                "dije2CandidatePtOverdiHiggsM := dijet2PtOverM()",
                
                "M1jj := dijet1().M()",
                "M2jj := dijet2().M()",
                
                "diphoton_pt := diPhoton.pt",
                "diphoton_eta := diPhoton.eta",
                "diphoton_phi := diPhoton.phi",
                
                "triHiggs_pt   := getTriHiggsP4().pt()",
                "triHiggs_mass := getTriHiggsP4().M()",
                "triHiggs_eta  := getTriHiggsP4().eta()",
                "triHiggs_phi  := getTriHiggsP4().phi()",
                "category := categoryNumber()",
                
                "leadingPhoton_pt := diPhoton.leadingPhoton.pt",
                "leadingPhoton_eta := diPhoton.leadingPhoton.eta",
                "leadingPhoton_phi := diPhoton.leadingPhoton.phi",
                "subleadingPhoton_pt := diPhoton.subLeadingPhoton.pt",
                "subleadingPhoton_eta := diPhoton.subLeadingPhoton.eta",
                "subleadingPhoton_phi := diPhoton.subLeadingPhoton.phi",
                
                
                "h1LeadingJet_pt := h1LeadJet().pt",
                "h1LeadingJet_eta := h1LeadJet().eta",
                "h1LeadingJet_phi := h1LeadJet().phi",
                "h1LeadingJet_mass := h1LeadJet().p4().M()",
                
                "h2LeadingJet_pt := h2LeadJet().pt",
                "h2LeadingJet_eta := h2LeadJet().eta",
                "h2LeadingJet_phi := h2LeadJet().phi",
                "h2LeadingJet_mass := h2LeadJet().p4().M()",
                
                "h1SubleadingJet_pt := h1SubleadJet().pt",
                "h1SubleadingJet_eta := h1SubleadJet().eta",
                "h1SubleadingJet_phi := h1SubleadJet().phi",
                "h1SubleadingJet_mass := h1SubleadJet().p4().M()",

                "h2SubleadingJet_pt := h2SubleadJet().pt",
                "h2SubleadingJet_eta := h2SubleadJet().eta",
                "h2SubleadingJet_phi := h2SubleadJet().phi",
                "h2SubleadingJet_mass := h2SubleadJet().p4().M()",

                "ntagMuons := ntagMuons()",
                "ntagElectrons := ntagElectrons()",
                "nMuons2018 := nMuons2018()",
                "nElectrons2018 := nElectrons2018()",
                #variables for the L2 energy regression
                "leadingJet_pt  := h1LeadJet().pt",
                "leadingJet_eta := h1LeadJet().eta",
                "leadingJet_phi := h1LeadJet().phi",
                "leadingJet_mass := h1LeadJet().p4().M()",
                "leadingJet_e := h1LeadJet().p4().E()",
                "leadingJet_DeepFlavour := h1LeadJet().bDiscriminator('mini_pfDeepFlavourJetTags:probb')+h1LeadJet().bDiscriminator('mini_pfDeepFlavourJetTags:probbb')+h1LeadJet().bDiscriminator('mini_pfDeepFlavourJetTags:problepb')", 
                "subleadingJet_pt  := h1SubleadJet().pt",
                "subleadingJet_eta := h1SubleadJet().eta",
                "subleadingJet_phi := h1SubleadJet().phi",
                "subleadingJet_mass := h1SubleadJet().p4().M()",
                "subleadingJet_e := h1SubleadJet().p4().E()",
                "subleadingJet_DeepFlavour := h1SubleadJet().bDiscriminator('mini_pfDeepFlavourJetTags:probb')+h1SubleadJet().bDiscriminator('mini_pfDeepFlavourJetTags:probbb')+h1SubleadJet().bDiscriminator('mini_pfDeepFlavourJetTags:problepb')",
                "corrMET := corrMET",
                "corrMETPhi := corrMETPhi",
                "MjjReg_phi12 := MjjReg_phi12",
                "MjjReg_phi1M := MjjReg_phi1M",
                "MjjReg_phi2M := MjjReg_phi2M",
                "year := year"          
            ]
            ##  Adding all jet information
            njetMax=8
            varsToGet=["jet_isValid","jet_pt",
                        "jet_eta","jet_phi",
                        "jet_mass","jet_csvScore",
                        "jet_deepCSVScore","jet_deepJetScore",
                        "jet_particleNetAK4_B","jet_particleNetAK4_CvsL",
                        "jet_particleNetAK4_CvsB","jet_particleNetAK4_QvsG",
                        "jet_particleNetAK4_puIdDisc","jet_flavour",
                        "jet_pFlavour","jet_bJetRegCorr",
                        "jet_bJetRegRes","jet_puJetIdMVA",
                        "jet_isLoose","jet_isTight",
                        "jet_isTight2017","jet_isTight2018" ]
            jetVarList=[]
            for jetVar in varsToGet:
                for i in range(njetMax):
                    jetVarList.append( jetVar.replace('_','_'+str(i)+'_')+' := getAK4JetDetails("'+jetVar+'" , '+ str(i) +' )' )
            variables += jetVarList
            print(jetVarList)

        if self.customize.doBJetRegression and self.customize.trippleHTagsOnly: variables +=[
                "h1LeadingJet_bRegNNCorr := h1LeadJet().userFloat('bRegNNCorr')",
                "h1LeadingJet_bRegNNResolution := h1LeadJet().userFloat('bRegNNResolution')",
                "h2LeadingJet_bRegNNCorr := h2LeadJet().userFloat('bRegNNCorr')",
                "h2LeadingJet_bRegNNResolution := h2LeadJet().userFloat('bRegNNResolution')",
                
                "h1SubleadingJet_bRegNNCorr := h1SubleadJet().userFloat('bRegNNCorr')",
                "h1SubleadingJet_bRegNNResolution := h1SubleadJet().userFloat('bRegNNResolution')",
                "h2SubleadingJet_bRegNNCorr := h2SubleadJet().userFloat('bRegNNCorr')",
                "h2SubleadingJet_bRegNNResolution := h2SubleadJet().userFloat('bRegNNResolution')",
                
                "sigmaM1Jets := getSigmaM1OverMJets()",
                "sigmaM2Jets := getSigmaM2OverMJets()",
                "leadingJet_bRegNNCorr := h1LeadJet().userFloat('bRegNNCorr')",
                "subleadingJet_bRegNNCorr :=  h1SubleadJet().userFloat('bRegNNCorr')"

        ]
        if self.customize.doubleHReweight > 0: 
            for num in range(0,12):  #12 benchmarks + 1 SM
                 variables += ["benchmark_reweight_%d := getBenchmarkReweight(%d)"%(num,num)]
                 var_workspace += ["benchmark_reweight_%d := getBenchmarkReweight(%d)"%(num,num)]
            variables += ["benchmark_reweight_SM := getBenchmarkReweight(12)"]
            variables += ["benchmark_reweight_box := getBenchmarkReweight(13)"]
            variables += ["benchmark_reweight_2017fake := getBenchmarkReweight(14)"]
            var_workspace += ["benchmark_reweight_SM := getBenchmarkReweight(12)"]
            var_workspace += ["benchmark_reweight_box := getBenchmarkReweight(13)"]
            var_workspace += ["benchmark_reweight_2017fake := getBenchmarkReweight(14)"]


        if self.customize.ttHKillerSaveInputVariables : variables += [
            "ttH_sumET := sumET()",
            "ttH_MET := MET()",
            "ttH_phiMET := phiMET()",
            "ttH_dPhi1 := dPhi1()",
            "ttH_dPhi2 := dPhi2()",
            "ttH_PhoJetMinDr := PhoJetMinDr()",
            "ttH_njets := njets()",
            "ttH_Xtt0 := Xtt0()",
            "ttH_Xtt1 := Xtt1()",
            "ttH_pte1 := pte1()",
            "ttH_pte2 := pte2()",
            "ttH_ptmu1 := ptmu1()",
            "ttH_ptmu2 := ptmu2()",
            "ttH_ptdipho := ptdipho()",
            "ttH_etae1 := etae1()",
            "ttH_etae2 := etae2()",
            "ttH_etamu1 := etamu1()",
            "ttH_etamu2 := etamu2()",
            "ttH_etadipho := etadipho()",
            "ttH_phie1 := phie1()",
            "ttH_phie2 := phie2()",
            "ttH_phimu1 := phimu1()",
            "ttH_phimu2 := phimu2()",
            "ttH_phidipho := phidipho()",
            "ttH_fabs_CosThetaStar_CS := fabs_CosThetaStar_CS()",
            "ttH_fabs_CosTheta_bb := fabs_CosTheta_bb()",
            "ttH_ptjet1 := ptjet1()",
            "ttH_ptjet2 := ptjet2()",
            "ttH_etajet1 := etajet1()",
            "ttH_etajet2 := etajet2()",
            "ttH_phijet1 := phijet1()",
            "ttH_phijet2 := phijet2()"
            ]
    
    
        if self.customize.doDoubleHttHKiller : 
             variables +=[
               "ttHScore := ttHScore()",
             ]
             var_workspace +=[
               "ttHScore := ttHScore()",
             ]
        print(" self.customize.doubleHTagDumpMinVariables : ",self.customize.doubleHTagDumpMinVariables)
        print(" self.customize.dumpWorkspace : ",self.customize.dumpWorkspace)
        if self.customize.doubleHTagDumpMinVariables or self.customize.dumpWorkspace :
            return var_workspace
        else :
            return variables


    def systematicVariables(self):
      systematicVariables=["CMS_hgg_mass[160,100,180]:=diPhoton().mass","Mjj[120,70,190]:=dijet().M()","HHbbggMVA[100,0,1.]:=MVA()","MX[300,250,5000]:=MX()","eventNumber[40,0.,1000000.]:=eventNumber()","genMhh[300,250,5000]:=genMhh()","genAbsCosThetaStar_CS[100,0,1]:=abs(genCosThetaStar_CS())",'btagReshapeWeight[100,-10.,10]:=weight("JetBTagReshapeWeightCentral")',"ntagMuons[100,0.,10] := ntagMuons()","ntagElectrons[100,0.,10] := ntagElectrons()","nMuons2018[100,0.,10] := nMuons2018()","nElectrons2018[100,0.,10] := nElectrons2018()","leadingJet_pt[100,0,1000] := leadJet().pt","subleadingJet_pt[100,0,1000] := subleadJet().pt"]
      
      if self.customize.doubleHReweight > 0: 
         for num in range(0,12):  #12 benchmarks
            systematicVariables += ["benchmark_reweight_%d[100,0,200] := getBenchmarkReweight(%d)"%(num,num)]
         systematicVariables+= ["benchmark_reweight_SM[100,0,200] := getBenchmarkReweight(12)"]
         systematicVariables+= ["benchmark_reweight_box[100,0,200] := getBenchmarkReweight(13)"]

      if self.customize.doDoubleHttHKiller : 
             systematicVariables +=["ttHScore[100,0,1.]:=ttHScore()"]

      return systematicVariables


    def customizeSystematics(self,systlabels,jetsystlabels,metsystlabels):
       for s in metsystlabels:
          systlabels.remove(s)
       metsystlabels = []
       if self.metaConditions['bRegression']['useBRegressionJERsf'] :
          for s in jetsystlabels:
             if "JER" in s :
                systlabels.remove(s)
                jetsystlabels.remove(s)
          if self.customize.doSystematics:
             for direction in ["Up","Down"]:
                jetsystlabels.append("JERbreg%s01sigma" % direction)
                systlabels.append("JERbreg%s01sigma" % direction)
       return systlabels,jetsystlabels,metsystlabels

    def customizeTagSequence(self):
        self.process.load("flashgg.Taggers.flashggTrippleHTag_cff")

        # customizing training file (with/wo Mjj) 
        training_type = 'with_Mjj' if self.customize.doubleHTagsUseMjj else 'wo_Mjj' 
        
        self.process.flashggTrippleHTag.MVAConfig.weights=cms.FileInPath(str(self.metaConditions["trippleHTag"]["weightsFile"][training_type]))  
        self.process.flashggTrippleHTag.MVAFlatteningFileName = cms.untracked.FileInPath(str(self.metaConditions["trippleHTag"]["MVAFlatteningFileName"][training_type]))
        if training_type == 'with_Mjj' :
            self.process.flashggTrippleHTag.MVABoundaries = cms.vdouble(0.44,0.67,0.79)
            self.process.flashggTrippleHTag.MXBoundaries = cms.vdouble(250.,385.,470.,640.,250.,345.,440.,515.,250.,330.,365.,545.)
            self.process.flashggTrippleHTag.ttHScoreThreshold = cms.double(0.) #0.26
        elif training_type == 'wo_Mjj' :
            self.process.flashggTrippleHTag.MVAConfig.variables.pop(0) 
            self.process.flashggTrippleHTag.MVABoundaries = cms.vdouble(0.37,0.62,0.78)
            self.process.flashggTrippleHTag.MXBoundaries = cms.vdouble(250., 385.,510.,600.,250.,330.,360.,540.,250.,330.,375.,585.)
            self.process.flashggTrippleHTag.ttHScoreThreshold = cms.double(0.26) #0.26
        
        #TODO  : CUSTOMIZE THE TTH KILLER BYPASS
        
        self.process.flashggTrippleHTag.ttHScoreThreshold = cms.double(-1e6) #0.26


        # customizing training file (with/wo Mjj) 
        training_type = 'with_Mjj' if self.customize.doubleHTagsUseMjj else 'wo_Mjj'



        if training_type == 'with_Mjj' :
            pass
        elif training_type == 'wo_Mjj' :
            pass
        ## customize meta conditions

        self.process.flashggTrippleHTag.JetIDLevel=cms.string(str(self.metaConditions["trippleHTag"]["jetID"]))
        self.process.flashggTrippleHTag.MVAscaling = cms.double(self.metaConditions["trippleHTag"]["MVAscalingValue"])
        self.process.flashggTrippleHTag.dottHTagger = cms.bool(self.customize.doDoubleHttHKiller)
        self.process.flashggTrippleHTag.ttHWeightfile = cms.untracked.FileInPath(str(self.metaConditions["trippleHTag"]["ttHWeightfile"]))
        self.process.flashggTrippleHTag.ttHKiller_mean = cms.vdouble(self.metaConditions["trippleHTag"]["ttHKiller_mean"])
        self.process.flashggTrippleHTag.ttHKiller_std = cms.vdouble(self.metaConditions["trippleHTag"]["ttHKiller_std"])
        self.process.flashggTrippleHTag.ttHKiller_listmean = cms.vdouble(self.metaConditions["trippleHTag"]["ttHKiller_listmean"])
        self.process.flashggTrippleHTag.ttHKiller_liststd = cms.vdouble(self.metaConditions["trippleHTag"]["ttHKiller_liststd"])
        self.process.flashggTrippleHTag.MaxJetEta = cms.double(self.metaConditions["bTagSystematics"]["eta"])

        ## add double Higgs tag to the tag sequence
        #  self.process.flashggTagSequence.replace(self.process.flashggUntagged,(self.process.flashggTrippleHTag+self.process.flashggUntagged))

        ## remove single Higgs tags
        if self.customize.trippleHTagsOnly:
            self.process.flashggTagSequence.remove(self.process.flashggVBFTag)
            self.process.flashggTagSequence.remove(self.process.flashggTTHLeptonicTag)
            self.process.flashggTagSequence.remove(self.process.flashggTTHHadronicTag)
            self.process.flashggTagSequence.remove(self.process.flashggVHEtTag)
            self.process.flashggTagSequence.remove(self.process.flashggVHLooseTag)
            self.process.flashggTagSequence.remove(self.process.flashggVHTightTag)
            self.process.flashggTagSequence.remove(self.process.flashggVHMetTag)
            self.process.flashggTagSequence.remove(self.process.flashggWHLeptonicTag)
            self.process.flashggTagSequence.remove(self.process.flashggZHLeptonicTag)
            self.process.flashggTagSequence.remove(self.process.flashggVHLeptonicLooseTag)
            self.process.flashggTagSequence.remove(self.process.flashggVHHadronicTag)
            self.process.flashggTagSequence.remove(self.process.flashggVBFMVA)
            self.process.flashggTagSequence.remove(self.process.flashggVHhadMVA)
            self.process.flashggTagSequence.remove(self.process.flashggVBFDiPhoDiJetMVA)
            self.process.flashggTagSequence.remove(self.process.flashggTTHDiLeptonTag)
            self.process.flashggTagSequence.remove(self.process.flashggUntagged)
            self.process.flashggTagSequence.remove(self.process.flashggUntagged)
            self.process.flashggTagSequence.remove(self.process.flashggTHQLeptonicTag)
 
    def trippleHTagMerger(self,systlabels=[]):
        '''
        merging step taking into account that different syst variations are produced by the same producer in the case of the HH tags
        '''

        self.process.p.remove(self.process.flashggTagSorter) 

        self.process.p.replace(self.process.flashggSystTagMerger,self.process.flashggTrippleHTagSequence*self.process.flashggTagSorter*self.process.flashggSystTagMerger)

        for systlabel in systlabels:
            if systlabel!='':
                self.process.p.remove(getattr(self.process,'flashggTagSorter'+systlabel))
                self.process.p.replace(self.process.flashggSystTagMerger,getattr(self.process, 'flashggTagSorter'+systlabel)*self.process.flashggSystTagMerger)            
            else:
                setattr(getattr(self.process, 'flashggTagSorter'+systlabel), 'TagPriorityRanges', cms.VPSet( cms.PSet(TagName = cms.InputTag('flashggTrippleHTag', systlabel))))
                 

    def trippleHTagRunSequence(self,systlabels,jetsystlabels,phosystlabels):
        if self.customize.trippleHTagsOnly: 
            self.trippleHTagMerger(systlabels)

        if len(systlabels)>1 :
            getattr(self.process, "flashggTrippleHTag").JetsSuffixes = cms.vstring([systlabels[0]]+jetsystlabels)
            getattr(self.process, "flashggTrippleHTag").DiPhotonSuffixes = cms.vstring([systlabels[0]]+phosystlabels)

        if self.customize.doTrippleHGenAnalysis:
            self.addGenAnalysis()


    def addGenAnalysis(self):
        if self.customize.processId == "Data": 
            return 

        import flashgg.Taggers.dumperConfigTools as cfgTools
        ## load gen-level bbgg 
        self.process.load( "flashgg.MicroAOD.flashggGenDiPhotonDiBJetsSequence_cff" )

        ## match gen-level to reco tag
        self.process.load("flashgg.Taggers.flashggTaggedGenDiphotons_cfi")
        self.process.flashggTaggedGenDiphotons.src  = "flashggSelectedGenDiPhotonDiBJets"
        self.process.flashggTaggedGenDiphotons.tags = "flashggTagSorter"
        self.process.flashggTaggedGenDiphotons.remap = self.process.tagsDumper.classifierCfg.remap
        self.process.flashggTaggedGenDiphotons.ForceGenDiphotonProduction = self.customize.ForceGenDiphotonProduction

        ## prepare gen-level dumper
        self.process.load("flashgg.Taggers.genDiphotonDumper_cfi")
        self.process.genDiphotonDumper.dumpTrees = True
        self.process.genDiphotonDumper.dumpWorkspace = False
        self.process.genDiphotonDumper.src = "flashggTaggedGenDiphotons"

        from flashgg.Taggers.globalVariables_cff import globalVariables
        self.process.genDiphotonDumper.dumpGlobalVariables = True
        self.process.genDiphotonDumper.globalVariables = globalVariables

        genVariables = ["absCosThetaStar_CS := abs(getcosthetaHHgen())",
                        "mhh := getmHHgen()",
                        "ptH1 := getptH1gen()",
                        "ptH2 := getptH2gen()"
                       ]

        if not self.customize.ForceGenDiphotonProduction:
            genVariables += ["mgg := mass",
                             "mbb := dijet.mass",
                             "leadPho_px := leadingPhoton.px",
                             "leadPho_py := leadingPhoton.py",
                             "leadPho_pz := leadingPhoton.pz",
                             "leadPho_e  := leadingPhoton.energy",
                             "subleadPho_px := subLeadingPhoton.px",
                             "subleadPho_py := subLeadingPhoton.py",
                             "subleadPho_pz := subLeadingPhoton.pz",
                             "subleadPho_e  := subLeadingPhoton.energy",
                             
                             "leadJet_px := leadingJet.px",
                             "leadJet_py := leadingJet.py",
                             "leadJet_pz := leadingJet.pz",
                             "leadJet_e  := leadingJet.energy",
                             "subleadJet_px := subLeadingJet.px",
                             "subleadJet_py := subLeadingJet.py",
                             "subleadJet_pz := subLeadingJet.pz",
                             "subleadJet_e  := subLeadingJet.energy",
                            ]
            
        ## define categories for gen-level dumper
        cfgTools.addCategory(self.process.genDiphotonDumper,  ## events with not reco-level tag
                             "NoTag", 'isTagged("flashggNoTag")',1,
                             variables=genVariables,
                             dumpGenWeight=self.customize.dumpGenWeight
                             )

        for tag in self.tagList: ## tagged events
            tagName,subCats = tag
            # need to define all categories explicitely because cut-based classifiers does not look at sub-category number
            for isub in xrange(subCats):
                cfgTools.addCategory(self.process.genDiphotonDumper,
                                     "%s_%d" % ( tagName, isub ), 
                                     'isTagged("%s") && categoryNumber == %d' % (tagName, isub),0,
                                     variables=genVariables,##+recoVariables
                                     dumpGenWeight=self.customize.dumpGenWeight
                                     )

        self.process.genp = cms.Path(self.process.flashggGenDiPhotonDiBJetsSequence*self.process.flashggTaggedGenDiphotons*self.process.genDiphotonDumper)
