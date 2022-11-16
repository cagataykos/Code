def breakpoints(in_vcf, out_vcf):
    accepted_bases = ["A","T","G","C","N"]
    with open(in_vcf ,'r') as bnd, open(out_vcf, "w") as out:
        output_vcf = list()
        for line in bnd:
            if line.startswith('#'):
                out.write(line)
                continue
            if line.startswith("#C"):
                out.write(line)
                continue
            output_vcf.append(line)
            if "SVTYPE=BND" not in line:
                continue
            v_chr, v_pos, v_id, v_ref, v_alt, v_qual, v_filter, v_info, v_format, v_sample = line.split("\t")
            """
            if ',' in v_alt:
                mate_information1, mate_information2 = v_alt.split(',')
                old_multi_mate_variant1 = v_chr + "\t" + v_pos + "\t" + v_id + "\t" + v_ref + "\t" + mate_information1 + "\t" + v_qual + "\t" + v_filter + "\t" + v_info + "\t" + v_format + "\t" + v_sample
                old_multi_mate_variant2 = v_chr + "\t" + v_pos + "\t" + v_id + "\t" + v_ref + "\t" + mate_information2 + "\t" + v_qual + "\t" + v_filter + "\t" + v_info + "\t" + v_format + "\t" + v_sample
                return breakpoints(in_vcf)
            """
        for bases in accepted_bases:
            # t]p] : t]p]
            if bases + "]" in v_alt[0:2]:
                mate_information = v_alt.split("]")
                mate_chromosome,mate_location = mate_information[1].split(":")
                mate_alt = "N" + "]" + v_chr + ":" + v_pos + "]"
                mate_info = v_info.replace("CHR2=" + mate_chromosome, "CHR2=" + v_chr)
                mate_variant = mate_chromosome + "\t" + mate_location + "\t" + v_id + "\t" + "N" + "\t" + mate_alt + "\t" +  v_qual + "\t" + v_filter + "\t" + v_info + "\t" + v_format + "\t" + v_sample
                #print(f"breakpoint variant is \n {line}")
                #print(f"mate variant is \n {mate_variant}")
                output_vcf.append(mate_variant)


                #"[p[t" : "[p[t"
            elif "[" + bases in v_alt[-2:]:
                mate_information =  v_alt.split("[")
                mate_chromosome,mate_location = mate_information[1].split(":")
                mate_alt = "[" + v_chr + ":" + v_pos + "[" + "N"
                mate_info = v_info.replace("CHR2="+mate_chromosome, "CHR2="+v_chr)
                mate_variant = mate_chromosome + "\t" + mate_location + "\t" + v_id + "\t" + "N" + "\t" + mate_alt + "\t" +  v_qual + "\t" + v_filter + "\t" + mate_info + "\t" + v_format + "\t" + v_sample
                #print(f"breakpoint variant is \n {line} ")
                #print(f"mate variant is \n {mate_variant}")
                output_vcf.append(mate_variant)

                #t[p[" : "]p]t",
            elif bases + "[" in v_alt[0:2]:
                mate_information =  v_alt.split("[")
                mate_chromosome, mate_location = mate_information[1].split(":")
                mate_alt = "]" + v_chr + ":" + v_pos + "]" + "N"
                mate_info = v_info.replace("CHR2=" + mate_chromosome, "CHR2=" + v_chr)
                mate_variant = mate_chromosome + "\t" + mate_location + "\t" + v_id + "\t" + "N" + "\t" + mate_alt + "\t" + v_qual + "\t" + v_filter + "\t" + mate_info + "\t" + v_format + "\t" + v_sample
                #print(f"breakpoint variant is \n {line}")
                #print(f"mate variant is \n {mate_variant}")
                output_vcf.append(mate_variant)

                #"]p]t" : "t[p["
            elif "]" + bases  in v_alt[-2:]:
                #print(f"breakpoint variant is \n {line}")
                mate_information = v_alt.split("]")
                #print(mate_information)
                mate_chromosome, mate_location = mate_information[1].split(":")
                mate_alt = "N" + "[" + v_chr + ":" + v_pos + "["
                mate_info = v_info.replace("CHR2=" + mate_chromosome, "CHR2=" + v_chr)
                mate_variant = mate_chromosome + "\t" + mate_location + "\t" + v_id + "\t" + "N" + "\t" + mate_alt + "\t" + v_qual + "\t" + v_filter + "\t" + mate_info + "\t" + v_format + "\t" + v_sample
                #print(f"mate variant is \n {mate_variant}")
                output_vcf.append(mate_variant)
            else:
                continue

        output_vcf.sort()
        for variants in output_vcf:
            #print(output_vcf)
            out.write(variants)


breakpoints("/home/cagatay/PycharmProjects/sniffles_reformat/sniffles_bnd_reformat.vcf","/home/cagatay/PycharmProjects/sniffles_reformat/reformatted.vcf")
