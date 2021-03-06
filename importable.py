importableFormats = ['','AlignedDNAFASTAFormat', 'AlignedDNASequencesDirectoryFormat', 
'AlphaDiversityDirectoryFormat', 'AlphaDiversityFormat', 'BIOMV100DirFmt', 'BIOMV100Format', 
'BIOMV210DirFmt', 'BIOMV210Format', 'BooleanSeriesDirectoryFormat', 'BooleanSeriesFormat', 
'Bowtie2IndexDirFmt', 'CasavaOneEightLanelessPerSampleDirFmt', 'CasavaOneEightSingleLanePerSampleDirFmt', 
'DADA2StatsDirFmt', 'DADA2StatsFormat', 'DNAFASTAFormat', 'DNASequencesDirectoryFormat', 'DeblurStatsDirFmt', 
'DeblurStatsFmt', 'DifferentialDirectoryFormat', 'DifferentialFormat', 'DistanceMatrixDirectoryFormat', 
'EMPPairedEndCasavaDirFmt', 'EMPPairedEndDirFmt', 'EMPSingleEndCasavaDirFmt', 'EMPSingleEndDirFmt', 
'ErrorCorrectionDetailsDirFmt', 'FastqGzFormat', 'FirstDifferencesDirectoryFormat', 'FirstDifferencesFormat', 
'HeaderlessTSVTaxonomyDirectoryFormat', 'HeaderlessTSVTaxonomyFormat', 'ImportanceDirectoryFormat', 
'ImportanceFormat', 'LSMatFormat', 'MultiplexedPairedEndBarcodeInSequenceDirFmt', 
'MultiplexedSingleEndBarcodeInSequenceDirFmt', 'NewickDirectoryFormat', 'NewickFormat', 
'OrdinationDirectoryFormat', 'OrdinationFormat', 'PairedDNASequencesDirectoryFormat', 
'PairedEndFastqManifestPhred33', 'PairedEndFastqManifestPhred33V2', 'PairedEndFastqManifestPhred64', 
'PairedEndFastqManifestPhred64V2', 'PlacementsDirFmt', 'PlacementsFormat', 'PredictionsDirectoryFormat', 
'PredictionsFormat', 'ProbabilitiesDirectoryFormat', 'ProbabilitiesFormat', 'QIIME1DemuxDirFmt', 
'QIIME1DemuxFormat', 'QualityFilterStatsDirFmt', 'QualityFilterStatsFmt', 'SampleEstimatorDirFmt', 
'SeppReferenceDirFmt', 'SingleEndFastqManifestPhred33', 'SingleEndFastqManifestPhred33V2', 
'SingleEndFastqManifestPhred64', 'SingleEndFastqManifestPhred64V2', 'SingleLanePerSamplePairedEndFastqDirFmt', 
'SingleLanePerSampleSingleEndFastqDirFmt', 'TSVTaxonomyDirectoryFormat', 'TSVTaxonomyFormat', 
'TaxonomicClassiferTemporaryPickleDirFmt', 'UchimeStatsDirFmt', 'UchimeStatsFmt']

importableTypes = ['', 'Bowtie2Index', 'DeblurStats', 'DistanceMatrix', 'EMPPairedEndSequences', 
'EMPSingleEndSequences', 'ErrorCorrectionDetails', 'FeatureData[AlignedSequence]', 'FeatureData[Differential]', 
'FeatureData[Importance]', 'FeatureData[PairedEndSequence]', 'FeatureData[Sequence]', 'FeatureData[Taxonomy]', 
'FeatureTable[Balance]', 'FeatureTable[Composition]', 'FeatureTable[Frequency]', 'FeatureTable[PercentileNormalized]', 
'FeatureTable[PresenceAbsence]', 'FeatureTable[RelativeFrequency]', 'Hierarchy', 'MultiplexedPairedEndBarcodeInSequence', 
'MultiplexedSingleEndBarcodeInSequence', 'PCoAResults', 'Phylogeny[Rooted]', 'Phylogeny[Unrooted]', 'Placements', 
'QualityFilterStats', 'RawSequences', 'SampleData[AlphaDiversity]', 'SampleData[BooleanSeries]', 
'SampleData[ClassifierPredictions]', 'SampleData[DADA2Stats]', 'SampleData[FirstDifferences]', 
'SampleData[JoinedSequencesWithQuality]', 'SampleData[PairedEndSequencesWithQuality]', 'SampleData[Probabilities]', 
'SampleData[RegressorPredictions]', 'SampleData[SequencesWithQuality]', 'SampleData[Sequences]', 
'SampleEstimator[Classifier]', 'SampleEstimator[Regressor]', 'SeppReferenceDatabase', 'TaxonomicClassifier', 'UchimeStats']

metrics = ('','shannon', 'goods_coverage', 'brillouin_d', 'heip_e',
    'berger_parker_d', 'enspie', 'robbins', 'observed_otus',
    'michaelis_menten_fit', 'doubles', 'chao1', 'faith_pd', 'mcintosh_e',
    'ace', 'menhinick', 'lladser_pe', 'fisher_alpha', 'margalef',
    'mcintosh_d', 'pielou_e', 'dominance', 'simpson_e', 'singles',
    'gini_index', 'simpson')

TrueFalse = (True,False)
FalseTrue = (False,True)