from qgis.PyQt import  QtGui, uic
from qgis.PyQt.QtCore import pyqtSignal,Qt,QUrl#,QEvent
from qgis.PyQt.QtSql import QSqlTableModel

from qgis.utils import iface

from qgis.PyQt.QtSql import QSqlQuery,QSqlQueryModel
from qgis.PyQt.QtWidgets import QMessageBox,QWhatsThis,QToolBar
import os

from os import path
import sys

#print(path.dirname(__file__))
#d=path.dirname(__file__)

from . import color_functions,grip_tester_dd,file_dialogs,copy_functions

from .to_hmd_2 import to_hmd,to_hmd_snode
#from . import database_dialog

#from fitter_functions import load_files_dialog,save_file_dialog,load_file_dialog
#from .better_table_model import better_table_model

#from .copy_action import make_copyable
#from qgis.PyQt.QtGui  import QDesktopServices,QMenuBar#fails. not version independent. Documentation lies.
from PyQt5.QtWidgets import QMenuBar,QDockWidget,QMenu
from PyQt5.QtGui import QDesktopServices

from .routes_widget.routes_widget import routes_widget
from .routes_widget.layer_functions import select_sections
from .routes_widget.better_table_model import betterTableModel


#from qgis.PyQt.QtWebKit import QWebView,QDesktopServices 

def fixHeaders(path):
    with open(path) as f:
        t=f.read()
    r={'qgsfieldcombobox.h':'qgis.gui','qgsmaplayercombobox.h':'qgis.gui'}
    for i in r:
        t=t.replace(i,r[i])
    with open(path, "w") as f:
        f.write(t)

uiPath=os.path.join(os.path.dirname(__file__), 'grip_tester_dockwidget_base.ui')
fixHeaders(uiPath)
FORM_CLASS, _ = uic.loadUiType(uiPath)


class grip_testerDockWidget(QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, parent=None):
        super(grip_testerDockWidget, self).__init__(parent)
        self.setupUi(self)

        self.connect_button.clicked.connect(self.connect)
        self.dd=grip_tester_dd.grip_dd(self)

        self.s10_button.clicked.connect(self.set_s10)
        self.zm3_button.clicked.connect(self.set_zm3)
        self.upload_button.clicked.connect(self.upload_run)

        self.to_hmd_button.clicked.connect(self.download_hmd)
        self.prepare_database_button.clicked.connect(self.prepare_database)

        self.search_hmds_button.clicked.connect(self.search_hmds)
          
        self.rw=routes_widget(self,self.dd,'gtest.routes',self.readings_box,self.network_box,self.run_fieldbox,self.f_line_fieldbox,self.sec_fieldbox)

        self.rw_placeholder.addWidget(self.rw)
        #self.tabs.insertTab(2,self.rw,'Fitting')
        
        self.upload_csv_button.clicked.connect(self.upload_run_csvs)

        self.init_requested_menu()
        self.init_missing_menu()
        self.init_run_menu()
        
        self.open_help_button.clicked.connect(self.open_help)        

        self.copy_lengths_button.clicked.connect(lambda:copy_functions.copy_all(self.lengths_view))
        self.copy_missing_button.clicked.connect(lambda:copy_functions.copy_all(self.missing_view))
        self.copy_benchmarks_button.clicked.connect(lambda:copy_functions.copy_all(self.benchmarks_view))
        self.upload_folder_button.clicked.connect(self.upload_folder)

        
    def connect(self):
        if self.dd.exec_():
            if self.dd.connected:
                self.database_label.setText('Connected to %s'%(self.dd.db.databaseName()))
                self.dd.sql('set search_path to gtest,public;')
                self.connect_coverage()
                self.connect_lengths()
                self.connect_missing()
                self.connect_benchmarks()
                self.rw.refresh_runs()
                self.connect_run_info()
                self.tabs.currentChanged.connect(self.refresh_coverage)
                self.coverage_toolbox.currentChanged.connect(self.refresh_coverage)
                self.requested_model.dataChanged.connect(lambda:self.missing_model.setQuery(self.missing_model.query()))

                
            else:
                self.database_label.setText('Not Connected')


