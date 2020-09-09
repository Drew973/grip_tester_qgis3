from collections import OrderedDict

#inputs
#(str line,list tp)
#outputs OrderedDict
def read_line(line,tp):
    vals=line_to_list(line)
    d=OrderedDict()
    for i,a in enumerate(tp):
        d.update({a:vals[i]})
    return d


#inputs str
#outputs list
def line_to_list(line):
    return line.strip()[0:-1].split('\\')[-1].split(',')#lose last character,\ and anything before


    

class record_processor:
    def __init__(self,template_line):
        self.atts=line_to_list(template_line)
        self.template_line=template_line+'\n'
        for a in self.atts:
            self.template_line=self.template_line.replace(a,'{'+a+'}')
            
    #template_line like 'SECTION\\{NETWORK},{LABEL},{SNODE},{LENGTH},{SDATE},{EDATE},{STIME},{ETIME};\n'
        
    def read_line(self,line):
        return read_line(line,self.atts)
        
    #each thing in template_line needs to be in vals.
    #things in vals not in template_line not a problem
    def write_line(self,vals):
        return self.template_line.format(**vals)
        
    
    

    
    
    
    
template=r'SECTION\NETWORK,LABEL,SNODE,LENGTH,SDATE,EDATE,STIME,ETIME;'
line=r'SECTION\UKPMS,A3032/05,R,293,29052019,29052019,,;'

#print(read_line(line,line_to_list(template)))

r=record_processor(template)
d=r.read_line(line)
d.update({'extra':1})
#d.update({'extra':1})
print(r.write_line(d))
#print(r.template_line)



