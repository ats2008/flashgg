#!/usr/bin/env cmsRun

import FWCore.ParameterSet.Config as cms
import FWCore.Utilities.FileUtils as FileUtils
import FWCore.ParameterSet.VarParsing as VarParsing
from flashgg.Systematics.SystematicDumperDefaultVariables import minimalVariables,minimalHistograms,minimalNonSignalVariables,systematicVariables
from flashgg.Systematics.SystematicDumperDefaultVariables import minimalVariablesHTXS,systematicVariablesHTXS
import os
import copy
from flashgg.MetaData.MetaConditionsReader import *

# SYSTEMATICS SECTION
dropVBFInNonGold = False  # for 2015 only!

process = cms.Process("FLASHggSyst")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("Configuration.StandardSequences.GeometryDB_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32( 1000 )


systlabels = [""]
phosystlabels = []
metsystlabels = []
jetsystlabels = []
elesystlabels = []
musystlabels = []

from flashgg.MetaData.JobConfig import customize
customize.options.register('tthTagsOnly',
                           False,
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.bool,
                           'tthTagsOnly'
                           )
customize.options.register('doHHHGen',
                           False,
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.bool,
                           'doHHHGen'
                           )
customize.options.register('minNGoodJets',
                           1,
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.int,
                           'minNGoodJets'
                           )
customize.options.register('doPromptGen',
                           True,
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.bool,
                           'doPromptGen'
                           )
customize.options.register('doubleHTagsOnly',
                           False,
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.bool,
                           'doubleHTagsOnly'
                           )
customize.options.register('trippleHTagsOnly',
                           True,
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.bool,
                           'trippleHTagsOnly'
                           )
customize.options.register('addVBFDoubleHTag',
                           False,
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.bool,
                           'addVBFDoubleHTag'
                           )
customize.options.register('addVBFDoubleHVariables',
                           False,
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.bool,
                           'addVBFDoubleHVariables'
                           )
customize.options.register('doubleHTagsUseMjj',
                           False,
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.bool,
                           'doubleHTagsUseMjj'
                           )
customize.options.register('doubleHTagDumpMinVariables',
                           False,
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.bool,
                           'doubleHTagDumpMinVariables'
                           )
customize.options.register('ForceGenDiphotonProduction',
                           True,
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.bool,
                           'ForceGenDiphotonProduction'
                           )
customize.options.register('dumpGenWeight',
                           False,
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.bool,
                           'dumpGenWeight'
                           )
customize.options.register('trippleHReweight',
                           -1,
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.int,
                           'trippleHReweight'
                           )
customize.options.register('doubleHReweight',
                           -1,
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.int,
                           'doubleHReweight'
                           )
customize.options.register('doDoubleHTag',
                           False,
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.bool,
                           'doDoubleHTag'
                           )
customize.options.register('doTrippleHTag',
                           True,
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.bool,
                           'doTrippleHTag'
                           )
customize.options.register('doDoubleHttHKiller',
                           True,
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.bool,
                           'doDoubleHttHKiller'
                           )
customize.options.register('ttHKillerSaveInputVariables',
                           True,
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.bool,
                           'ttHKillerSaveInputVariables'
                           )
customize.options.register('doTrippleHGenAnalysis',
                           True,
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.bool,
                           'doTrippleHGenAnalysis'
                           )

customize.options.register('doDoubleHGenAnalysis',
                           False,
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.bool,
                           'doDoubleHGenAnalysis'
                           )
customize.options.register('doBJetRegression',
                           True,
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.bool,
                           'doBJetRegression'
                           )
customize.options.register('doHTXS',
                           False,
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.bool,
                           'doHTXS'
                           )
customize.options.register('doStageOne',
                           False,
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.bool,
                           'doStageOne'
                           )
customize.options.register('acceptance',
                           'NONE',
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.string,
                           'acceptance'
                           )
customize.options.register('doSystematics',
                           False,
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.bool,
                           'doSystematics'
                           )
customize.options.register('doGranularJEC',
                           False,
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.bool,
                           'doGranularJEC'
                           )
customize.options.register('doPdfWeights',
                           False,
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.bool,
                           'doPdfWeights'
                           )
customize.options.register('ignoreNegR9',
                           True,
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.bool,
                           'ignoreNegR9'
                           )
customize.options.register('dumpTrees',
                           True,
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.bool,
                           'dumpTrees'
                           )
customize.options.register('dumpWorkspace',
                           False,
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.bool,
                           'dumpWorkspace'
                           )
customize.options.register('verboseTagDump',
                           False,
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.bool,
                           'verboseTagDump'
                           )
customize.options.register('verboseSystDump',
                           False,
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.bool,
                           'verboseSystDump'
                           )
customize.options.register('analysisType',
                           'mainAnalysis',
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.string,
                           'analysisType'
                           )
customize.options.register('applyNNLOPSweight',
                           False,
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.bool,
                           'applyNNLOPSweight'
                           )
    


print "Printing defaults"
print 'acceptance '+str(customize.acceptance)
print 'tthTagsOnly '+str(customize.tthTagsOnly)
# import flashgg customization to check if we have signal or background
from flashgg.MetaData.JobConfig import customize
# set default options if needed
customize.setDefault("maxEvents",-1)
customize.setDefault("targetLumi",1.00e+3)
customize.parse()
customize.metaConditions = MetaConditionsReader(customize.metaConditions)

if customize.processId == "sig" or customize.processId.lower()=='signal':
    customize.doHHHGen = True

### Global Tag
from Configuration.AlCa.GlobalTag import GlobalTag
if customize.processId == "Data":
    process.GlobalTag.globaltag = str(customize.metaConditions['globalTags']['data'])
else:
    process.GlobalTag.globaltag = str(customize.metaConditions['globalTags']['MC'])

from flashgg.Systematics.SystematicsCustomize import *
jetSystematicsInputTags = createStandardSystematicsProducers(process , customize)
if dropVBFInNonGold:
    process.flashggVBFTag.SetArbitraryNonGoldMC = True
    process.flashggVBFTag.DropNonGoldData = True
modifyTagSequenceForSystematics(process,jetSystematicsInputTags)

print "Printing options"
print 'acceptance '+str(customize.acceptance)
print 'tthTagsOnly '+str(customize.tthTagsOnly)


# process.load("flashgg/Taggers/flashggTagSequence_cfi")
# process.flashggTagSequence = flashggPrepareTagSequence(customize.metaConditions)

# needed for 0th vertex from microAOD
if customize.tthTagsOnly:
    process.load("flashgg/MicroAOD/flashggDiPhotons_cfi")
    process.flashggDiPhotons.whichVertex = cms.uint32(0)
    process.flashggDiPhotons.useZerothVertexFromMicro = cms.bool(True)
    process.flashggDiPhotons.vertexIdMVAweightfile = customize.metaConditions['flashggDiPhotons']['vertexIdMVAweightfile'].encode("ascii")
    process.flashggDiPhotons.vertexProbMVAweightfile = customize.metaConditions['flashggDiPhotons']['vertexProbMVAweightfile'].encode("ascii")

print 'here we print the tag sequence before'
print process.flashggTagSequence

if customize.tthTagsOnly:
    process.flashggTagSequence.remove(process.flashggVBFTag)
    process.flashggTagSequence.remove(process.flashggVHMetTag)
    process.flashggTagSequence.remove(process.flashggWHLeptonicTag)
    process.flashggTagSequence.remove(process.flashggZHLeptonicTag)
    process.flashggTagSequence.remove(process.flashggVHHadronicTag)
    process.flashggTagSequence.remove(process.flashggUntagged)
    process.flashggTagSequence.remove(process.flashggVBFMVA)
    process.flashggTagSequence.remove(process.flashggVBFDiPhoDiJetMVA)
    process.flashggTagSequence.remove(process.flashggTTHHadronicTag) # Remove ttH tags as well, as we add these in later manually (with modified systematics worfklow)
    process.flashggTagSequence.remove(process.flashggTTHLeptonicTag)
    process.flashggTagSequence.remove(process.flashggTTHDiLeptonTag)
    process.flashggTagSequence.remove(process.flashggTHQLeptonicTag)

else:
    if not customize.doSystematics: # allow memory-intensive ttH MVAs if we are not running systematics
        allowLargettHMVAs(process)

if customize.doDoubleHTag:
    import flashgg.Systematics.doubleHCustomize 
    hhc = flashgg.Systematics.doubleHCustomize.DoubleHCustomize(process, customize, customize.metaConditions)
    minimalVariables += hhc.variablesToDump()
    systematicVariables = hhc.systematicVariables()

if customize.doTrippleHTag:
    import flashgg.Systematics.trippleHCustomize
    print(customize) 
    hhhc = flashgg.Systematics.trippleHCustomize.TrippleHCustomize(process, customize, customize.metaConditions)
    minimalVariables += hhhc.variablesToDump()
    systematicVariables = hhhc.systematicVariables()


if customize.doStageOne:
    assert (not customize.doHTXS)
    from flashgg.Systematics.stageOneCustomize import StageOneCustomize
    soc = StageOneCustomize(process, customize, customize.metaConditions)
    minimalVariables = soc.variablesToDump()
    systematicVariables = soc.systematicVariables()

process.flashggTHQLeptonicTag.processId = cms.string(str(customize.processId))

#print 'here we print the tag sequence after'
#print process.flashggTagSequence

if customize.tthTagsOnly:
    process.flashggTagSorter.TagPriorityRanges = cms.VPSet(   
        cms.PSet(TagName = cms.InputTag('flashggTTHLeptonicTag')),
        cms.PSet(TagName = cms.InputTag('flashggTTHHadronicTag')) 
    )

    print "customize.processId:",customize.processId

    print "Removing FracRVNvtxWeight from syst and adding  PixelSeed"
    
    newvpset = cms.VPSet()
    for pset in process.flashggDiPhotonSystematics.SystMethods:
        if not pset.Label.value().count("FracRVNvtxWeight") :
            print  pset.Label.value()
            newvpset += [pset]
    #from flashgg.Systematics.flashggDiPhotonSystematics_cfi import PixelSeedWeight #FIXME: this does not currently work, so comment it out for now
    #newvpset += [ PixelSeedWeight ]
    
    process.flashggDiPhotonSystematics.SystMethods = newvpset
   

print "customize.processId:",customize.processId
# load appropriate scale and smearing bins here
# systematics customization scripts will take care of adjusting flashggDiPhotonSystematics
#process.load("flashgg.Systematics.escales.escale76X_16DecRereco_2015")

# Or use the official tool instead
useEGMTools(process)

# Only run systematics for signal events
# convention: ggh vbf wzh (wh zh) tth
signal_processes = ["ggh_","vbf_","wzh_","wh_","zh_","bbh_","thq_","thw_","tth_","ggzh_","HHTo2B2G","GluGluHToGG","VBFHToGG","VHToGG","ttHToGG","Acceptance","hh","vbfhh","qqh","ggh","tth","vh"]
is_signal = reduce(lambda y,z: y or z, map(lambda x: customize.processId.count(x), signal_processes))

applyL1Prefiring = customizeForL1Prefiring(process, customize.metaConditions, customize.processId)

#if customize.processId.count("h_") or customize.processId.count("vbf_") or customize.processId.count("Acceptance") or customize.processId.count("hh_"): 
if is_signal:
    print "Signal MC, so adding systematics and dZ"
    if customize.doHTXS:
        variablesToUse = minimalVariablesHTXS
    else:
        variablesToUse = minimalVariables

    if customize.doSystematics:
        for direction in ["Up","Down"]:
            phosystlabels.append("MvaShift%s01sigma" % direction)
            phosystlabels.append("SigmaEOverEShift%s01sigma" % direction)
            phosystlabels.append("MaterialCentralBarrel%s01sigma" % direction)
            phosystlabels.append("MaterialOuterBarrel%s01sigma" % direction)
            phosystlabels.append("MaterialForward%s01sigma" % direction)
            phosystlabels.append("FNUFEB%s01sigma" % direction)
            phosystlabels.append("FNUFEE%s01sigma" % direction)
            phosystlabels.append("MCScaleGain6EB%s01sigma" % direction)
            phosystlabels.append("MCScaleGain1EB%s01sigma" % direction)
            jetsystlabels.append("JEC%s01sigma" % direction)
            jetsystlabels.append("JER%s01sigma" % direction)
            jetsystlabels.append("PUJIDShift%s01sigma" % direction)
            if customize.doGranularJEC:
                for sourceName in customize.metaConditions['flashggJetSystematics']['listOfSources']:
                    jetsystlabels.append("JEC%s%s01sigma" % (str(sourceName),direction))
            if customize.metaConditions['flashggJetSystematics']['doHEMuncertainty']:
                jetsystlabels.append("JetHEM%s01sigma" % direction)
            metsystlabels.append("metJecUncertainty%s01sigma" % direction)
            metsystlabels.append("metJerUncertainty%s01sigma" % direction)
            metsystlabels.append("metPhoUncertainty%s01sigma" % direction)
            metsystlabels.append("metUncUncertainty%s01sigma" % direction)
            variablesToUse.append("LooseMvaSF%s01sigma[1,-999999.,999999.] := weight(\"LooseMvaSF%s01sigma\")" % (direction,direction))
            variablesToUse.append("PreselSF%s01sigma[1,-999999.,999999.] := weight(\"PreselSF%s01sigma\")" % (direction,direction))
            variablesToUse.append("electronVetoSF%s01sigma[1,-999999.,999999.] := weight(\"electronVetoSF%s01sigma\")" % (direction,direction))
            variablesToUse.append("TriggerWeight%s01sigma[1,-999999.,999999.] := weight(\"TriggerWeight%s01sigma\")" % (direction,direction))
            variablesToUse.append("FracRVWeight%s01sigma[1,-999999.,999999.] := weight(\"FracRVWeight%s01sigma\")" % (direction,direction))
            variablesToUse.append("MuonIDWeight%s01sigma[1,-999999.,999999.] := getObjectWeight(\"Muon%sIDWeight%s01sigma\")" % (direction,str(customize.metaConditions["MUON_ID"]),direction))
            variablesToUse.append("ElectronIDWeight%s01sigma[1,-999999.,999999.] := getObjectWeight(\"ElectronIDWeight%s01sigma\")" % (direction,direction))
            variablesToUse.append("ElectronRecoWeight%s01sigma[1,-999999.,999999.] := getObjectWeight(\"ElectronRecoWeight%s01sigma\")" % (direction,direction))
            variablesToUse.append("MuonIsoWeight%s01sigma[1,-999999.,999999.] := getObjectWeight(\"Muon%sISOWeight%s01sigma\")" % (direction,str(customize.metaConditions['MUON_ISO']),direction))
            variablesToUse.append("JetBTagCutWeight%s01sigma[1,-999999.,999999.] := getObjectWeight(\"JetBTagCutWeight%s01sigma\")" % (direction,direction))
            variablesToUse.append("JetBTagReshapeWeight%s01sigma[1,-999999.,999999.] := getObjectWeight(\"JetBTagReshapeWeight%s01sigma\")" % (direction,direction))
            if applyL1Prefiring:
                variablesToUse.append("prefireWeight%s01sigma[1,-999999.,999999.] := weight(\"prefireWeight%s01sigma\")" % (direction,direction))
            variablesToUse.append("THU_ggH_Mu%s01sigma[1,-999999.,999999.] := getTheoryWeight(\"THU_ggH_Mu%s01sigma\")" % (direction,direction))
            variablesToUse.append("THU_ggH_Res%s01sigma[1,-999999.,999999.] := getTheoryWeight(\"THU_ggH_Res%s01sigma\")" % (direction,direction))
            variablesToUse.append("THU_ggH_Mig01%s01sigma[1,-999999.,999999.] := getTheoryWeight(\"THU_ggH_Mig01%s01sigma\")" % (direction,direction))
            variablesToUse.append("THU_ggH_Mig12%s01sigma[1,-999999.,999999.] := getTheoryWeight(\"THU_ggH_Mig12%s01sigma\")" % (direction,direction))
            variablesToUse.append("THU_ggH_VBF2j%s01sigma[1,-999999.,999999.] := getTheoryWeight(\"THU_ggH_VBF2j%s01sigma\")" % (direction,direction))
            variablesToUse.append("THU_ggH_VBF3j%s01sigma[1,-999999.,999999.] := getTheoryWeight(\"THU_ggH_VBF3j%s01sigma\")" % (direction,direction))
            variablesToUse.append("THU_ggH_PT60%s01sigma[1,-999999.,999999.] := getTheoryWeight(\"THU_ggH_PT60%s01sigma\")" % (direction,direction))
            variablesToUse.append("THU_ggH_PT120%s01sigma[1,-999999.,999999.] := getTheoryWeight(\"THU_ggH_PT120%s01sigma\")" % (direction,direction))
            variablesToUse.append("THU_ggH_qmtop%s01sigma[1,-999999.,999999.] := getTheoryWeight(\"THU_ggH_qmtop%s01sigma\")" % (direction,direction))
            for r9 in ["HighR9","LowR9"]:
                for region in ["EB","EE"]:
                    phosystlabels.append("ShowerShape%s%s%s01sigma"%(r9,region,direction))
#                    phosystlabels.append("MCSmear%s%s%s01sigma" % (r9,region,direction))
                    phosystlabels.append("MCScale%s%s%s01sigma" % (r9,region,direction))
                    for var in ["Rho","Phi"]:
                        phosystlabels.append("MCSmear%s%s%s%s01sigma" % (r9,region,var,direction))
        systlabels += phosystlabels
        systlabels += jetsystlabels
        systlabels += metsystlabels
    customizeSystematicsForSignal(process)
elif customize.processId == "Data":
    print "Data, so turn off all shifts and systematics, with some exceptions"
    variablesToUse = minimalNonSignalVariables
    customizeSystematicsForData(process)
else:
    print "Background MC, so store mgg and central only"
    variablesToUse = minimalNonSignalVariables
    customizeSystematicsForBackground(process)

if customize.doubleHTagsOnly:
    variablesToUse = minimalVariables
   # if customize.processId == "Data":
   #     variablesToUse = minimalNonSignalVariables
  
if customize.trippleHTagsOnly:
    variablesToUse = minimalVariables
   # if customize.processId == "Data":
   #     variablesToUse = minimalNonSignalVariables
  
if customize.doDoubleHTag:
   systlabels,jetsystlabels,metsystlabels = hhc.customizeSystematics(systlabels,jetsystlabels,metsystlabels)

if customize.doTrippleHTag:
   systlabels,jetsystlabels,metsystlabels = hhhc.customizeSystematics(systlabels,jetsystlabels,metsystlabels)
           

print "--- Systematics  with independent collections ---"
print systlabels
print "-------------------------------------------------"
print "--- Variables to be dumped, including systematic weights ---"
print variablesToUse
print "------------------------------------------------------------"

#from flashgg.Taggers.globalVariables_cff import globalVariables
#globalVariables.extraFloats.rho = cms.InputTag("rhoFixedGridAll")

#cloneTagSequenceForEachSystematic(process,systlabels,phosystlabels,jetsystlabels,jetSystematicsInputTags)
cloneTagSequenceForEachSystematic(process,systlabels,phosystlabels,metsystlabels,jetsystlabels,jetSystematicsInputTags)

# Dump an object called NoTag for untagged events in order to track QCD weights
# Will be broken if it's done for non-central values, so turn this on only for the non-syst tag sorter
process.flashggTagSorter.CreateNoTag = True # MUST be after tag sequence cloning
process.flashggTagSorter.isGluonFusion = cms.bool(bool(customize.processId.count("ggh")))
process.flashggTagSorter.applyNNLOPSweight = cms.bool(customize.applyNNLOPSweight)

###### Dumper section

from FWCore.ParameterSet.VarParsing import VarParsing
from flashgg.MetaData.samples_utils import SamplesManager

process.source = cms.Source ("PoolSource",
                             fileNames = cms.untracked.vstring(
                                 "file:/grid_mnt/t3storage3/athachay/trippleHiggs/hhhTo4b2g/flashgg/CMSSW_10_6_29/MicroAODProduction/results/mc/v1p3/c3_1_c4_1_HHHto4b2gamma_FS/c3_1_c4_1_FS_0.root"
                             ))

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("test.root"))

