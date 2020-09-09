#import obval
from .hmd_record import hmd_record

class observ(hmd_record):    
    
    def __init__(self,vals,processor):
        self.hmd_record_init(vals,processor,['obval'])
  

#########
    def invert(self,sec_len):
        self.vals['SCHAIN']=float(sec_len)-float(self.vals['SCHAIN'])
        self.vals['ECHAIN']=float(sec_len)-float(self.vals['ECHAIN'])
        
        if self.vals['XSECT']=='CL1':
            self.vals['XSECT']='CR1'
            
        else:
            if self.vals['XSECT']=='CR1':
                self.vals['XSECT']='CL1'


    def add_obval(self,obv):
        self.obvals.append(obv)

    def maybe_swap_ch(self):
        if float(self.vals['SCHAIN'])>float(self.vals['ECHAIN']):
            old=self.vals['SCHAIN']
            self.vals['SCHAIN']=self.vals['ECHAIN']
            self.vals['ECHAIN']=old

    def __lt__(self,other):
        return self.vals['SCHAIN']<other.vals['SCHAIN']
    
         
    def add_to_ch(self,val):
        self.vals['SCHAIN']+=val
        self.vals['ECHAIN']+=val
        
    #all obvals ['VALUE']==0
    def all_zeros(self):
        for s in self.subrecs['obval']:
            if float(s.vals['VALUE'])!=0:
                return False
            else:
                return True
