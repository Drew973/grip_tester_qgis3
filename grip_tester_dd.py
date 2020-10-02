from .database_dialog.database_dialog import database_dialog

from .hmd2.hmd import hmd
#import psycopg2
from psycopg2.extras import DictCursor,execute_batch
from os import path


'''
subclass of database_dialog specific to scrim processor.

'''

SCHEMA='gtest'

class grip_dd(database_dialog):

    def __init__(self,parent=None):
        self.routes_table='gtest.routes'
        database_dialog.__init__(self,parent)

    def upload_s10(self,s10):
        pass


#',' in note column is problem. fix with quote charactors?
    def upload_route(self,csv):
        with open(csv,'r') as f:
            self.cur.copy_expert('copy routes from STDIN with CSV HEADER',f)
            #c.copy_from(f,'routes',sep=',')
            self.con.commit()
            

    def download_routes(self,f):
        #self.query_to_csv(query='select * from routes order by run,s',to=s,force_quote='(run,sec,note)')
        self.cur.copy_expert("COPY routes TO STDOUT WITH (FORMAT CSV,HEADER,FORCE_QUOTE(run,sec,note),null '')",f)
        
    
    def search_hmds(self,hmds,reset=False):

        if reset:
            self.sql("update requested set hmds='{}'::varchar[];")
        
        for h in hmds:
            self.search_hmd(h)


#update hmds column of table req by searching hmd file f.
 #direction of xsp values in f and table req needs to be the same. ie both in direction of section or both in direction of survey.
    def search_hmd(self,f):
        h=hmd()
        h.read_hmd(f)
        with self.con:
            labs=[{'xsp':xsp,'sec':sec.vals['LABEL'],'hmd':f} for sec in h.sects.values() for xsp in sec.xsp_vals()]#dict for each sec+xsp in hmd
            #array_append(null,val) gives null. added not null constraint to hmds col.
            execute_batch(self.cur,'update requested set hmds=array_append(hmds,%(hmd)s) where sec=%(sec)s and xsp=%(xsp)s and not %(hmd)s=any(hmds);',labs)


    #update coverage column of table req
    def update_coverage(self):
        self.sql('update gtest.requested set coverage=gtest.coverage(sec,reversed,xsp)')


#reads setup.txt, seperated by ;. If file then runs script otherwise run line.
    def setup_database(self):
        folder=path.join(path.dirname(__file__),'sql_scripts')
        with open(path.join(folder,'setup.txt')) as f:
            for c in f.read().split(';'):
                com=c.strip()
                f=path.join(folder,com)
                if com:
                    if path.exists(f):
                        print(f)
                        self.sql_script(f)
                    else:
                        print(com)
                        self.sql(com)
                        

    def autofit_run(self,run):
        self.sql('select gtest.autofit_run(%(run)s)',{'run':run})
        
    
    def upload_run_csv(self,run):
        try:
            ref=path.splitext(path.basename(run))[0]
            date=get_date(run)

            with self.con:
                self.cur.execute("insert into gtest.run_info(run,survey_date) values (%(ref)s,to_date(%(date)s,'dd/MM/yyyy'))",{'ref':ref,'ref2':ref,'date':date})
                
                q='insert into gtest.readings(run,ch,left_skid,speed,f_line,pt) values(%(run)s,%(ch)s,%(left_skid)s,%(speed)s,%(f_line)s,ST_transform(ST_SetSRID(ST_makePoint(%(lon)s,%(lat)s),4326),27700));'

                with open(run,'r') as f:
                     vals = [read_line(line,i+1,ref) for i,line in enumerate(f.readlines())]
                vals = [v for v in vals if v]

                execute_batch(self.cur,q,vals)
            #self.con.commit()

            self.sql('select gtest.update_readings(%(run)s)',{'run':ref}) 
            
            return True
            
        except Exception as e:
            self.con.rollback()
            return e


    def drop_runs(self,runs):
        runs='{'+','.join(runs)+'}'
        self.sql('delete from gtest.run_info where run =any(%(runs)s::varchar[])',{'runs':runs})


    def refit_run(self,run):
        #self.cancelable_task(self.sql,{'q':'select refit_run(%(run)s);','args':run},'grip tester tool:refitting run')
        q='select gtest.refit_run(%(run)s);select gtest.resize_run(%(run)s);'        
        self.cancelable_query(q=q,args={'run':run},text='refitting run:'+run,sucess_message='grip tester tool:refit run:'+run)


    def refit_runs(self,runs):        
        self.cancelable_queries(queries=['select gtest.refit_all();','select gtest.resize_all();'],args=None,text='refitting all runs',sucess_message='grip tester tool:refit runs')


    def get_runs(self):
        res=self.sql('select run from gtest.run_info order by run',ret=True)
        return [r['run'] for r in res]

    
#parse line of run csv
    #n=int line number
def read_line(line,f_line,run):
    row=line.strip().split(',')
    try:
        return {'ch':float(row[0]),'left_skid':float(row[1]),'speed':float(row[3]),'lat':float(row[7]),'lon':float(row[8]),'f_line':f_line,'run':run}
    except:
        pass   


#find date from run csv p
def get_date(p):
    with open(p,'r') as f:
        for i,line in enumerate(f.readlines()):
            if i==2:
                return line.split(',')[18]

       