process.extraDumpers = cms.Sequence()

from flashgg.Taggers.TagsDumperCustomize import customizeTagsDumper
customizeTagsDumper(process, customize) ## move all the default tags dumper configuration to this function

if customize.processId == "tHq":
    import flashgg.Taggers.THQLeptonicTagVariables as var
    variablesToUse = minimalVariables + var.vtx_variables + var.dipho_variables

#tagList=[
#["UntaggedTag",4],
#["VBFTag",2],
#["VHTightTag",0],
#["VHLooseTag",0],
#["VHEtTag",0],
#["VHHadronicTag",0],
#["TTHHadronicTag",0],
##["TTHLeptonicTag",0]
#]

tag_only_variables = {}

if customize.tthTagsOnly:
    tagList=[
        ["TTHHadronicTag",4],
        ["TTHLeptonicTag",4]
        ]
elif customize.doubleHTagsOnly:
    tagList = hhc.tagList
    print "taglist is:"
    print tagList
    if customize.addVBFDoubleHTag and customize.addVBFDoubleHVariables:
        tag_only_variables["VBFDoubleHTag"] = hhc.vbfHHVariables()    
elif customize.trippleHTagsOnly:
    tagList = hhhc.tagList
    print "taglist is:"
    print tagList
elif customize.doStageOne:
    tagList = soc.tagList
