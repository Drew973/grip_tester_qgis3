from PyQt4.QtGui import QFormLayout,QSpinBox,QWidget

w=QWidget()
d={'label':1,'a':3,'b':6}

widgets = {}
form = QFormLayout()
for key, value in d.iteritems():
    widgets[key] = widget = {}
    widget['spinbox'] = spinbox = QSpinBox()
    spinbox.setValue(value)
    form.addRow(key, spinbox)
    
w.setLayout(form)

w.show()
