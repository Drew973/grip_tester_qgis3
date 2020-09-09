#import sys
from os import path
#sys.path.append(r'C:\Users\drew.bennett\Documents\hmd')

from hmd import hmd

folder=r'C:\Users\drew.bennett\Documents\hmd_jobs\add_thresholds\Wokingham'

a=hmd()
#a.read_hmd(path.join(folder,'SC19HMDF.DIF'))

#with open(path.join(folder,'SC19HMDF.DIF'),'r') as f:

a.section_processor.set_csv_cols({'LABEL':0,'SNODE':1},
                                  {'LENGTH':0,'SDATE':'','EDATE':'','STIME':'','ETIME':'','NETWORK':'UKPMS'})
a.threshold_processor.set_csv_cols({'FTXSECT':6,'FTSCHAIN':2,'FTECHAIN':3,'FTNUM':5,'SCODE':4},{'FTSDATE':'','PIFIND':''})
a.read_csv(path.join(folder,'Wokingham_SCRIM_IL_Updated.csv'),thresholds=True,observs=False,obvals=False,header=True)

#a.filter_sections("sec.vals['SNODE']=='F' and sec.vals['observ']!=[]",inplace=True)

a.to_hmd('test2.hmd')
    
    
#print([s.label for s in a.missing_thresholds()])


##pifind of m?

#print(a.filter_sections("sec.snode=='R'"))       
       
#print([s.label for s in a.missing_thresholds()])
