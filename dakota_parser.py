def get_lcoe():
    with open('dakota.out') as dak:
        daklines = dak.readlines()

    # read data
    vals = {}
    for n, line in enumerate(daklines):
        if n<49 or n > len(daklines)-64: pass
        else: 
           split_line = line.split()
           if len(split_line)==2:
               if split_line[1] not in vals: vals[split_line[1]] = [split_line[0]]
               else:vals[split_line[1]].append(split_line[0])
    return vals['lcoe_se.coe']
# return lcoe
# write data
#values = [value for value in vals]
#out = open('dakota.csv','w')
#print >> out, ', '.join(values)
#
#for i in range(len(vals[values[1]])):
#     print >> out, ', '.join([str(vals[v][i]) for v in values])
#out.close()
