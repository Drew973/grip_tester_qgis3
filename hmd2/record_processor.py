#object that stores template line and handles converting between strings and dicts. 


class record_processor:
    def __init__(self,template_line):
        self.atts=line_to_list(template_line)
        self.origonal_line=template_line
        self.template_line=template_line+'\n'
        for a in self.atts:
            self.template_line=self.template_line.replace(a,'{'+a+'}')        
    #template_line like 'SECTION\\{NETWORK},{LABEL},{SNODE},{LENGTH},{SDATE},{EDATE},{STIME},{ETIME};\n'
        
    
    #read hmd line to dict using template/atts    
    def read_hmd_line(self,line):
        return read_line(line,self.atts)
        
    
    #return {att:char}
    def atts_to_dict(self,char):
        return {att:char for att in self.atts}
    
    
    #return hmd row with all values set to char
    def blanks(self,char=''):
        vals={}
        for a in self.atts:
            vals.update({a:char})
        return self.template_line.format(**vals)  
    
    #dict to hmd row
    #each thing in template_line needs to be in vals.
    #things in vals but not template_line not a problem
    
    def write_line(self,vals):
        try:
            return self.template_line.format(**vals)
        except Exception as e:
            raise ValueError(str(self)+'failed to write line with values:'+str(vals)+' with error:'+str(e))
    
    
    def set_csv_cols(self,cols,constants):
        self.cols=cols
        self.constants=constants
        for a in self.atts:
            if not (a in cols or a in constants):
                raise KeyError('attribute '+a+' not in cols or constants')
            if a in cols and a in constants:
                raise KeyError('attribute '+a+' in both cols and constants')


    def set_query_cols(self,cols,constants):  #cols like {hmdatt:colname}
        for a in self.atts:
            if not (a in cols or a in constants):
                raise KeyError('attribute '+a+' not in cols or constants')
            if a in cols and a in constants:
                raise KeyError('attribute '+a+' in both cols and constants')
        self.qcols=cols
        self.qconstants=constants

#DictRow or row
    def read_query_row(self,row,sep=','):               
        d={c:row[self.qcols[c]] for c in self.qcols}
        d.update({c:self.qconstants[c] for c in self.qconstants})      
        return d
 
    #cols like {hmdatt:colname}
    def set_upload_cols(self,cols):
        c=[]
        v=[]
        for k in cols:
            if not k in self.atts:
                raise KeyError(k+' is not in template_line:'+self.origonal_line)     
            else:
                c.append(cols[k])
                v.append('%('+k+')s')
        self.upload_cols=cols
        self.upload_query='insert into {t} ({tcols}) values({vals})'.format(
                t='{table}',tcols=','.join(c),vals=','.join(v))
        return self.upload_query
        
    #insert into {table} (nwk,lab) values({},{})
    
    
    #d like {hmdatt:value}
    def upload_line(self,d,cur,table):
        cur.execute(self.upload_query.format(table=table),d)
        

#{att:index} index of list like or key of dict like
    def set_read_cols(self,inds,constants):
        have=[k for k in inds]+[k for k in constants]
        
        
        if sorted(have)!=sorted(self.atts):
            raise KeyError(' keys %s != attributes:%s'%(sorted(have),sorted(self.atts)))
        else:
            self.r_inds=inds
            self.r_constants=constants
        
        
    # list or dict to dict. 
    #used to read row of csv(list) and query (list or dict)
    def read_row(self,row):
        d={k:self.r_constants[k] for k in self.r_constants}# copy of r_constants
        d.update({k:row[self.r_inds[k]] for k in self.r_inds})        
        return d
        
        
    
    def __str__(self):
        return 'record_processor:'+self.template_line
    
    
#inputs str,removes whitespace and last charactor ';', splits at ',' to output list
def line_to_list(line):
    return line.strip()[0:-1].split('\\')[-1].split(',')#lose last character,\ and anything before


#reads string line using list tp and outputs dict d
def read_line(line,tp):
    vals=line_to_list(line)
    d={}
    for i,a in enumerate(tp):
        d.update({a:vals[i]})
    return d


#p=record_processor(r'SECTION\NETWORK,LABEL,SNODE;')

#p.set_read_cols({'LABEL':0,'SNODE':1},{'NETWORK':'UKPMS'})
#print(p.read_row(['lab','sn','extra']))
