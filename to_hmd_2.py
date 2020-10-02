from .hmd2.hmd import hmd


def to_hmd_snode(to,f,r,db):
    a=hmd()
    a.set_survey_line(r'SURVEY\,SCRIM,1,,10M,,SKID,1,F;')
    a.observ_processor.set_query_cols({'XSECT':'xsp','SCHAIN':'s_ch','ECHAIN':'e_ch'},{'DEFECT':'SFC','VERSION':'1'})
    a.observ_processor.template_line='OBSERV\\{DEFECT},{VERSION},{XSECT},{SCHAIN:.0f},{ECHAIN:.0f};\n'
    a.obval_processor.set_query_cols({'VALUE':'sfc'},{'PARM':'12','OPTION':'','PERCENT':'V'}) #OBVAL\PARM,OPTION,VALUE,PERCENT;
    a.obval_processor.template_line='OBVAL\\{PARM},{OPTION},{VALUE:.2f},{PERCENT};\n'
    a.section_processor.set_query_cols({'LABEL':'sec','LENGTH':'meas_len','SDATE':'sdate','EDATE':'edate','SNODE':'snode'},{'NETWORK':'UKPMS','STIME':'','ETIME':''})
        
    if f:
        q='''
select sec,int_meas_len(sec) as meas_len,xsp,s_ch,e_ch,sfc,
(select to_char(min(survey_date),'ddmmyyyy') from run_info where run in(select run from fitted where pk=any(r.pks))) as sdate,
(select to_char(max(survey_date),'ddmmyyyy') from run_info where run in(select run from fitted where pk=any(r.pks))) as edate,
(select start_node from network where network.sec=r.sec) as snode,
(select end_node from network where network.sec=r.sec) as enode
from resized as r where not reversed and (not sfc is null)
order by sec,xsp,s_ch

        '''

       
        a.read_query(db.hostName(),db.databaseName(),q,db.userName(),db.password(),thresholds=False,observs=True,obvals=True)

    if r:


       q='''
select sec,int_meas_len(sec) as meas_len,xsp,s_ch,e_ch,sfc,
(select to_char(min(survey_date),'ddmmyyyy') from run_info where run in(select run from fitted where pk=any(r.pks))) as sdate,
(select to_char(max(survey_date),'ddmmyyyy') from run_info where run in(select run from fitted where pk=any(r.pks))) as edate,
(select start_node from network where network.sec=r.sec) as snode,
(select end_node from network where network.sec=r.sec) as enode
from resized as r where reversed and (not sfc is null)
order by sec,xsp,s_ch

        '''

       a.read_query(db.hostName(),db.databaseName(),q,db.userName(),db.password(),thresholds=False,observs=True,obvals=True)
    
    a.to_hmd(to) 


def to_hmd(to,f,r,db):
    a=hmd()
    a.set_survey_line(r'SURVEY\,SCRIM,1,,10M,,SKID,1,F;')
    a.observ_processor.set_query_cols({'XSECT':'xsp','SCHAIN':'s_ch','ECHAIN':'e_ch'},{'DEFECT':'SFC','VERSION':'1'})
    a.observ_processor.template_line='OBSERV\\{DEFECT},{VERSION},{XSECT},{SCHAIN:.0f},{ECHAIN:.0f};\n'
    a.obval_processor.set_query_cols({'VALUE':'sfc'},{'PARM':'12','OPTION':'','PERCENT':'V'}) #OBVAL\PARM,OPTION,VALUE,PERCENT;
    a.obval_processor.template_line='OBVAL\\{PARM},{OPTION},{VALUE:.2f},{PERCENT};\n'
        
    if f:
        q='''
select sec,int_meas_len(sec) as meas_len,xsp,s_ch,e_ch,sfc,
(select to_char(min(survey_date),'ddmmyyyy') from run_info where run in(select run from fitted where pk=any(r.pks))) as sdate,
(select to_char(max(survey_date),'ddmmyyyy') from run_info where run in(select run from fitted where pk=any(r.pks))) as edate
from resized as r where not reversed and (not sfc is null)
order by sec,xsp,s_ch
        '''
        
        a.section_processor.set_query_cols({'LABEL':'sec','LENGTH':'meas_len','SDATE':'sdate','EDATE':'edate'},{'NETWORK':'UKPMS','STIME':'','ETIME':'','SNODE':'F'})
        a.read_query(db.hostName(),db.databaseName(),q,db.userName(),db.password(),thresholds=False,observs=True,obvals=True)

    if r:
        q='''
select sec,int_meas_len(sec) as meas_len,xsp,s_ch,e_ch,sfc,
(select to_char(min(survey_date),'ddmmyyyy') from run_info where run in(select run from fitted where pk=any(r.pks))) as sdate,
(select to_char(max(survey_date),'ddmmyyyy') from run_info where run in(select run from fitted where pk=any(r.pks))) as edate
from resized as r where not reversed and (not sfc is null)
order by sec,xsp,s_ch
        '''    
        a.section_processor.set_query_cols({'LABEL':'sec','LENGTH':'meas_len','SDATE':'sdate','EDATE':'edate'},{'NETWORK':'UKPMS','STIME':'','ETIME':'','SNODE':'R'})      
        a.read_query(db.hostName(),db.databaseName(),q,db.userName(),db.password(),thresholds=False,observs=True,obvals=True)
    
    a.to_hmd(to) 
    
