class hmd_record:
    def __init__(self,vals,processor,subrecords=[]):
        self.hmd_record_init(vals,processor,subrecords)
        
        
    #subrecords=[str]. Names for subrecords
    def hmd_record_init(self,vals,processor,subrecords=[]):
        self.vals=vals
        self.processor=processor
        self.subrecords=subrecords
        
        self.subrecs={}

        for r in subrecords:
            self.subrecs.update({r:[]})
        
        
    def read_line(self,line):
        self.vals=self.processor.read_line(line)
        
        
    def output_line(self):
        return self.processor.write_line(self.vals)

        
    #output record and subrecords
    def output(self):
        s=self.processor.write_line(self.vals)
        for k in self.subrecords:
            for r in self.subrecs[k]:
                s+=r.output()
        return s
    
    
#returns iterator through leafs    
    def leafs(self):
        return leaf_iterator(self)
                
            
    
    #dcount for record and subrecords
    def count(self):
        count=1        
        for k in self.subrecords:
            for r in self.subrecs[k]:
                count+=r.count()
        return count
        
    #hmd_record,type
    def add_subrecord(self,r,t):
        #self.vals[t].append(r)
        self.subrecs[t].append(r)
        
        
    
    def __str__(self):
        return self.output()


    def get_att(self,att):
        return self.vals[att]


    def __eq__(self,other):
        if self.processor==other.processor and self.vals==other.vals:
            return True
        else:
            return False 
          
    
    
def to_best_type(v):
    try:
        return int(v)
    except:
        try:
            return float(v)
        except:
            return str(v)    
        
def dict_to_best_type(d):
    return {key:to_best_type(value) for (key,value) in d.items()}
                
        
        
#convert all keys to upper case

#template=r'SECTION\NETWORK,LABEL,SNODE,LENGTH,SDATE,EDATE,STIME,ETIME;'
#line=r'SECTION\UKPMS,A3032/05,F,293,29052019,29052019,,;'

#line='nwk,lab,snode,len'
#a=record_processor(template)
#a.set_csv_cols({'NETWORK':0, 'LABEL':1, 'SNODE':2, 'LENGTHe':3},{'SDATE':1,'EDATE':2,'STIME':3,'ETIME':None})
#d=a.read_csv_row(line)
#print(a.set_upload_cols({'NETWORK':'nwk','LABEL':'lab'}))

#print(a.upload_line({'NETWORK':'n','LABEL':'lab'},0,0))
#print(a.write_line(d))

#a=record_processor(r'SURVEY\OWNER,TYPE,VERSION,NUMBER,SUBSECT,MACHINE,PREPROC,SVC,XSPUSED;')
#print(a.blanks())