else:
    tagList=[
           ["NoTag",0],
           ["UntaggedTag",4],
           ["VBFTag",3],
           ["ZHLeptonicTag",2],
           ["WHLeptonicTag",6],
           ["VHMetTag",2],
           ["VHHadronicTag",0],
           ["TTHHadronicTag",4],
           ["TTHLeptonicTag",4],
           ["THQLeptonicTag",0],
           ["TTHDiLeptonTag",0]
        ]

definedSysts=set()
process.tagsDumper.classifierCfg.remap=cms.untracked.VPSet()
import flashgg.Taggers.dumperConfigTools as cfgTools
for tag in tagList: 
  tagName=tag[0]
  tagCats=tag[1]
  # remap return value of class-based classifier
  process.tagsDumper.classifierCfg.remap.append( cms.untracked.PSet( src=cms.untracked.string("flashgg%s"%tagName), dst=cms.untracked.string(tagName) ) )
  for systlabel in systlabels:
      if not systlabel in definedSysts:
          # the cut corresponding to the systematics can be defined just once
          cutstring = "hasSyst(\"%s\") "%(systlabel)
          definedSysts.add(systlabel)
      else:
          cutstring = None
      if systlabel == "":
          currentVariables = copy.deepcopy(variablesToUse)
      else:
          if customize.doHTXS:
              currentVariables = copy.deepcopy(systematicVariablesHTXS)
          else:    
              currentVariables = copy.deepcopy(systematicVariables)
      if tagName.upper().count("NOTAG"):
          if customize.doHTXS:
              currentVariables = ["stage0bin[72,9.5,81.5] := tagTruth().HTXSstage0bin"]
          elif customize.doStageOne:
              currentVariables = copy.deepcopy(soc.noTagVariables())
          else:
              currentVariables = []
      isBinnedOnly = (systlabel !=  "")
      is_signal = reduce(lambda y,z: y or z, map(lambda x: customize.processId.count(x), signal_processes))
      if ( customize.doPdfWeights and customize.doSystematics ) and ( (customize.datasetName() and customize.datasetName().count("HToGG")) or customize.processId.count("h_") or customize.processId.count("vbf_") or is_signal ) and (systlabel ==  "") and not (customize.processId.count("bbh_") or customize.processId.count("thw_") or customize.processId.count("thq_")):
          #print "Signal MC central value, so dumping PDF weights"
          dumpPdfWeights = True
          nPdfWeights = 60
          nAlphaSWeights = 2
          nScaleWeights = 9
      else:
          #print "Data, background MC, or non-central value, or no systematics: no PDF weights"
          dumpPdfWeights = False
          nPdfWeights = -1
          nAlphaSWeights = -1
          nScaleWeights = -1

      if systlabel == "":
         if tagName in tag_only_variables.keys():
            currentVariables += tag_only_variables[tagName]
      cfgTools.addCategory(process.tagsDumper,
                           systlabel,
                           classname=tagName,
                           cutbased=cutstring,
                           subcats=tagCats, 
                           variables=currentVariables,
                           histograms=minimalHistograms,
                           binnedOnly=isBinnedOnly,
                           dumpPdfWeights=dumpPdfWeights,
                           nPdfWeights=nPdfWeights,
                           nAlphaSWeights=nAlphaSWeights,
                           nScaleWeights=nScaleWeights,
                           splitPdfByStage0Bin=customize.doHTXS,
                           splitPdfByStage1Bin=customize.doStageOne,
                           dumpGenWeight=customize.dumpGenWeight
                           )

