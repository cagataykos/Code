DEL = "SVTYPE=DEL"
INS = "SVTYPE=INS"
DUP = "SVTYPE=DUP"
BND = "SVTYPE=BND"
INV = "SVTYPE=INV"

SV_TYPES = [
    "deletion",
    "insertion",
    "duplication",
    "bnd",
    "inversion",
    "total",
]

def read_vcf(infile):
    import gzip
    open_func = gzip.open if infile.endswith(".gz") else open
    with open_func(infile) as fh:
        for line in fh:
            if infile.endswith(".gz"):
                yield line.decode("utf-8")
            else:
                yield line

print(*SV_TYPES, sep="\t")
def get_sv_types(infile):
    sv_type_total = {
        "deletion": 0,
        "insertion": 0,
        "duplication": 0,
        "bnd": 0,
        "inversion": 0,
        "total": 0,

    }
    lines = read_vcf(infile)
    for line in lines:
        if line.startswith('#'):
            continue
        if "SVTYPE" not in line:
            continue
        ls = line.split('\t')
        info = ls[7]
        sv_type_total["total"] += 1
        if DEL in info:
            sv_type_total["deletion"] += 1
        elif INS in info:
            sv_type_total["insertion"] += 1
        elif DUP in info:
            sv_type_total["duplication"] += 1
        elif BND in info:
            sv_type_total["bnd"] += 1
        elif INV in info:
            sv_type_total["inversion"] += 1
        else:
            raise Exception(line)
    print(*[sv_type_total[key] for key in SV_TYPES], sep="\t")


#TP
get_sv_types('/home/cagatay/Masaüstü/SV/sniffles_tandem_repeats/tp-call.vcf')
#FP
get_sv_types('/home/cagatay/Masaüstü/SV/sniffles_tandem_repeats/fp-call.vcf')
#FN
get_sv_types('/home/cagatay/Masaüstü/SV/sniffles_tandem_repeats/fn-base.vcf')

