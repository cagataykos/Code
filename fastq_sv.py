import argparse

from sv_generator import fasta_to_fastq

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-i", "--input_fasta", action="store", dest='infasta',  required=True,
                        help="Path of fasta") 
    parser.add_argument("-t", "--mutation_type",  action="store", dest='type', required=True,
                        help="Types of mutation Deletion, Duplication, Inversion")
    parser.add_argument("-s", "--start_position",  action="store", dest='start', required=True,
                        help="Start position of sv")
    parser.add_argument("-e", "--end_position",  action="store", dest='end', required=True,
                        help="End position of sv")                    
    parser.add_argument("-o", "--output_fastq", action="store", dest='outfastq', required=True,
                        help="Path of fastq")
    parsed_args = parser.parse_args()