# Require standard diphoton trigger
filterHLTrigger(process, customize)

process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

process.dataRequirements = cms.Sequence()
if customize.processId == "Data":
        process.dataRequirements += process.hltHighLevel

# Split WH and ZH
process.genFilter = cms.Sequence()
if ((customize.processId.count("wh") or customize.processId.count("zh")) and not (customize.processId.count("powheg"))) and not customize.processId.count("wzh") :
    print "enabling vh filter!!!!!"
    process.load("flashgg/Systematics/VHFilter_cfi")
    process.genFilter += process.VHFilter
    process.VHFilter.chooseW = bool(customize.processId.count("wh"))
    process.VHFilter.chooseZ = bool(customize.processId.count("zh"))

#no longer needed, we can pass these samples through the usual STXS classification code now
#if (customize.processId == "th_125" or customize.processId == "bbh_125"):
#    process.load("flashgg/Systematics/CentralHiggsFilter_cfi")
#    process.genFilter += process.CentralHiggsFilter

#pythia8 has an unanticipated EM showering feature, check have two photons from hard scatter
process.penultimateFilter= cms.Sequence()
if customize.processId == "th_125": # for this sample the filter removes also H -> ZG
    process.load("flashgg/Systematics/HardProcessFinalStateFilter_cfi")
