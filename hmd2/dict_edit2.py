#import sys
#from PyQt4.QtGui import *

#from PyQt5.QtGui import 
#from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QSpinBox,QPushButton,QDialog,QFormLayout,QLineEdit,QDoubleSpinBox
#from PyQt4.QtCore import *

#dialog for editing dict of int,float,str
class dict_edit(QDialog):
    def __init__(self,d,parent=None):
        super(QDialog,self).__init__(parent)
        #self.setupUi(self)
        
        self.vals={}
        
        form = QFormLayout()
        
        for key,val in d.items():
            if isinstance(val,int):
                b=QSpinBox()
                b.setValue(val)
            
            if isinstance(val,str):
                b=QLineEdit()
                b.setText(val)
                
            if isinstance(val,float):
                b=QDoubleSpinBox()
                b.setValue(val)
                
            self.vals.update({key:b})
            form.addRow(key, b)
            
        self.setLayout(form)


    def output(self):
        d={}
        for key,val in self.vals.items():
            if isinstance(val,QSpinBox) or isinstance(val,QDoubleSpinBox):
                d.update({key:val.value()})
            if isinstance(val,QLineEdit):
                d.update({key:val.text()})
        return d
    
    


if __name__ == '__main__':
  #  window()
    de=dict_edit({'label':1.1,'a':3,'c':'hello'})
    de.exec_()
    print(de.output())
    
