from qgis.PyQt.QtSql import QSqlTableModel#,QSqlQueryModel
from qgis.PyQt.QtCore import Qt



class betterTableModel(QSqlTableModel):

    def __init__(self,db, dbcursor=None):
        super(better_table_model, self).__init__(db=db,dbcursor=dbcursor)
        self.colorFunction=None
        self.editable_dict={col:True for col in range(0,self.columnCount())}#dict of column index:editable 
        

 #index=qmodelindex 
    #called by model to refresh tableviews etc
    def data(self, index, role):
        if role == Qt.BackgroundRole:
            if self.colorFunction:
                if self.colorFunction(index):
                    return self.color_function(index)
                
        return QSqlTableModel.data(self, index, role);


#sets function to determine colour of cell given index. Function should return QBrush,False or None.
    
    def setColorFunction(self,function):
        self.color_function=function
             
    
    
