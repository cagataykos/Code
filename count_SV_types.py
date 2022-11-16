DEL = "SVTYPE=DEL"
INS = "SVTYPE=INS"
DUP = "SVTYPE=DUP"
BND = "SVTYPE=BND"
INV = "SVTYPE=INV"

sv_type_del = {
    "SVTYPE=DEL" :0,

}
sv_type_ins = {
    "SVTYPE=INS" :0,

}
sv_type_dup = {
    "SVTYPE=DUP" :0,

}
sv_type_bnd = {
    "SVTYPE=BND" :0,

}
sv_type_inv = {
    "SVTYPE=INV" :0,

}
sv_type_other = {
    "other": 0,

}
sv_type_total = {
    "SVTYPE=DEL":0,
    "SVTYPE=INS": 0,
    "SVTYPE=DUP": 0,
    "SVTYPE=BND": 0,
    "SVTYPE=INV": 0,
}
sv_total= {
    "TOTAL SV": 0,

}

def svtype(sv):
    with open(sv) as svtype:
        for line in svtype:
            if line.startswith('#'):
                continue
            ls = line.split('\t')
            info= ls[7].split(';')
            sv_variants = info[1]
            if DEL in sv_variants:
                sv_type_total[DEL] += 1
                for total_del in sv_type_del:
                    sv_type_del[total_del] += 1
            elif INS in sv_variants:
                sv_type_total[INS] += 1
                for total_ins in sv_type_ins:
                    sv_type_ins[total_ins] += 1
            elif DUP in sv_variants:
                sv_type_total[DUP] += 1
                for total_dup in sv_type_dup:
                    sv_type_dup[total_dup] +=1
            elif BND in sv_variants:
                sv_type_total[BND] += 1
                for total_bnd in sv_type_bnd:
                    sv_type_bnd[total_bnd] +=1
            elif INV in sv_variants:
                sv_type_total[INV] += 1
                for total_inv in sv_type_inv:
                    sv_type_inv[total_inv] +=1
            else:
                for total_other in sv_type_other:
                    sv_type_other[total_other] += 1
                print(sv_variants)
    print(sv_type_total)
    print(sv_type_other)


svtype('/home/cagatay/Masaüstü/SV/truvari/cutesv_hg002.vcf')
