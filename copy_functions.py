import io
import csv

from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QApplication
#from PyQt4.QtGui import QApplication

'''
functions for copying contents of QtableView
'''

#copy selected items of QtableView tv to clipboard in excel compatible format
def copy_selection(tv):
        selection = tv.selectedIndexes()
        if selection:
                rows = sorted(index.row() for index in selection)
                columns = sorted(index.column() for index in selection)
                rowcount = rows[-1] - rows[0] + 1
                colcount = columns[-1] - columns[0] + 1
                table = [[''] * colcount for _ in range(rowcount)]
                for index in selection:
                        row = index.row() - rows[0]
                        column = index.column() - columns[0]
                        table[row][column] = index.data()
                stream = io.StringIO()#python3
                #stream = io.BytesIO()#python2   
            
                csv.writer(stream,dialect='excel',delimiter='\t').writerows(table)
                QApplication.clipboard().setText(stream.getvalue())


#copy all items of QtableView tv to clipboard in excel compatible format
def copy_all(tv):
        model=tv.model()
        table=[[parse(model.index(row,col).data(role=Qt.DisplayRole)) for col in range(0,model.columnCount())] for row in range(0,model.rowCount())]


        #null is PyQt5.QtCore.QVariant 
      #  print(table)
        stream = io.StringIO()#python3
        #stream = io.BytesIO()#python2   
            
        csv.writer(stream,dialect='excel',delimiter='\t').writerows(table)
        QApplication.clipboard().setText(stream.getvalue())



#ugly fix for null qvariant becoming 'NULL'
#returns empty string if v is null qvariant otherwise v
def parse(v):
        s=str(v)
        if s=='NULL':
                return ''
        else:
                return s
