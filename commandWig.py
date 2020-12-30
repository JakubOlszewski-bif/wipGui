from importable import importableFormats,importableTypes,metrics

"""
commandWig is a python library of instructions to build widgets for commands used in qiime2. It's used by winBuilder.py to create windows for each command.

combobox : ["combo",<label>,<list of elements (first is default)>]
fileChose : ["fChoose", <label>]
fileName : ["fName",<label>]
dirName : ["fDir",<label>]
ifSpin : ["ifSpin", <label>,True (int) OR False (float),<default value>]
importChoose : ["importChoose",<label>]
"""

commandWig = {
    "tools" : {
        "tools import" : (["combo","--type",importableTypes],["importChoose",'--input-path'],["fName","--output-path"],"optional",["combo","--input-format",importableFormats])
        },
    "dada" : {
        "dada2 denoise-paired" : (["fDir","--output-directory"],["fChoose", "--i-demultiplexed-seqs"],["ifSpin","--p-trunc-len-f",True,0],["ifSpin","--p-trunc-len-r",True,0],["fName","--o-table"],["fName","--o-representative-sequences"],["fName","--o-denoising-stats"],
        "optional",["ifSpin","--p-trim-left-f",True,0],["ifSpin","--p-trim-left-r",True,0],["ifSpin","--p-max-ee-f",False,2.0],["ifSpin","--p-max-ee-r",False,2.0],["ifSpin","--p-trunc-q",True,2],["combo","--p-pooling-method",('independent','pseudo')],["combo","--p-chimera-method",('consensus','none', 'pooled')],["ifSpin","--p-min-fold-parent-over-abundance",False,1.0],["ifSpin","--p-n-threads",True,1],["ifSpin","--p-n-reads-learn",True,1000000])
        },
    "phylogeny" : {
        "phylogeny align-to-tree-mafft-fasttree" : (["fChoose","--i-sequences"],["fName","--o-alignment"],["fName","--o-masked-alignment"],["fName","--o-tree"],["fName","--o-rooted-tree"],
        "optional",["ifSpin","--p-n-threads",True,1],["ifSpin","--p-mask-max-gap-frequency",False,1.0],["ifSpin","--p-mask-min-conservation",False,0.4],["combo","--p-parttree",('False','True')])
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
    }
}
