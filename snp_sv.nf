#!/usr/bin/env nextflow

//Add file
params.outdir = "results"
params.fastq_file_path = "/*.fastq.gz"
params.genome = ""
params.sequencing_summary=""
params.tandem_repeats_bed = ""


//Add paramaters of tools

params.ont_r10_q20 = ""
params.ont_alignment = ""

// Files

summary_file = file(params.sequencing_summary)
genome_file = file(params.genome)


process pycoqc {
    container 'tleonardi/pycoqc:2.5.2'
    publishDir "${params.outdir}/pycoqc", mode: 'copy'
    input:
    file summary_file
    output:
    tuple file("*.html"), file("*.json")
    script:
    """
    pycoQC -f ${summary} -o pycoqc.html -j pycoqc.json
    """

}

process fastq_cat {

    input:
    path fastq_file_path
    output:
    file "merged.fastq.gz" into merged_fastq
    script:
    """
    cat ${fastq_file_path} > merged.fastq.gz"
    """

}
process minimap2 {
    container 'nanozoo/minimap2:2.24--82ff7f3'
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
    container 'zavolab/samtools:1.10'
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
    input:
    tuple file(bam), file(bai) from sorted_bam_ch
    file genome
    output:
    path
    script:
    """
    mkdir output
    run_pepper_margin_deepvariant call_variant \
    -b $bam \
    -f ${genome} \
    -o output/ \
    -t 8 \
    --ont_r10_q20
    """
}
process sv_call {
    publishDir "${params.outdir}/Structural_V", mode: 'copy', overwrite: true
    memory '30 GB'
    input:
    tuple file(bam), file(bai) from sorted_bam_ch_2
    file genome
    file tandem_repeats_bed
    output:

    script:
    """
    sniffles --input $bam --reference ${genome} --vcf sv.vcf --tandem_repeats_bed ${tandem_repeats_bed} --threads 4
    """
}
