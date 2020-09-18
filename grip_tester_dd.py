from .database_dialog.database_dialog import database_dialog

from .hmd2.hmd import hmd
#import psycopg2
from psycopg2.extras import DictCursor,execute_batch
from os import path



'''
subclass of database_dialog specific to scrim processor.

'''

class grip_dd(database_dialog):


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
       # self.sql('select update_lengths();')


    #update coverage column of table req
    def update_coverage(self):
        self.sql('update requested set coverage=coverage(sec,reversed,xsp)')


    def setup_database(self):
        self.sql('create extension if not exists postgis')

        folder=path.join(path.dirname(__file__),'sql_scripts','setup_database')
        with open(path.join(folder,'setup.txt')) as f:
            for c in f.read().split(';'):
                com=c.strip()
                if com:
                    self.sql_script(path.join(folder,com))
      

    def autofit_run(self,run):
        self.sql_script(path.join(path.dirname(__file__),'sql_scripts','autofit_run.sql'),{'run':run})

    
    def upload_run_csv(self,run):
        try:
            ref=path.splitext(path.basename(run))[0]
            date=get_date(run)

            with self.con:
                self.cur.execute("insert into run_info(run,survey_date) values (%(ref)s,to_date(%(date)s,'dd/MM/yyyy'))",{'ref':ref,'ref2':ref,'date':date})
                
                q='insert into r(run,ch,left_skid,speed,f_line,pt) values(%(run)s,%(ch)s,%(left_skid)s,%(speed)s,%(f_line)s,ST_transform(ST_SetSRID(ST_makePoint(%(lon)s,%(lat)s),4326),27700));'

                with open(run,'r') as f:
                     vals = [read_line(line,i+1,ref) for i,line in enumerate(f.readlines())]
                vals = [v for v in vals if v]

                execute_batch(self.cur,q,vals)
            #self.con.commit()

            self.sql_script(path.join(path.dirname(__file__),'sql_scripts','update_run.sql'),{'run':ref})#run is name of run in run_info
            
            return True
            
        except Exception as e:
            self.con.rollback()
            return e



    def refit_run(self,run):
        #self.cancelable_task(self.sql,{'q':'select refit_run(%(run)s);','args':run},'grip tester tool:refitting run')

        q='select refit_run(%(run)s);select resize_run(%(run)s);'
        
        self.cancelable_query(q=q,args={'run':run},text='refitting run:'+run,sucess_message='grip tester tool:refit run:'+run)
        #self.sql('select refit_run(%(run)s);',run)
        #self.sql('select resize_run(%(run)s);',run)


    def refit_runs(self,runs):

        #queries=['select refit_run(%(run)s,False);' for r in runs]
        #args=[{'run':r} for r in runs]
        #queries.append('select calc_benchmarks();') #need to set scf through calc_benchmarks before resizing   
        #args.append(None)
        
        #queries+=['select resize_run(%(run)s);' for r in runs]
       # args+=[{'run':r} for r in runs]
        
   
                       
        #self.cancelable_queries(queries=queries,args=args,text='refitting all runs',sucess_message='grip tester tool:refit runs')
        
        #'select refit_all();')
         #   'select resize_all();')  


        
        self.cancelable_queries(queries=['select refit_all();','select resize_all();'],args=None,text='refitting all runs',sucess_message='grip tester tool:refit runs')


    
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

















        
