#import sys
#sys.path.append(r'C:\Users\drew.bennett\Documents\hmd\hmd2')
from hmd import hmd

#use hmd2 to download query.


a=hmd()
q='''
        select sec,int_meas_len(sec) as meas_len,
		(select snode from network where network.sec=fitted2.sec),
		xsp,s_ch,e_ch,sc,
		(select to_char(sdate,'ddmmyyyy') from sedates where sedates.sec=fitted2.sec and sedates.xsp=fitted2.xsp) as sdate,
        (select to_char(sdate,'ddmmyyyy')  from sedates where sedates.sec=fitted2.sec and sedates.xsp=fitted2.xsp) as edate
        from fitted2 where xsp='CL1' and not sc is null
        order by sec,s_ch
        '''     
        
        
 #       SURVEY\OWNER,TYPE,VERSION,NUMBER,SUBSECT,MACHINE,PREPROC,SVC,XSPUSED;
#SURVEY\,SCRIM,1,,10M,,SKID,1,F;

#a.survey_processor.set_query_cols({},{'OWNER':'','TYPE':'SCRIM','VERSION':'1','NUMBER':'','SUBSECT':'10m','MACHINE':'','PREPROC':'SKID','SVC':'1','XSPUSED':'F'})        
#a.set_survey_line(r'SURVEY\UKPMS,SCRIM,,5,10M,HSL,V0116a,1, F;')
a.set_survey_line(r'SURVEY\,SCRIM,1,,10M,,SKID,1,F;')


a.section_processor.set_query_cols({'LABEL':'sec','LENGTH':'meas_len','SDATE':'sdate','EDATE':'edate'},{'NETWORK':'UKPMS','STIME':'','ETIME':'','SNODE':'F'})
a.observ_processor.set_query_cols({'XSECT':'xsp','SCHAIN':'s_ch','ECHAIN':'e_ch'},{'DEFECT':'SFC','VERSION':'1'})
a.observ_processor.template_line='OBSERV\\{DEFECT},{VERSION},{XSECT},{SCHAIN:.0f},{ECHAIN:.0f};\n'

a.obval_processor.set_query_cols({'VALUE':'sc'},{'PARM':'12','OPTION':'','PERCENT':'V'}) #OBVAL\PARM,OPTION,VALUE,PERCENT;
a.obval_processor.template_line='OBVAL\\{PARM},{OPTION},{VALUE:.2f},{PERCENT};\n'

a.read_query(query=q,db_name='pts1936-11_Bedford',host='192.168.5.157',user='stuart',thresholds=False)


a.to_hmd('test.hmd')


  # a.set_observ_cols({'xsp':3,'schain':4,'echain':5},{'defect':'SFC','version':'1'})
#a.section_processor.set_read_cols({'LABEL':7,'SNODE':1},{'NETWORK':'UKPMS','LENGTH':'','SDATE':'','EDATE':'','STIME':'','ETIME':''})
#    a.set_section_cols({'label':0,'length':1,'snode':2},{'sdate':'','edate':'','stime':'','etime':'','network':'UKPMS'})    
#a.read_pg_table(db.hostName(),db.databaseName(),q,db.userName(),db.password())