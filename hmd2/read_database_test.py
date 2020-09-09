#import sys
#sys.path.append(r'C:\Users\drew.bennett\Documents\hmd')

from hmd import hmd
#########################################


q='''
        select sec as label,int_meas_len(sec) as length,(select cast(snode as varchar) from network where network.sec=fitted2.sec) as SNODE,xsp,s_ch,e_ch,sc,
        'UKPMS' as network,'' as sdate,''as edate,'' as stime,'' as etime
        from fitted2 where xsp='CL1' and not sc is null
        order by sec,s_ch
'''

a=hmd()

#a.section_processor.set_query_cols({'LABEL':0,'LENGTH':1,'SNODE':2},{'SDATE':'','EDATE':'','STIME':'','ETIME':'','NETWORK':'UKPMS'})
#a.set_observ_cols({'xsp':3,'schain':4,'echain':5},{'defect':'SFC','version':'1'})
#a.set_obval_cols({'value':6},{'parm':'12','option':'','percent':'V'})
a.read_query('192.168.5.157','pts1962-05_north_tyneside',q,'stuart',thresholds=False,observs=False,obvals=False)#
a.set_survey_line(r'SURVEY\UKPMS,SCRIM,,5,10M,HSL,V0116a,1, F;')

a.to_hmd('query_test.hmd')
    
#print(a.sects)
#{'1775A20302/00028_000958': <section.sect object at 0x000001CB0BCEFE10>, '1775A20306/00021_096240': <section.sect object at 0x000001CB0BD0C4E0>, 
#'1775A288_0/00031_004887': <section.sect object at 0x000001CB0DD8E550>, '1775A288_1/00057_000382': <section.sect object at 0x000001CB0DD8E240>, 
#'1775A3___0/00096_096608': <section.sect object at 0x000001CB0DD8E2E8>}



#print(len(a.sects['1775A20302/00028_000958'].observs))#100