#    process.HardProcessFinalStateFilter.debug = True
    process.penultimateFilter += process.HardProcessFinalStateFilter

# Split out prompt-fake or fake-fake
process.finalFilter = cms.Sequence()
if (customize.processId.count("qcd") or customize.processId.count("gjet")) and customize.processId.count("fake"):
    process.load("flashgg/Systematics/PromptFakeFilter_cfi")
    process.finalFilter += process.PromptFakeFilter
    if (customize.processId.count("promptfake")):
        process.PromptFakeFilter.doPromptFake = cms.bool(True)
        process.PromptFakeFilter.doFakeFake =cms.bool(False)
    elif (customize.processId.count("fakefake")):
        process.PromptFakeFilter.doPromptFake =cms.bool(False)
        process.PromptFakeFilter.doFakeFake =cms.bool(True)
    else:
        raise Exception,"Mis-configuration of python for prompt-fake filter"

# Met Filters
process.load('flashgg/Systematics/flashggMetFilters_cfi')

if customize.processId == "Data":
    metFilterSelector = "data"
    filtersInputTag = cms.InputTag("TriggerResults", "", "RECO")
else:
    metFilterSelector = "mc"
    filtersInputTag = cms.InputTag("TriggerResults", "", "PAT")

process.flashggMetFilters.requiredFilterNames = cms.untracked.vstring([filter.encode("ascii") for filter in customize.metaConditions["flashggMetFilters"][metFilterSelector]])
process.flashggMetFilters.filtersInputTag = filtersInputTag

