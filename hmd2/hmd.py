from .record_processor import record_processor
from .section import section
from .threshold import threshold
from .observ import observ
from .obval import obval

import psycopg2
from psycopg2.extras import DictCursor


class hmd:
    def __init__(self,
                 survey_template=r'SURVEY\OWNER,TYPE,VERSION,NUMBER,SUBSECT,MACHINE,PREPROC,SVC,XSPUSED;',
                 section_template=r'SECTION\NETWORK,LABEL,SNODE,LENGTH,SDATE,EDATE,STIME,ETIME;',
                 threshold_template=r'THRESHLD\FTXSECT,FTSCHAIN,FTECHAIN,FTSDATE,FTNUM,PIFIND,SCODE;',
                 observ_template=r'OBSERV\DEFECT,VERSION,XSECT,SCHAIN,ECHAIN;',
                 obval_template=r'OBVAL\PARM,OPTION,VALUE,PERCENT;',
                 hmstart='HMSTART ukPMS 008 " " ; , \\',
                 ):
        
        self.set_templates(survey_template,section_template,threshold_template,observ_template,obval_template)
        self.hmstart=hmstart
        self.sects={}        
        self.survey=None
        
                
    def set_templates(self,survey_template,section_template,threshold_template,observ_template,obval_template):
        self.survey_processor=record_processor(survey_template)
        self.section_processor=record_processor(section_template)
        self.threshold_processor=record_processor(threshold_template)
        self.observ_processor=record_processor(observ_template)
        self.obval_processor=record_processor(obval_template)         


    def set_threshold_template(self,template):
        self.threshold_processor=record_processor(template)


    def set_survey_line(self,survey_line):
        self.survey=self.survey_processor.read_hmd_line(survey_line)
     
        
    def start_lines(self,survey=True,section=True,thresholds=True,observs=True,obvals=True):
        self.start_count=2#includes TSTART,TEND
        
        start_lines=self.hmstart+'\n'+'TSTART;\n'
        
        if survey:
             start_lines+=self.survey_processor.origonal_line+'\n'
             self.start_count+=1
             
        if section:
            start_lines+=self.section_processor.origonal_line+'\n'
            self.start_count+=1
            
        if thresholds:
            start_lines+=self.threshold_processor.origonal_line+'\n'
            self.start_count+=1
            
        if observs:
            start_lines+=self.observ_processor.origonal_line+'\n'
            self.start_count+=1
            
        if obvals:
            start_lines+=self.obval_processor.origonal_line+'\n'
            self.start_count+=1
        
        start_lines+='TEND\\'+str(self.start_count)+';\n'
        
        return start_lines
        
    
    #templates will set templates to those in file, 
    #otherwise uses current templates. file needs all attributes in current templates for this.
    def read_hmd(self,file,thresholds=True,observs=True,obvals=True,templates=True,hmstart=True,survey=True):
        started=False
        c=0
        lab=''
        with open(file,'r') as f:
            for line in f.readlines():
                t=line.strip().split('\\')[0]
                r=line.strip()
                if not started:
                    if c==0 and hmstart:
                        self.hmstart=line.strip()
                    if templates:
                        if t=='SURVEY':
                            self.survey_processor=record_processor(r)
                        if t=='SECTION':
                            self.section_processor=record_processor(r)
                        if t=='THRESHLD':
                            self.threshold_processor=record_processor(r)
                        if t=='OBSERV':
                            self.observ_processor=record_processor(r)
                        if t=='OBVAL':
                            self.obval_processor=record_processor(r)
                        if line=='DSTART;\n':
                            started=True                
                        
                else:
                    if t=='SURVEY' and survey:
                        self.survey=self.survey_processor.read_hmd_line(r)
                    
                    #add section to sects
                    if t=='SECTION':
                        d=self.section_processor.read_hmd_line(line)
                        lab=d['LABEL']+d['SNODE']
                        if not lab in self.sects:
                            self.add_section(lab,section(d,self.section_processor))
                    #add line            
                    if lab!='':
                        if t=='THRESHLD' and thresholds:
                            self.add_threshold(lab,threshold(self.threshold_processor.read_hmd_line(line),self.threshold_processor))
                       
                        if t=='OBSERV' and observs:
                           self.add_observ(lab,observ(self.observ_processor.read_hmd_line(line),self.observ_processor))
                           
                        if t=='OBVAL' and obvals:
                            self.add_obval(lab,obval(self.obval_processor.read_hmd_line(line),self.obval_processor))   
                                        
                c+=1


    def read_csv(self,file,sep=',',header=False,srow=0,thresholds=False,observs=False,obvals=False,drop_spaces=False):
        if header and srow==0:
            srow=1
        r=0
        with open(file,'r') as f:
            for line in f.readlines():
                if r>=srow:
                    
                    row=line.strip().split(',')
                    
                    sec=self.section_processor.read_row(row) 
                    
                    if drop_spaces:
                        lab=sec['LABEL'].replace(' ','')+sec['SNODE']
                    else:
                        lab=sec['LABEL']+'***'+sec['SNODE']
                        
                    if not lab in self.sects:
                        self.add_section(lab,section(sec,self.section_processor))
                        
                    if thresholds:
                        self.add_threshold(lab,threshold(self.threshold_processor.read_row(row),self.threshold_processor))
                        
                    if observs:
                        self.add_observ(lab,observ(self.observ_processor.read_row(row),self.observ_processor))
                 
                    if obvals:
                       self.add_observ(lab,obval(self.obval_processor.read_row(row),self.obval_processor))
                  
                r+=1
                    
    def to_hmd(self,to,desc=False):
        if to:
            with open(to,'w') as f:
                f.write(self.start_lines())
                f.write('DSTART;\n')
                if self.survey:
                    f.write(self.survey_processor.write_line(self.survey))
                
                else:
                    f.write(self.survey_processor.blanks())
                    
                for s in sorted(self.sects.keys()):#ordered alphabetically
                    f.write(self.sects[s].output())
                f.write('DEND\\%d;'%(self.dcount()+2)+'\n')#self.dcount does not include DSTART and DEND
                f.write('HMEND\\%d;'%(self.dcount()+2+self.start_count+1+1))#start count does not include HMstart. includes HMEND line

         
    def add_section(self,k,sec):
        self.sects.update({k:sec})
    
    def drop_section(self,k):
        self.sects.pop(k)#remove and count data lines
    
    def add_observ(self,k,obs):
        self.sects[k].add_observ(obs)
    
    def add_obval(self,k,obv):
        self.sects[k].add_obval(obv)
        
        
    def add_threshold(self,k,t):
        self.sects[k].add_threshold(t)


    def dcount(self):
        return 1+sum([s.count() for s in self.sects.values()])#includes survey line                    
        
    
    #returns sections matching condition cond.
    #cond=string to evaluate.
    #use sec to acess section object
    #list comprehention might be more efficient?
    def get_sections(self,cond):
        s=[]
        for sec in self.sects.values():
            if eval(cond):
                s.append(sec)    
        return s
    
    
    #drops any sections not matching condition.
    # cond=string to evaluate
    #use sec to acess section object
    def filter_sections(self,cond):
        to_drop=[]
        for lab in self.sects:
            sec= self.sects[lab]
            if not eval(cond):
                to_drop.append(lab)
        for lab in to_drop:
            self.drop_section(lab)
            
    
    def read_query(self,host,db_name,query,user,password='',port='5432',thresholds=True,observs=True,obvals=True):
        con=psycopg2.connect(host=host,dbname=db_name,user=user,password=password,port=port)
        c=con.cursor(cursor_factory=DictCursor)
        c.execute(query)
        
        #colnames = [desc[0] for desc in c.description]
       # self.section_processor.check_query_cols(colnames)
        
        for row in c.fetchall():
            r=dict(row)
            
            d=self.section_processor.read_query_row(r)
            #lab=str(r['LABEL'])+str(r['SNODE'])
            lab=str(d['LABEL'])+str(d['SNODE'])

            if not lab in self.sects:
                self.add_section(lab,section(d,self.section_processor))            
                                
            if thresholds:
                self.add_threshold(lab,threshold(self.threshold_processor.read_query_row(r),self.threshold_processor))
                            
            if observs:
                self.add_observ(lab,observ(self.observ_processor.read_query_row(r),self.observ_processor))
                     
            if obvals:
                self.add_observ(lab,obval(self.obval_processor.read_query_row(r),self.obval_processor))
   
        con.close()


    def invalid_sections(self):
        return [s.vals['LABEL'] for s in self.sects.values() if s.invalid_lengths()]
        

    def apply(self,funct):
        for s in self.sects.values():
            funct(s)
    
    def apply_method(self,method):
         for s in self.sects.values():
             s.method()


    def group_thresholds(self):
         for s in self.sects.values():
             s.group_thresholds()
        

    def snode_to(self,to):       
        for sec in self.sects.values():
            sec.vals['SNODE']=to
        self.redo_keys()
     
        
    def redo_keys(self):
        self.sects={sec.vals['LABEL']+'***'+sec.vals['SNODE']:sec for sec in self.sects.values()}
    
    
    def list_section_labels(self):
        return [sec.vals['LABEL'] for sec in self.sects.values()] 
  
    
#a=hmd()
#a.read_hmd(r'C:\Users\drew.bennett\Documents\hmd_jobs\add_thresholds\Wokingham\SC19HMDF.DIF')
#with open('test.hmd','w') as f:
#    a.to_hmd(f)
def upper_dict(d):
   new_dict = dict((k.upper(), v) for k, v in d.items())
   return new_dict
