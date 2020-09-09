
from .hmd_record import hmd_record

class threshold(hmd_record):    
  
    def output(self):
        return self.output_line()
    
    def invert(self,sec_len):
        if self.vals['FTXSECT']=='CL1':
            self.vals['FTXSECT']='CR1'
        else:
            if self.vals['FTXSECT']=='CR1':
                self.vals['FTXSECT']='CL1'
        
        self.vals['FTSCHAIN']=sec_len-self.vals['FTSCHAIN']
        self.vals['FTECHAIN']=sec_len-self.vals['FTECHAIN']
    
    #swap chainages where schain>echain
    def maybe_swap_ch(self):
        if self.vals['FTSCHAIN']>self.vals['FTECHAIN']:
            old=self.vals['FTECHAIN']
            self.vals['FTECHAIN']=self.vals['FTSCHAIN']
            self.vals['FTSCHAIN']=old

    def __lt__(self,other):
        return self.vals['FTSCHAIN']<other.vals['FTSCHAIN']
    
    
    def __eq__(self,other):
        return self.vals['FTSCHAIN']==other.vals['FTSCHAIN']
    
    
