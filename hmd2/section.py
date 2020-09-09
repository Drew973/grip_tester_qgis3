#import threshold
#import observ
#import obval
from .hmd_record import hmd_record


def get_att(rec,att):
    return rec.vals[att]


class section(hmd_record):
    def __init__(self,vals,processor):
        self.hmd_record_init(vals,processor,['threshold','observ'])

   # section:{...,'thresholds':[...],'observs':[{...,'obvals':[{...}]}}
 
    def add_observ(self,obs):
        self.add_subrecord(obs,'observ')

    def add_obval(self,obv):
        self.subrecs['observ'][-1].add_subrecord(obv,'obval')


    def add_threshold(self,thr):
        self.add_subrecord(thr,'threshold')
        
   
    ###########################################################################
    def swap_rev_chainages(self):
        for i in self.subrecs['observ']:
            i.maybe_swap_ch()        
        for t in self.subrecs['threshold']:
            t.maybe_swap_ch()
            
    

    def sort_observs(self,by=['XSECT','SCHAIN','ECHAIN'],reverse=False):
       #self.subrecs['observ'].sort(key=lambda x: to_best_type(x.vals[by]),reverse=reverse)
       self.subrecs['observ'].sort(key=sortkeypicker(by),reverse=reverse)
    
    
    def sort_thresholds(self,by=['FTXSECT','FTSCHAIN','FTECHAIN'],reverse=False):
       #self.subrecs['observ'].sort(key=lambda x: to_best_type(x.vals[by]),reverse=reverse)
       self.subrecs['threshold'].sort(key=sortkeypicker(by),reverse=reverse)


    
    #group ajacent thresholds with same FTNUM
    def group_thresholds(self):
        self.sort_thresholds()
        nt=[]
        for t in self.subrecs['threshold']:
            if nt==[]:
                nt.append(t)
            
            else:
                if t.vals['FTNUM']==nt[-1].vals['FTNUM']:#different FTNUM
                    nt[-1].vals['FTECHAIN']=t.vals['FTECHAIN']
                    
                else:
                    nt.append(t)
               
        self.subrecs['threshold']=nt
    
    
    #unfinished
    def has_threshold_gaps(self):
        last=0
        
        for c in sorted([float(t.vals['FTSCHAIN']) for t in self.subrecs['threshold']]):
            if c>last:
                return True
            last=c
    
        return False
                
            
    def has_overlapping_thresholds(self):
        ranges=[]
        
        for t in self.subrecs['threshold']:
            r=rg(t.vals['FTSCHAIN'],t.vals['FTECHAIN'])
            for r2 in ranges:
                if r.collides(r2):
                    return True
            ranges.append(r)
            
        return False
        
        
    
    #returns true if any length>section length
    def invalid_lengths(self):
        L=self.vals['LENGTH']
        
        for t in self.subrecs['threshold']:
            if t.vals['FTSCHAIN']>L or t.vals['FTECHAIN']>L:
                return True
            
        for t in self.subrecs['observ']:
            if t.vals['SCHAIN']>L or t.vals['ECHAIN']>L:
                return True            
        
        return False    
    
    
    
    def drop_invalid_thresholds(self):
        L=self.vals['LENGTH']
        for t in self.subrecs['threshold']:
            if t.vals['FTSCHAIN']>L or t.vals['FTECHAIN']>L:
                self.subrecs['threshold'].remove(t)
        
    
    def xsp_vals(self):
        vals=[]
        for row in self.subrecs['observ']:
            if not row.vals['XSECT'] in vals:
                vals.append(row.vals['XSECT'])
        return vals
    
    #invert direction
    
    def invert(self):
        #self.snode=swap_between(self.snode,'F','R')
        self.vals['SNODE']=swap_between(self.vals['SNODE'],'F','R')
                        
        for ob in self.subrecs['observ']:
            #ob.invert(self.length)
            ob.invert(self.vals['LENGTH'])
            
        for t in self.subrecs['threshold']:
            t.invert(self.vals['LENGTH'])

    
    def reversed_from_nodes(self,start_node,end_node,raise_error=True): 
        #snode=self.snode.lstrip('0')#remove any leading zeros
        snode=self.vals['SNODE'].lstrip('0')#remove any leading zeros
        
        if snode==str(start_node):
            self.reversed=False
            return False
        
        if snode==str(end_node):
            self.reversed=True
            return True
        
        if raise_error:
            raise KeyError('snode %s not start_node %s or end_node %ds of section %s'%(snode,start_node,end_node,self.label))

    def add_to_ch(self,val):
        for ob in self.observs:
            ob.add_to_ch(val)
           
   
    def add_other(self,other):
        self.thresholds+=other.thresholds
        self.observs+=other.observs
         
#needed for sorting
    def __lt__(self,other):
        return self.label<other.label
    
    
    def __eq__(self,other):
        return self.label==other.label and (self.reversed==other.reversed or self.snode==other.snode)
     

    def drop_zeros(self):
        self.subrecs['observ']=[obs for obs in self.subrecs['observ'] if not obs.all_zeros()]



def line_to_section(line,processor):
    return section(processor.read_line(line),processor)

def swap_between(val,a,b):
    if val==a:
        return b
    if val==b:
        return a
    
    
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
        
    
def sortkeypicker(keynames):
    negate = set()
    for i, k in enumerate(keynames):
        if k[:1] == '-':
            keynames[i] = k[1:]
            negate.add(k[1:])
    def getit(adict):
       composite = [to_best_type(adict.vals[k]) for k in keynames]
       for i, (k, v) in enumerate(zip(keynames, composite)):
           if k in negate:
               composite[i] = -v
       return composite
    return getit



class rg:
    def __init__(self,low,high):
        self.low=low
        self.high=high
        
    def collides(self,other):
        if self.low<other.low and other.low<self.high:
            return True
        if self.low<other.high and other.low<self.high:
            return True

        return False



#a = sorted(b, key=sortkeypicker(['-Total_Points', 'TOT_PTS_Misc']))    
