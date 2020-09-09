import psycopg2
  

def upload_readings(hmd,table,host,db_name,user,password='',port='5432',overwrite=True): 
    con=psycopg2.connect(host=host,dbname=db_name,user=user,password=password,port=port)
    cur=con.cursor()
    atts=['LABEL','SNODE','LENGTH']+hmd.observ_processor.atts+hmd.obval_processor.atts
    #print(hmd.observ_processor.atts+hmd.obval_processor.atts)
    q='insert into {table}({cols}) values ({vals})'.format(table=table,cols=','.join(atts),vals=','.join(['%('+a+')s' for a in atts]))    
    #execute_batch should be faster than looping- less round trips
    psycopg2.extras.execute_batch(cur,q,list_vals(hmd))            
    con.commit()
    con.close()  
        

def list_vals(hmd):
    vals=[]
    for s in hmd.sects.values():
        vals+=section_vals(s)
    return vals


def section_vals(s):
    vals=[]
    lab={'LABEL':s.vals['LABEL'],'SNODE':s.vals['SNODE'],'LENGTH':s.vals['LENGTH']}
    for obs in s.subrecs['observ']:
        for obv in obs.subrecs['obval']:
                #vals.append(add_dicts([s.vals,obs.vals,obv.vals]))
            vals.append(add_dicts([lab,obs.vals,obv.vals]))
    return vals
    

def upload_sections(hmd,table,host,db_name,user,password='',port='5432'): 
    con=psycopg2.connect(host=host,dbname=db_name,user=user,password=password,port=port)
    cur=con.cursor()
    atts=hmd.section_processor.atts
    q='insert into {table}({cols}) values ({vals})'.format(table=table,cols=','.join(atts),vals=','.join(['%('+a+')s' for a in atts]))
    #execute_batch should be faster than looping- less round trips
    psycopg2.extras.execute_batch(cur,q,[s.vals for s in hmd.sects.values()])      
    con.commit()
    con.close()  
        

#need types . take some values and try to cast to int,float,string in that order?
def init_sections(hmd,table,host,db_name,user,password='',port='5432'): 
    con=psycopg2.connect(host=host,dbname=db_name,user=user,password=password,port=port)
    cur=con.cursor()
    atts=hmd.section_processor.atts
    q="drop table if exists {table}".format(table=table)
    cur.execute(q)
    
    q='create table {table} (t)'.format(table=table,cols=','.join(atts),vals=','.join(['%('+a+')s' for a in atts]))
    q=''
    
    for s in hmd.sects.values():
        cur.execute(q,s.vals)
            
    con.commit()
    con.close()  


#list of dicts
def add_dicts(dl):
    r={}
    for d in dl:
        r.update(d)
    return r
    