#opens help/index.html in default browser
    def open_help(self):
        help_path=os.path.join(os.path.dirname(__file__),'help','index.html')
        help_path='file:///'+os.path.abspath(help_path)
        QDesktopServices.openUrl(QUrl(help_path))
        

    def connect_run_info(self):
        self.run_info_model=QSqlTableModel(db=self.dd.db)
        self.run_info_model.setTable('gtest.run_info')
        self.run_info_model.setSort(self.run_info_model.fieldIndex("run"),Qt.AscendingOrder)
        self.run_info_model.setEditStrategy(QSqlTableModel.OnFieldChange)
        
        self.run_info_view.setModel(self.run_info_model)
        self.run_info_model.select()
        
            
    def connect_coverage(self):
       # self.requested_model = QSqlTableModel(db=self.dd.db)
        self.requested_model=betterTableModel(db=self.dd.db)
        self.requested_model.setEditStrategy(QSqlTableModel.OnFieldChange)        
        self.requested_model.setTable('gtest.requested')
        self.requested_model.setEditable(False)#set all cols uneditable
        self.requested_model.setColEditable(self.requested_model.fieldIndex("note"),True)#make note col editable

        self.requested_model.setSort(self.requested_model.fieldIndex("sec"),Qt.AscendingOrder)
        
        self.requested_view.setModel(self.requested_model)
        self.requested_view.setColumnHidden(self.requested_model.fieldIndex("pk"), True)#hide pk column
        self.requested_view.setColumnHidden(self.requested_model.fieldIndex("coverage"), True)#hide coverage column
        
        #self.show_all_button.clicked.connect(self.coverage_show_all)
        #self.show_missing_button.clicked.connect(self.coverage_show_missing)
        self.show_missing_button.clicked.connect(self.filter_requested)
        self.show_all_button.clicked.connect(self.filter_requested)
        self.partly_missing_button.clicked.connect(self.filter_requested)

        self.filter_requested()

        self.requested_view.resizeColumnsToContents()


    def filter_requested(self):
        if self.show_missing_button.isChecked():
            self.requested_model.setFilter("cardinality(hmds)=0")

        if self.show_all_button.isChecked():
            self.requested_model.setFilter('')

        if self.partly_missing_button.isChecked():
            self.requested_model.setFilter('cardinality(hmds)>0 and (select count (sec) from gtest.resized where gtest.resized.sec=gtest.requested.sec and gtest.resized.reversed=gtest.requested.reversed and sfc is null)>1')
                
        self.requested_model.select()


    def connect_benchmarks(self):
        self.benchmarks_model=QSqlQueryModel()
        self.benchmarks_model.setQuery("select early,mid,late,com from gtest.benchmarks_view order by sec,xsp,s_ch",self.dd.db)
        self.benchmarks_view.setModel(self.benchmarks_model)
        self.benchmarks_view.resizeColumnsToContents()

    def refresh_coverage(self):
        self.requested_model.select()
        self.missing_model.setQuery(self.missing_model.query())
        self.lengths_model.setQuery(self.lengths_model.query())
        self.benchmarks_model.setQuery(self.benchmarks_model.query())

    def connect_missing(self):
        self.missing_model=QSqlQueryModel()
        self.missing_model.setQuery("select * from gtest.missing_view",self.dd.db)
        self.missing_view.setModel(self.missing_model)
        self.missing_view.resizeColumnsToContents()

        
    def connect_lengths(self):
        self.lengths_model=QSqlQueryModel()
        self.lengths_model.setQuery("select * from gtest.lengths",self.dd.db)
        self.lengths_view.setModel(self.lengths_model)
        self.lengths_view.resizeColumnsToContents()
        #make_copyable(self.lengths_view)

        
    def check_connected(self):
        if self.dd.con:
            return True
        else:
            iface.messageBar().pushMessage('fitting tool: Not connected to database')
            return False


    def upload_run_csvs(self):
        if self.check_connected():
            files=file_dialogs.load_files_dialog('.csv','upload csv')
            if files:
                for f in files:
                    #r=self.dd.upload_run_csv(f)
                    r=self.dd.upload_run(f)
                    if r==True:
                        self.upload_log.appendPlainText('sucessfully uploaded %s'%(f))
                    else:
                        self.upload_log.appendPlainText('error uploading %s:%s'%(f,str(r)))
                  #  self.upload_log.repaint()
                    self.update()
                    #processEvents()
               
                self.run_info_model.select()
                self.rw.refresh_runs()
            

    def upload_folder(self):
        folder=file_dialogs.load_directory_dialog('.csv','upload all .csv in directory')
        if folder:
            self.dd.upload_runs(file_dialogs.filter_files(folder,'.csv'))
                
            
        
    def closeEvent(self, event):
        self.dd.disconnect()        
        self.closingPlugin.emit()
        event.accept()


    def upload_run(self):
        if self.check_connected():
            if self.run_number.text()=='':
                iface.messageBar().pushMessage('fitting tool: run number not set')
            else:
            
                self.dd.sql("insert into run_info select '{run}',to_date('{date}','dd-mm-yyyy') where not exists (select run from run_info where run='{run}')",
                                     {'run':self.run_number.text(),'date':str(self.survey_date.date().day())+'-'+str(self.survey_date.date().month())+'-'+str(self.survey_date.date().year())})

                if self.s10.text()!='':
                    try:
                        upload_s10(self.run_number.text(),self.s10.text(),db_to_con(self.dd.db))
                        iface.messageBar().pushMessage('fitting tool: uploaded s10:'+str(self.s10.text()))

                    except Exception as e:
                        iface.messageBar().pushMessage('fitting tool: error uploading s10:'+self.s10.text()+': '+str(e))


                if self.zm3.text()!='':
                    try:#zm3,con
                        upload_zm3(self.run_number.text(),self.zm3.text(),db_to_con(self.dd.db))
                        iface.messageBar().pushMessage('fitting tool: uploaded zm3:'+self.zm3.text())
                    except Exception as e:
                        iface.messageBar().pushMessage('fitting tool: error uploading zm3:'+self.zm3.text()+': '+str(e))
                        
                self.rw.refresh_runs()
                
    
    def set_s10(self):
        s=file_dialogs.load_file_dialog('.s10','load .s10')        
        if s:
            self.s10.setText(s)  
 

    def set_zm3(self):
            s=file_dialogs.load_file_dialog('.zm3','load .zm3')        
            if s:
                self.zm3.setText(s)

                    
    def download_hmd(self):
        if self.check_connected():
            s=file_dialogs.save_file_dialog('.hmd')
            print(s)
            if s:
                if self.include_snode_box.isChecked():
                    to_hmd_snode(s,self.forward_box.isChecked(),self.reversed_box.isChecked(),self.dd.db)
                else:
                    to_hmd(s,self.forward_box.isChecked(),self.reversed_box.isChecked(),self.dd.db)
                iface.messageBar().pushMessage('fitting tool: saved:'+s)
    
                
    def prepare_database(self):
        if self.check_connected():
            msgBox=QMessageBox();
            msgBox.setText("DON'T USE THIS PARTWAY THROUGH THE JOB! because this will erase any data in tables used by this plugin.");
            msgBox.setInformativeText("Continue?");
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No);
            msgBox.setDefaultButton(QMessageBox.No);
            i=msgBox.exec_()
            if i==QMessageBox.Yes:
                self.dd.setup_database()
                iface.messageBar().pushMessage('fitting tool: prepared database')

    #drop selected run of run_info table
    def drop_run(self):
        r=self.run_box.currentText()
        self.dd.sql("delete from run_info where run='{run}'",{'run':r})
        self.rw.get_runs()
            
                
    def search_hmds(self):
        hmds=file_dialogs.load_files_dialog(ext='.hmd',caption='search hmds')
        if hmds and self.check_connected():
            self.dd.search_hmds(hmds,reset=True)
            iface.messageBar().pushMessage('fitting tool:searched hmds: '+','.join(hmds))
            self.missing_model.setQuery("select * from missing_view")#refresh missing_model
            self.lengths_model.setQuery("select * from lengths")
            self.requested_model.select()


