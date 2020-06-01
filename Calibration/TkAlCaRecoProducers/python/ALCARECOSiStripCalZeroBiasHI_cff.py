import FWCore.ParameterSet.Config as cms

# Set the HLT paths
import HLTrigger.HLTfilters.hltHighLevel_cfi
ALCARECOSiStripCalZeroBiasHLT = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone(
    andOr = True, # choose logical OR between Triggerbits
#    HLTPaths = [
#        #SiStripCalZeroBias
#        "HLT_ZeroBias",
#        #Random Trigger for Cosmic Runs
#        'RandomPath'
#        ],
    eventSetupPathsKey='SiStripCalZeroBiasHI',
    throw = False # tolerate triggers stated above, but not available
)

# Select only events where tracker had HV on (according to DCS bit information)
# AND respective partition is in the run (according to FED information)
import CalibTracker.SiStripCommon.SiStripDCSFilter_cfi
DCSStatusForSiStripCalZeroBias = CalibTracker.SiStripCommon.SiStripDCSFilter_cfi.siStripDCSFilter.clone()

# Select pp-like events based on the pixel cluster multiplicity
import HLTrigger.special.hltPixelActivityFilter_cfi
HLTPixelActivityFilterForSiStripCalZeroBias = HLTrigger.special.hltPixelActivityFilter_cfi.hltPixelActivityFilter.clone()
HLTPixelActivityFilterForSiStripCalZeroBias.maxClusters = 500
HLTPixelActivityFilterForSiStripCalZeroBias.inputTag    = 'siPixelClusters'

# Include masking only from Cabling and O2O
import CalibTracker.SiStripESProducers.SiStripQualityESProducer_cfi
siStripQualityESProducerUnbiased = CalibTracker.SiStripESProducers.SiStripQualityESProducer_cfi.siStripQualityESProducer.clone()
siStripQualityESProducerUnbiased.appendToDataLabel = 'unbiased'
siStripQualityESProducerUnbiased.ListOfRecordToMerge = cms.VPSet(
    cms.PSet(
        record = cms.string( 'SiStripDetCablingRcd' ), # bad components from cabling
        tag = cms.string( '' )
    ),
    cms.PSet(
        record = cms.string( 'SiStripBadChannelRcd' ), # bad components from O2O
        tag = cms.string( '' )
    )
)


# Clusterizer #
from RecoLocalTracker.SiStripClusterizer.SiStripClusterizer_cfi import *

calZeroBiasClusters = siStripClusters.clone()
calZeroBiasClusters.Clusterizer.QualityLabel = 'unbiased'

# Not persistent collections needed by the filters in the AlCaReco DQM
from DPGAnalysis.SiStripTools.eventwithhistoryproducerfroml1abc_cfi import *
from DPGAnalysis.SiStripTools.apvcyclephaseproducerfroml1tsDB_cfi import *

# SiStripQuality (only to test the different data labels)#
from DQMServices.Core.DQMEDAnalyzer import DQMEDAnalyzer
qualityStatistics = DQMEDAnalyzer("SiStripQualityStatistics",
                                  TkMapFileName = cms.untracked.string(''),
                                  dataLabel = cms.untracked.string('unbiased')
                                  )

# Sequence #
# Short-term workaround to preserve the "run for every event" while removing the use of convertToUnscheduled()
# To be reverted in a subsequent PR
seqALCARECOSiStripCalZeroBiasTask = cms.Task(calZeroBiasClusters,APVPhases,consecutiveHEs)
seqALCARECOSiStripCalZeroBias = cms.Sequence(ALCARECOSiStripCalZeroBiasHLT*HLTPixelActivityFilterForSiStripCalZeroBias*DCSStatusForSiStripCalZeroBias, seqALCARECOSiStripCalZeroBiasTask)
