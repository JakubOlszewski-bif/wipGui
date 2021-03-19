from importable import importableFormats,importableTypes,metrics,TrueFalse,FalseTrue

"""
A python library of instructions to build widgets for commands used in qiime2. It's used by winBuilder.py to create windows for each command.

combo : ["combo",<label>,<list of elements (first is default)>]
fChoose : ["fChoose", <label>] 
fName : ["fName",<label>] #In output scenarios, needs default extension
dirName : ["fDir",<label>]
ifSpin : ["ifSpin", <label>,True (int) OR False (float),<default value>] #Needs range
importChoose : ["importChoose",<label>]
"""

commandWig = {
    "tools" : {
        "tools import" : (["combo","--type",importableTypes],["importChoose",'--input-path'],["fName","--output-path"],"optional",["combo","--input-format",importableFormats])
    },
    "dada" : {
        "dada2 denoise-single" : (["fChoose", "--i-demultiplexed-seqs"],["ifSpin", "--p-trunc-len",True,0],["fName","--o-table"],["fName","--o-representative-sequences"],["fName","--o-denoising-stats"],
        "optional",["ifSpin","--p-trim-left",True,0],["ifSpin","--p-max-ee",False,2.0],["ifSpin","--p-trunc-q",True,2],["combo","--p-pooling-method",('independent','pseudo')],["combo","--p-chimera-method",('consensus','none', 'pooled')],["ifSpin","--p-min-fold-parent-over-abundance",False,1.0],["ifSpin","--p-n-threads",True,1],["ifSpin","--p-n-reads-learn",True,1000000],["combo","--p-hashed-feature-ids",TrueFalse]),
        "dada2 denoise-paired" : (["fDir","--output-directory"],["fChoose", "--i-demultiplexed-seqs"],["ifSpin","--p-trunc-len-f",True,0],["ifSpin","--p-trunc-len-r",True,0],["fName","--o-table"],["fName","--o-representative-sequences"],["fName","--o-denoising-stats"],
        "optional",["ifSpin","--p-trim-left-f",True,0],["ifSpin","--p-trim-left-r",True,0],["ifSpin","--p-max-ee-f",False,2.0],["ifSpin","--p-max-ee-r",False,2.0],["ifSpin","--p-trunc-q",True,2],["combo","--p-pooling-method",('independent','pseudo')],["combo","--p-chimera-method",('consensus','none', 'pooled')],["ifSpin","--p-min-fold-parent-over-abundance",False,1.0],["ifSpin","--p-n-threads",True,1],["ifSpin","--p-n-reads-learn",True,1000000])
    },
    "demux" : {
        "demux emp-paired" : (["fChoose", "--i-seqs"],["fChoose", "--m-barcodes-file"],["fName","--m-barcodes-column"],["fName","--o-per-sample-sequences"],["fName","--o-error-correction-details"],
        "optional",["combo","--p-golay-error-correction",TrueFalse],["combo","--p-rev-comp-barcodes",FalseTrue],["combo","--p-rev-comp-mapping-barcodes",FalseTrue]),
        "demux summarize" : (["fChoose","--i-data"],["ifSpin","--p-n",True,10000],["fName","--o-visualization"])
    },
    "alignment" : {
        "alignment mafft" : (["fChoose","--i-sequences"],["ifSpin","--p-n-threads",True,1],["combo","--p-parttree",FalseTrue],["fName","--o-alignment"]),
        "alignment mask" : (["fChoose","--i-alignment"],["ifSpin","--p-max-gap-frequency",False,1.0],["ifSpin","--p-min-conservation",False,0.4],["fName","--o-masked-alignment"])
    },
    "phylogeny" : {
        "phylogeny fasttree" : (["fChoose","--i-alignment"],["ifSpin","--p-n-threads",True,1],["fName","--o-tree"]),
        "phylogeny align-to-tree-mafft-fasttree" : (["fChoose","--i-sequences"],["fName","--o-alignment"],["fName","--o-masked-alignment"],["fName","--o-tree"],["fName","--o-rooted-tree"],
        "optional",["ifSpin","--p-n-threads",True,1],["ifSpin","--p-mask-max-gap-frequency",False,1.0],["ifSpin","--p-mask-min-conservation",False,0.4],["combo","--p-parttree",('False','True')]),
        "phylogeny midpoint-root" : (["fChoose","--i-tree"],["fName","--o-rooted-tree"])
    },
    "diversity" : {
        "diversity core-metrics-phylogenetic" : (["fChoose","--i-phylogeny"],["fChoose","--i-table"],["ifSpin","--p-sampling-depth",True,1],["fChoose","--m-metadata-file"],["fDir","--output-dir"]),
        "diversity alpha-group-significance" : (["fChoose","--i-alpha-diversity"],["fChoose","--m-metadata-file"],["fName","--o-visualization"]),
        "diversity beta-group-significance" : (["fChoose","--i-distance-matrix"],["fChoose","--m-metadata-file"],["fName","--m-metadata-column"],["fName","--o-visualization"],
        "optional",["combo","--p-method",('permanova', 'anosim', 'permdisp')],["combo","-p-pairwise",("False","True")],["ifSpin","--p-permutations",True,999]),
        "diversity alpha-rarefaction" : (["fChoose","--i-table"],["fChoose","--i-phylogeny"],["ifSpin","--p-max-depth",True,1],["fName","--o-visualization"],
        "optional",["fChoose","--i-phylogeny"],["combo","--p-metrics",metrics],["fChoose","--m-metadata-file"],["ifSpin","--p-min-depth",True,1],["ifSpin","--p-steps",True,10],["ifSpin","--p-iterations",True,10])
    },
    "feature-table" : {
        "feature-table summarize" : (["fChoose","--i-table"],["fName","--o-visualization"],
        "optional",["fChoose","--m-sample-metadata-file"]),
        "feature-table tabulate-seqs" : (["fChoose","--i-data"],["fName","--o-visualization"])
    },
    "metadata" : {
        "metadata tabulate" : (["fChoose","--m-input-file"],["ifSpin","--p-page-size",True,100],["fName","--o-visualization"])
    },
    "feature-classifier" :{
        "feature-classifier classify-sklearn" : (["fChoose","--i-reads"],["fChoose","--i-classifier"],["fName","--o-classification"],
        "optional",["ifSpin","--p-reads-per-batch",True,0],["ifSpin","--p-n-jobs",True,1],["fName","--p-pre-dispatch"],["ifSpin","--p-confidence",False,0.7],["combo","--p-read-orientation",('auto','same','reverse-complement')])
    },
    "taxa" : {
        "taxa barplot" : (["fChoose","--i-table"],["fChoose","--i-taxonomy"],["fChoose","--m-metadata-file"],["fName","--o-visualization"])
    },
    "emperor" : {
        "emperor plot" : (["fChoose","--i-pcoa"],["fChoose","--m-metadata-file"],["fName","--o-visualization"],
        "optional",["fName","--p-custom-axes"],["combo","--p-ignore-missing-samples",FalseTrue])
    }
}