if customize.tthTagsOnly:
    process.p = cms.Path(process.dataRequirements*
                         process.flashggMetFilters*
                         process.genFilter*
                         process.flashggDiPhotons* # needed for 0th vertex from microAOD
                         process.flashggDifferentialPhoIdInputsCorrection*
                         process.flashggDiPhotonSystematics*
                         process.flashggMetSystematics*
                         process.flashggMuonSystematics*process.flashggElectronSystematics*
                         (process.flashggUnpackedJets*process.jetSystematicsSequence)*
                         (process.flashggTagSequence*process.systematicsTagSequences)*
                         process.flashggSystTagMerger*
                         process.penultimateFilter*
                         process.finalFilter*
                         process.tagsDumper)
    # Now, we put the ttH tags back in the sequence with modified systematics workflow
    modifySystematicsWorkflowForttH(process, systlabels, phosystlabels, metsystlabels, jetsystlabels)

else:
    process.p = cms.Path(process.dataRequirements*
                         process.flashggMetFilters*
                         process.genFilter*
                         process.flashggDifferentialPhoIdInputsCorrection*
                         process.flashggDiPhotonSystematics*
                         process.flashggMetSystematics*
                         process.flashggMuonSystematics*process.flashggElectronSystematics*
                         (process.flashggUnpackedJets*process.jetSystematicsSequence)*
                         (process.flashggTagSequence*process.systematicsTagSequences)*
                         process.flashggSystTagMerger*
                         process.penultimateFilter*
                         process.finalFilter*
                         process.tagsDumper)
    if customize.doStageOne: 
        if soc.modifyForttH: soc.modifyWorkflowForttH(systlabels, phosystlabels, metsystlabels, jetsystlabels)

