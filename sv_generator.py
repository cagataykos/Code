
"""
Structural Variant Generator 
    1) Give single fasta with one header otherwise the result will not be correct
    2) Specify desired sv  type(Deletion, Duplcation, Inversion) with start and end position
"""



def fasta_to_fastq(infasta, type, start, end, outfastq):
    with open(infasta, "r") as input,  open(outfastq, 'w') as output:
        fullfasta = ''
        genome = input.readlines()
        for head in genome:
            if head.startswith('>'):
                head = head.strip()
                output.write('@%s\n' % head)  
            else:
                pass
        for line in genome:
            if not (line.startswith(">")):
                line = line.strip()
                line  = line.upper()
                fullfasta = fullfasta + line
        if type == 'deletion':
            deletion = fullfasta[:start] + fullfasta[end:]
            output.write('%s\n' % deletion)
            output.write('+\n')
            for q in range(len(deletion)):
                quality = ''
                q = '1'
                quality = quality + q
                output.write(quality)
        if type == 'inversion':
            inversion = fullfasta.replace(fullfasta[start:end],fullfasta[start:end][::-1])
            output.write('%s\n' % inversion)
            output.write('+\n')
            for q in range(len(inversion)):
                quality = ''
                q = '1'
                quality = quality + q
                output.write(quality) 
        if type == 'duplication':
            duplication = fullfasta[:end] + fullfasta[start:end] + fullfasta[end+1:]
            output.write('%s\n' % duplication)
            output.write('+\n')
            for q in range(len(duplication)):
                quality = ''
                q = '1'
                quality = quality + q
                output.write(quality)
 
print('Succesfully mutation generated')


