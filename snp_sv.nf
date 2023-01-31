#!/usr/bin/env nextflow

// Files
params.sequencing  = "/pass"
params.genome = "/home"
params.seq_summary = "/seq_summary"
params.outdir = "results"


genome = file(params.genome)
summary = file(params.seq_summary)


process pycoqc {
    container 'test/qc:2.5.2'
    memory '30 GB'
    publishDir "${params.outdir}/pycoqc", mode: 'copy', overwrite: true

    input:
    file summary

    output:
    tuple file('pycoqc.html'), file('pycoqc.json') into pycoqc_ch

    script:
    """
    qc -f ${summary} -o pycoqc.html -j pycoqc.json
    """
}
process merge_fastq {
    memory '30 GB'
    input:
    path reads from params.sequencing
    output:
    file("merged_fastq_GM24385_Q20.fastq.gz") into merged_fastq_ch
    script:
    """
    cat ${reads}/*.gz > merged_fastq_GM24385_Q20.fastq.gz
    """
}
process minimap2 {
    container 'test/minimap2:2.24--82ff7f3'
    memory '30 GB'

    input:
    file merged from merged_fastq_ch
    file genome

    output:
    file 'unsorted.bam' into bam_ch
    script:
    """
    minimap2 -y -ax map-ont ${genome} ${merged} | samtools view -hb -F 0x904  > unsorted.bam
    """
}
process sort_bam {
    container 'test/samtools:1.10'
    memory '30 GB'
    input:
    file bam from bam_ch
    output:
    tuple file('sorted.bam'), file('sorted.bam.bai') into sorted_bam_ch, sorted_bam_ch2
    script:
    """
    samtools sort -@32 $bam  -o sorted.bam
    samtools index  sorted.bam
    """
}
process pepper {
    container "test/snp:0.8"
    input:
    tuple file(bam), file(bai) from sorted_bam_ch
    file genome
    output:
    file "vcf.gz*" into annotation_channel
    script:
    """
    mkdir output
    run_pepper_margin_deepvariant call_variant \
    -b $bam \
    -f $genome \
    -o output/ \
    -t 8 \
    --ont_r10_q20
    """


}
process sv_call {
    publishDir "${params.outdir}/Structural_V", mode: 'copy', overwrite: true
    container "cbkos/sv:2.2"
    memory '30 GB'
    input:
    tuple file(bam), file(bai) from sorted_bam_ch_2
    file genome
    file tandem_repeats_bed
    output:
    file "vcf.gz*" into sv_annotation_channel
    script:
    """
    sv tool command
    """
}