#for requested view
    def init_requested_menu(self):
        self.requested_menu = QMenu()
        requested_zoom_act=self.requested_menu.addAction('zoom to section')
        requested_zoom_act.triggered.connect(lambda:self.select_on_network([i.data() for i in self.requested_view.selectionModel().selectedRows()]))

        copy_all_requested_act=self.requested_menu.addAction('copy all rows to clipboard')
        copy_all_requested_act.triggered.connect(lambda:copy_functions.copy_all(self.requested_view))

        self.requested_view.setContextMenuPolicy(Qt.CustomContextMenu);
        self.requested_view.customContextMenuRequested.connect(self.show_requested_menu)
        

#for missing_view
    def init_missing_menu(self):
        self.missing_menu = QMenu()
        act=self.missing_menu.addAction('zoom to section')
        act.triggered.connect(lambda:self.select_on_network([i.data() for i in self.missing_view.selectionModel().selectedRows(1)]))# selectedRows(1) returns column 1 (sec)
        self.missing_view.setContextMenuPolicy(Qt.CustomContextMenu);
        self.missing_view.customContextMenuRequested.connect(self.show_missing_menu)


#for run_info_view
    def init_run_menu(self):
        self.run_info_menu = QMenu()
        act=self.run_info_menu.addAction('drop run')
        act.triggered.connect(lambda:self.dd.drop_runs([str(i.data()) for i in self.run_info_view.selectionModel().selectedRows(0)]))# selectedRows(0) returns column 0 (run)
        act.triggered.connect(self.refresh_runs)# selectedRows(0) returns column 0 (sec)

        self.run_info_view.setContextMenuPolicy(Qt.CustomContextMenu);
        self.run_info_view.customContextMenuRequested.connect(self.show_run_info_menu)

        
    def show_requested_menu(self,pt):
        self.requested_menu.exec_(self.mapToGlobal(pt))


    def show_missing_menu(self,pt):
        self.missing_menu.exec_(self.mapToGlobal(pt))


    def show_run_info_menu(self,pt):
        self.run_info_menu.exec_(self.mapToGlobal(pt))


    def refresh_runs(self):
        self.rw.get_runs()
        self.run_info_model.select()
       

#select sec on network
    def select_on_network(self,sects):
       # inds=self.requested_view.selectionModel().selectedRows()#indexes of column 0
        have_network=self.network_box.currentLayer() and self.sec_fieldbox.currentField()
        
        if have_network:
            select_sections(sects,self.network_box.currentLayer(),self.sec_fieldbox.currentField(),zoom=True)

        else:
            iface.messageBar().pushMessage('fitting tool:network layer&section field not set')