if customize.doBJetRegression:

    bregProducers = []
    doubleHTagProducers = []
    trippleHTagProducers = []   
 
    from flashgg.Taggers.flashggTags_cff import UnpackedJetCollectionVInputTag
    from flashgg.Taggers.flashggbRegressionProducer_cfi import flashggbRegressionProducer
    recoJetCollections = UnpackedJetCollectionVInputTag
    if customize.metaConditions['bRegression']['useBRegressionJERsf'] :
       bregJERJetsProducers,recoJetCollections = createJetSystematicsForBreg(process , customize)
       process.bregJERJetsProducers = cms.Sequence(reduce(lambda x,y: x+y, bregJERJetsProducers))

    jetsysts = cms.vstring()
    jetnames = cms.vstring()
    for jetsyst in [systlabels[0]]+jetsystlabels:
        jetsysts.append(jetsyst)
    for icoll,coll in enumerate(recoJetCollections):
        jetnames.append(coll.moduleLabel)
    producer = flashggbRegressionProducer.clone(JetSuffixes = jetsysts)
    producer.JetNames = jetnames
    producer.bRegressionWeightfile = cms.untracked.string(str(os.environ["CMSSW_BASE"]+customize.metaConditions['bRegression']['weightFile']))
    producer.y_mean = customize.metaConditions['bRegression']['y_mean']
    producer.y_std = customize.metaConditions['bRegression']['y_std']
    producer.year = cms.untracked.string(str(customize.metaConditions['bRegression']['year']))

    setattr(process,"bRegProducer",producer)
    bregProducers.append(producer)
    process.bregProducers = cms.Sequence(reduce(lambda x,y: x+y, bregProducers))
    if customize.metaConditions['bRegression']['useBRegressionJERsf'] :
       process.p.replace(process.jetSystematicsSequence,process.jetSystematicsSequence*process.bregJERJetsProducers*process.bregProducers)
    else : process.p.replace(process.jetSystematicsSequence,process.jetSystematicsSequence+process.bregProducers)
    

if customize.doDoubleHTag:
    process.p.remove(process.flashggMetFilters)
    hhc.doubleHTagRunSequence(systlabels,jetsystlabels,phosystlabels)
  
if customize.doTrippleHTag:
    process.p.remove(process.flashggMetFilters)
    hhhc.trippleHTagRunSequence(systlabels,jetsystlabels,phosystlabels)

if( not hasattr(process,"options") ): process.options = cms.untracked.PSet()
process.options.allowUnscheduled = cms.untracked.bool(True)

print "--- Dumping modules that take diphotons as input: ---"
mns = process.p.moduleNames()
for mn in mns:
    module = getattr(process,mn)
    if hasattr(module,"src") and type(module.src) == type(cms.InputTag("")) and module.src.value().count("DiPhoton"):
        print str(module),module.src
    elif hasattr(module,"DiPhotonTag"):
        print str(module),module.DiPhotonTag
print
printSystematicInfo(process)

### Rerun microAOD sequence on top of microAODs using the parent dataset
if customize.useParentDataset:
    runRivetSequence(process, customize.metaConditions, customize.processId)
    if customize.recalculatePDFWeights and is_signal and not (customize.processId.count("th_") or customize.processId.count("bbh_") or customize.processId.count("thw_") or customize.processId.count("thq_")):
        recalculatePDFWeights(process, customize.metaConditions)

#### BELOW HERE IS MOSTLY DEBUGGING STUFF

#####################################################################
## Memory and timing, n.b. igprof is very complicated to interpret ##
##################################################################### 

#from Validation.Performance.TimeMemoryInfo import customise as TimeMemoryCustomize
#TimeMemoryCustomize(process)
#process.MessageLogger.cerr.threshold = 'WARNING'

#process.load("IgTools.IgProf.IgProfTrigger")
#process.igprof.reportEventInterval     = cms.untracked.int32(250)
#process.igprof.reportToFileAtBeginJob  = cms.untracked.string("|gzip -c>igprof.begin-job.gz")
#process.igprof.reportToFileAtEvent     = cms.untracked.string("|gzip -c>igprof.%I.%E.%L.%R.event.gz")
#process.p += process.igprof

################################
## Dump merged tags to screen ##
################################

if customize.verboseTagDump:
    # crashes right now, dunno why - 02 May 2018
    pass
#    process.load("flashgg/Taggers/flashggTagTester_cfi")
#    process.flashggTagTester.TagSorter = cms.InputTag("flashggSystTagMerger")
#    process.flashggTagTester.ExpectMultiples = cms.untracked.bool(True)
#    process.p += process.flashggTagTester

############################################
## Additional details on tag sorter steps ##
############################################

if customize.verboseTagDump:
    process.flashggTagSorter.Debug = True
    customize.maxEvents = 10
                           
if customize.verboseSystDump:
    turnOnAllSystematicsDebug(process)
    customize.maxEVents = 10

##############
## Dump EDM ##
##############

#process.out = cms.OutputModule("PoolOutputModule", fileName = cms.untracked.string('CustomizeWillChangeThisAnyway.root'),
#                               outputCommands = cms.untracked.vstring('keep *') # dump everything! small tests only!
#                               )
#process.e = cms.EndPath(process.out)

############################
## Dump the output Python ##
############################
#print process.dumpPython()
#processDumpFile = open('processDump.py', 'w')
#print >> processDumpFile, process.dumpPython()
# call the customization
customize(process)

