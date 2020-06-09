import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from testclass import *
thistest=dettest()

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class Ui_MainWindow(object):
    def __init__(self):
        #TODO use this variabledict instead of lineedits everywhere and use updatevardict fxn to set vars/lineedits
        self.variableDict={'muBest': float('NaN'), 'muMax': float('NaN'), 'muMin': float('NaN'), 'muPrec': float('NaN'), 'sigmaBest': float('NaN'), 'designStim': float('NaN'), 'designProb': float('NaN'), 'experimentModel': float('NaN'), 'experimentDesign': float('NaN'), 'experimentBias': bool(1), 'suggestionStimulus': float('NaN')}
        self.previousTab = 0

        self.muBest= None
        self.muMax= None
        self.muMin= None
        self.muPrec= None
        #TODO muprec and designprob initializations
        # muPrec.set(int(log10(1.0/thistest.mufuzz)))
        self.sigmaBest= None
        self.designStim= None
        self.designProb= None
        # designProb.set(str(thistest.dprob))
        self.dprobwarn= None
        self.modelval= None
        self.designval= None
        self.ibias= 1
        self.stimval= ""
        self.expconf = ""
        self.clevela = "xx.xx%"
        self.clevelub = "xx.xx%"
        self.datacomment= None
        self.modelforms=["logit", "probit"]
        self.ourdesigns=["c optimal","sigma optimal","d optimal"]

        #0 muBest, 1 muMax, 2 muMin, 3 muPrec, 4 sigmaBest, 5 designStim, 6 designProb
        self.lconfig=[0,0,0,1,1,0,0]

    def rexopt(self):
        try: ptest=float(self.lineEditDesignprob.text())
        except: ptest=1.0
        if ptest > 50.0 and ptest < 100.0:
            thistest.dprob=ptest
        else: 
            thistest.dprob=99.9
            self.lineEditDesignprob.setText("99.9")
            MainWindow.statusBar().showMessage('Design probability must be between 50 and 100%') 
        thistest.tval()

    def getconf(self):
        if self.updatevariableDict():
            while 10.0**(-float(self.lineEditMuprecision.text())) > float(self.lineEditSigmabestguess.text())/5.0:
                print("debug ",self.lineEditMuprecision.text()," debug ",self.lineEditSigmabestguess.text())
                self.lineEditMuprecision.setText(str(int(self.lineEditMuprecision.text())+1))
            try: self.lconfig[0]=float(self.lineEditMubestguess.text())
            except: self.lconfig[0]=0.0
            try: self.lconfig[1]= float(self.lineEditMumaxguess.text())
            except: self.lconfig[1]=0.0
            try: self.lconfig[2]=float(self.lineEditMuminguess.text())
            except: self.lconfig[2]=0.0
            try: self.lconfig[3]=float(self.lineEditMuprecision.text())
            except: self.lconfig[3]=1.0
            try: self.lconfig[4]=float(self.lineEditSigmabestguess.text())
            except: self.lconfig[4]=1.0
            try: self.lconfig[5]=float(self.lineEditDesignstim.text())
            except: self.lconfig[5]=0.0
            try: self.lconfig[6]=float(self.lineEditDesignprob.text())
            except: self.lconfig[6]=0.0
            thistest.list2design(self.lconfig)

    def getdconf(self):
        if self.updatevariableDict():
            self.getconf()

    def setconf(self):
        if self.updatevariableDict():
            blah="{:."+self.lineEditMuprecision.text()+"f}"
            aguess=blah.format(thistest.sguess)
            self.lineEditSigmabestguess.setText(aguess)

    def f2data(self):
        fname, filters = QtWidgets.QFileDialog.getOpenFileName(MainWindow, "Select File")    
        try:
            fin=open(fname, "r")
            lines=fin.readlines()
            fin.close()
        except:
            lines=[]
        astring=""
        if len(lines) > 0:
            for aline in lines:
                astring+=aline
            self.plainTextEditCurrentdata.setPlainText(astring)

    def f2fdata(self,fname):
        try:
            fin=open(fname, "r")
            lines=fin.readlines()
            fin.close()
        except:
            lines=[]
        astring=""
        if len(lines) > 0:
            for aline in lines:
                astring+=aline
            self.plainTextEditCurrentdata.setPlainText(astring)
        print("finished f2fdata. fname = ",fname)

    def data2f(self):
        fname,filter = QtWidgets.QFileDialog.getSaveFileName(MainWindow,"Select File")
        try:
            fout=open(fname,"w")
            dtext=self.plainTextEditCurrentdata.toPlainText()
            fout.write(dtext)
            fout.close()
        except:
            print("No file selected")

    def mkdataobj(self):
        """turn text box data from page2 into organized data in object thisclass"""
        dtext=self.plainTextEditCurrentdata.toPlainText()
        thistest.text2data(dtext)

    def suggestion(self):
        if self.updatevariableDict():
            self.getconf()
            self.mkdataobj()
            thesug = thistest.nextpoint()
            blah="{:."+self.lineEditMuprecision.text()+"f}"
            testsug = blah.format(thesug)
            self.stimval = str(testsug)
            self.lineEditSuggestedstimulus.setText(testsug)

    def resuggest(self):
        if self.updatevariableDict():
            self.getconf()
            print("sguess1 = ",thistest.sguess)
            self.mkdataobj()
            print("sguess2 = ",thistest.sguess)
            thistest.reducebias = self.ibias
            print("sguess3 = ",thistest.sguess)
            thesug=thistest.nextpoint()
            print("sguess4 = ",thistest.sguess)
            blah="{:."+self.lineEditMuprecision.text()+"f}"
            testsug = blah.format(thesug)
            self.stimval = str(testsug)
            self.lineEditSuggestedstimulus.setText(testsug)

    def outmodel(self):
        if self.updatevariableDict():
            thistest.model=(self.comboBoxModelform.currentText()).strip()
            thistest.tval()
            self.resuggest()

    def outdesign(self):
        if self.updatevariableDict():
            teststring=(self.comboBoxDesign.currentText()).strip()
            if thistest.model=="probit":
                if teststring=="d optimal" :
                    thistest.xopt=1.138
                elif teststring=="sigma optimal":
                    thistest.xopt=1.56
                else:
                    thistest.tval()
            elif thistest.model=="logit":
                if teststring=="d optimal":
                    thistest.xopt=1.6
                elif teststring=="sigma optimal":
                    thistest.xopt=2.39
                else:
                    thistest.tval()   
                self.resuggest()

    def getclevels(self):
        if self.updatevariableDict():
            try:
                c1=thistest.cltcl()
                c1=0.01*int(c1/0.0001)
                c2=thistest.lklhdcl()
                c2=0.01*int(c2/0.0001)
                c1s="{:5.2f}".format(c1)
                c2s="{:5.2f}".format(c2)
                self.clevela = c1s+"%" 
                self.clevelub = c2s+"%"
                self.expconf = "Using stimulus of "+self.lineEditDesignstim.text()+" and probability "+self.lineEditDesignprob.text()+"%."
                self.label_7.setText(self.clevela + " asymptotic confidence level, likely too optimistic")
                self.label_8.setText(self.clevelub + " confidence using observed likelihood")
                self.label_9.setText(self.expconf)
            except:
                pass
        else:
            MainWindow.statusBar().showMessage('Cannot calculate: Missing parameters and/or data points') 

    def add2data(self,afloat):
        if self.updatevariableDict():
            self.stimval = self.lineEditSuggestedstimulus.text()
            thestim=self.stimval
            datastring=thestim+"  "+str(afloat)+"\n"
            datatext=self.plainTextEditCurrentdata.toPlainText()
            dlines=datatext.split('\n')
            newdatastring=""
            for aline in dlines:
                if len(aline) > 0:
                    newdatastring+=aline
                    newdatastring+="\n"
            newdatastring+=datastring
            self.plainTextEditCurrentdata.setPlainText(newdatastring)

    def addsuccess(self):
        if self.updatevariableDict():
            self.add2data(1.0)
            self.labelPassfailholder.setText("added success at "+self.stimval)
            self.resuggest()

    def addfailure(self):
        if self.updatevariableDict():
            self.add2data(0.0)
            self.labelPassfailholder.setText("added failure at "+self.stimval)
            self.resuggest()

        super(Ui_MainWindow, self).__init__()

    def freshplot(self):
        self.mkdataobj()
        iplotmodel=0

        if (self.checkBoxMlmodelsprobit.isChecked() or self.checkBoxMlmodelslogit.isChecked()): iplotmodel=1
        if (self.checkBoxLessbiasedprobit.isChecked() or self.checkBoxLessbiasedlogit.isChecked()): iplotmodel=1
        if thistest.npoints > 0:
            if self.checkBoxFreezeaxes.isChecked():
                amin,amax=self.sc.axes.get_xlim()
                bmin,bmax=self.sc.axes.get_ylim()
            self.sc.axes.clear()
            self.sc.axes.plot(thistest.sx, thistest.sy, 'r^')
            self.sc.axes.plot(thistest.fx, thistest.fy, 'bv')
            if thistest.xmax < thistest.dstimulus:
                xul=thistest.dstimulus+thistest.mufuzz
            else:
                xul=thistest.xmax+thistest.mufuzz
            t=np.arange(thistest.xmin-thistest.mufuzz,xul,0.01)
            if self.checkBoxMlmodelsprobit.isChecked():
                vals=thistest.probmusig() 
                mu=vals[0]; sigma=vals[1]
                print("prob "+str(mu)+" "+str(sigma))
                f1=thistest.arr2pg(t, mu, sigma)
                self.sc.axes.plot(t,f1)
            if self.checkBoxMlmodelslogit.isChecked():
                vals=thistest.logmusig()
                mu=vals[0]; sigma=vals[1]
                print("log "+str(mu)+" "+str(sigma))
                f1=thistest.arr2pl(t, mu, sigma)
                self.sc.axes.plot(t,f1) 
            if self.checkBoxLessbiasedprobit.isChecked():
                vals=thistest.brprob() 
                mu=vals[0]; sigma=vals[1]
                f1=thistest.arr2pg(t, mu, sigma)
                self.sc.axes.plot(t,f1)
            if self.checkBoxLessbiasedlogit.isChecked():
                vals=thistest.brlog()
                mu=vals[0]; sigma=vals[1]
                f1=thistest.arr2pl(t, mu, sigma)
                self.sc.axes.plot(t,f1)
            if self.checkBoxFreezeaxes.isChecked():
                self.sc.axes.set_xlim((amin,amax))
                self.sc.axes.set_ylim((bmin,bmax))
            if self.checkBoxShowmargin.isChecked():
                marginstring=""
                stxsd=(self.lineEditDesignstim.text()).strip()
                stypd=(self.lineEditDesignprob.text()).strip()
                if stxsd != "" and stypd != "":
                    xsd=float(stxsd)
                    ypd=float(stypd)/100.0 
                    xmarlow=t[len(t)-1]
                    i=0
                    while i < len(t):
                        if f1[i] >= ypd:
                            xmarlow=t[i]
                            i=len(t)
                        i+=1
                    ydstim=t[len(t)-1]
                    i=len(t)-1
                    while i > 0:
                        if t[i] < thistest.dstimulus:
                            ydstim=f1[i]
                            i=0
                        i-=1
                    if xmarlow < t[len(t)-1]:
                        ymarlow,junk=self.sc.axes.get_ylim()
                        self.sc.axes.plot([xmarlow,xmarlow],[ymarlow,thistest.dprob/100.0],color='black')
                        self.sc.axes.plot([xsd,xsd],[ymarlow,ydstim],color='black')
                        vmargin=xsd-xmarlow
                        blah="{:."+self.lineEditMuprecision.text()+"f}"
                        lmargin=blah.format(vmargin)
                        marginstring=", margin$="+str(lmargin)+"$"
                    else:
                        marginstring=" NO MARGIN!"
            if self.checkBoxWritevalues.isChecked():
                amin,amax=self.sc.axes.get_xlim()
                bmin,bmax=self.sc.axes.get_ylim()
                #doesn't need 'r' in front of TeX string?
                if iplotmodel:
                    blah="{:."+self.lineEditMuprecision.text()+"f}"
                    lmu=blah.format(mu)
                    lsig=blah.format(sigma)
                    labelstring="$\mu="+str(lmu)+", \sigma="+str(lsig)+"$"
                    if self.checkBoxShowmargin.isChecked(): labelstring+=marginstring
                    self.sc.axes.text(amin+0.05*(amax-amin), bmax-0.1*(bmax-bmin), labelstring)
            axlabel=self.lineEditXaxislabel.text() 
            aylabel=self.lineEditYaxislabel.text()
            if len(axlabel) > 0:
                self.sc.axes.axes.set_xlabel(axlabel)
            if len(aylabel) > 0:
                self.sc.axes.axes.set_ylabel(aylabel)
            self.sc.draw()

    def setupUi(self, MainWindow):

        #Sets up main window which encapsulates the tab widget
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 750)
        MainWindow.setMinimumSize(QtCore.QSize(900, 750))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QtCore.QSize(800, 600))
        self.centralwidget.setBaseSize(QtCore.QSize(800, 600))
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        #The tab widget which holds the majority of the program
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.tabWidget.setBaseSize(QtCore.QSize(800, 600))
        font = QtGui.QFont()
        font.setFamily("Trebuchet MS")
        font.setPointSize(11)
        font.setKerning(True)
        self.tabWidget.setFont(font)
        self.tabWidget.setIconSize(QtCore.QSize(20, 20))
        self.tabWidget.setObjectName("tabWidget")

        #Configure tab is created and, on the last line, is added to the tab widget
        self.tabConfigure = QtWidgets.QWidget()
        self.tabConfigure.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabConfigure.sizePolicy().hasHeightForWidth())
        self.tabConfigure.setSizePolicy(sizePolicy)
        self.tabConfigure.setMinimumSize(QtCore.QSize(200, 200))
        font = QtGui.QFont()
        font.setFamily("Trebuchet MS")
        font.setPointSize(10)
        font.setKerning(True)
        self.tabConfigure.setFont(font)
        self.tabConfigure.setObjectName("tabConfigure")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tabConfigure)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBoxConfigureTop = QtWidgets.QGroupBox(self.tabConfigure)
        font = QtGui.QFont()
        font.setFamily("Trebuchet MS")
        font.setPointSize(11)
        font.setKerning(True)
        self.groupBoxConfigureTop.setFont(font)
        self.groupBoxConfigureTop.setAutoFillBackground(False)
        self.groupBoxConfigureTop.setStyleSheet("")
        self.groupBoxConfigureTop.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBoxConfigureTop.setFlat(True)
        self.groupBoxConfigureTop.setCheckable(False)
        self.groupBoxConfigureTop.setObjectName("groupBoxConfigureTop")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBoxConfigureTop)
        self.horizontalLayout.setContentsMargins(50, 25, 50, 25)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox_7 = QtWidgets.QGroupBox(self.groupBoxConfigureTop)
        self.groupBox_7.setTitle("")
        self.groupBox_7.setObjectName("groupBox_7")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_7)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_6 = QtWidgets.QLabel(self.groupBox_7)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 0, 1, 1, 1)
        self.lineEditMubestguess = QtWidgets.QLineEdit(self.groupBox_7)
        self.lineEditMubestguess.setMaximumSize(QtCore.QSize(120, 16777215))
        font = QtGui.QFont()
        font.setFamily("Trebuchet MS")
        font.setPointSize(11)
        font.setKerning(True)
        self.lineEditMubestguess.setFont(font)
        self.lineEditMubestguess.setInputMethodHints(QtCore.Qt.ImhNone)
        self.lineEditMubestguess.setText("")
        self.lineEditMubestguess.setPlaceholderText("")
        self.lineEditMubestguess.setObjectName("lineEditMubestguess")
        self.gridLayout_2.addWidget(self.lineEditMubestguess, 1, 0, 1, 1)
        self.lineEditMumaxguess = QtWidgets.QLineEdit(self.groupBox_7)
        self.lineEditMumaxguess.setMaximumSize(QtCore.QSize(120, 16777215))
        self.lineEditMumaxguess.setObjectName("lineEditMumaxguess")
        self.gridLayout_2.addWidget(self.lineEditMumaxguess, 1, 1, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.groupBox_7)
        self.label_12.setToolTipDuration(-1)
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.gridLayout_2.addWidget(self.label_12, 0, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox_7)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 0, 2, 1, 1)
        self.lineEditMuminguess = QtWidgets.QLineEdit(self.groupBox_7)
        self.lineEditMuminguess.setMaximumSize(QtCore.QSize(120, 16777215))
        self.lineEditMuminguess.setObjectName("lineEditMuminguess")
        self.gridLayout_2.addWidget(self.lineEditMuminguess, 1, 2, 1, 1)
        self.horizontalLayout.addWidget(self.groupBox_7)
        self.groupBox_8 = QtWidgets.QGroupBox(self.groupBoxConfigureTop)
        self.groupBox_8.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.groupBox_8.setTitle("")
        self.groupBox_8.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_8.setObjectName("groupBox_8")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.groupBox_8)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label = QtWidgets.QLabel(self.groupBox_8)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_7.addWidget(self.label)
        self.frame_3 = QtWidgets.QFrame(self.groupBox_8)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_13.setContentsMargins(100, -1, 100, -1)
        self.horizontalLayout_13.setSpacing(0)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.lineEditMuprecision = QtWidgets.QLineEdit(self.frame_3)
        self.lineEditMuprecision.setMaximumSize(QtCore.QSize(1677777, 16777215))
        self.lineEditMuprecision.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEditMuprecision.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEditMuprecision.setObjectName("lineEditMuprecision")
        self.horizontalLayout_13.addWidget(self.lineEditMuprecision)
        self.verticalLayout_7.addWidget(self.frame_3)
        self.horizontalLayout.addWidget(self.groupBox_8)
        self.verticalLayout_3.addWidget(self.groupBoxConfigureTop)
        self.groupBoxConfigureMiddle = QtWidgets.QGroupBox(self.tabConfigure)
        font = QtGui.QFont()
        font.setFamily("Trebuchet MS")
        font.setPointSize(11)
        font.setKerning(True)
        self.groupBoxConfigureMiddle.setFont(font)
        self.groupBoxConfigureMiddle.setAutoFillBackground(False)
        self.groupBoxConfigureMiddle.setStyleSheet("")
        self.groupBoxConfigureMiddle.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBoxConfigureMiddle.setFlat(True)
        self.groupBoxConfigureMiddle.setCheckable(False)
        self.groupBoxConfigureMiddle.setObjectName("groupBoxConfigureMiddle")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.groupBoxConfigureMiddle)
        self.horizontalLayout_11.setContentsMargins(50, 25, 50, 25)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.groupBox_6 = QtWidgets.QGroupBox(self.groupBoxConfigureMiddle)
        self.groupBox_6.setObjectName("groupBox_6")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.groupBox_6)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.lineEditSigmabestguess = QtWidgets.QLineEdit(self.groupBox_6)
        self.lineEditSigmabestguess.setMaximumSize(QtCore.QSize(120, 16777215))
        self.lineEditSigmabestguess.setObjectName("lineEditSigmabestguess")
        self.verticalLayout_8.addWidget(self.lineEditSigmabestguess)
        self.horizontalLayout_11.addWidget(self.groupBox_6)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem)
        self.horizontalLayout_11.setStretch(0, 1)
        self.horizontalLayout_11.setStretch(1, 1)
        self.verticalLayout_3.addWidget(self.groupBoxConfigureMiddle)
        self.groupBoxConfigureBottom = QtWidgets.QGroupBox(self.tabConfigure)
        font = QtGui.QFont()
        font.setFamily("Trebuchet MS")
        font.setPointSize(11)
        font.setKerning(True)
        self.groupBoxConfigureBottom.setFont(font)
        self.groupBoxConfigureBottom.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.groupBoxConfigureBottom.setAutoFillBackground(False)
        self.groupBoxConfigureBottom.setStyleSheet("")
        self.groupBoxConfigureBottom.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBoxConfigureBottom.setFlat(True)
        self.groupBoxConfigureBottom.setCheckable(False)
        self.groupBoxConfigureBottom.setObjectName("groupBoxConfigureBottom")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBoxConfigureBottom)
        self.gridLayout_3.setContentsMargins(50, 25, 50, 25)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBox_5 = QtWidgets.QGroupBox(self.groupBoxConfigureBottom)
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.lineEditDesignprob = QtWidgets.QLineEdit(self.groupBox_5)
        self.lineEditDesignprob.setMaximumSize(QtCore.QSize(120, 16777215))
        self.lineEditDesignprob.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEditDesignprob.setObjectName("lineEditDesignprob")
        self.verticalLayout_6.addWidget(self.lineEditDesignprob)

        self.lineEditDesignprob.editingFinished.connect(self.rexopt)

        self.gridLayout_3.addWidget(self.groupBox_5, 1, 0, 1, 1)
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBoxConfigureBottom)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.lineEditDesignstim = QtWidgets.QLineEdit(self.groupBox_4)
        self.lineEditDesignstim.setMaximumSize(QtCore.QSize(120, 16777215))
        self.lineEditDesignstim.setObjectName("lineEditDesignstim")
        self.verticalLayout_5.addWidget(self.lineEditDesignstim)
        self.gridLayout_3.addWidget(self.groupBox_4, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 0, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem2, 1, 1, 1, 1)
        self.gridLayout_3.setColumnStretch(0, 1)
        self.gridLayout_3.setColumnStretch(1, 1)
        self.verticalLayout_3.addWidget(self.groupBoxConfigureBottom)
        self.tabWidget.addTab(self.tabConfigure, "")

        #Data tab is created
        self.tabData = QtWidgets.QWidget()
        self.tabData.setObjectName("tabData")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.tabData)
        self.horizontalLayout_3.setSpacing(30)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.groupBoxImpExp = QtWidgets.QGroupBox(self.tabData)
        self.groupBoxImpExp.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBoxImpExp.setFlat(True)
        self.groupBoxImpExp.setObjectName("groupBoxImpExp")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.groupBoxImpExp)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_10.addItem(spacerItem3)
        self.label_2 = QtWidgets.QLabel(self.groupBoxImpExp)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_10.addWidget(self.label_2)
        self.pushButtonImport = QtWidgets.QPushButton(self.groupBoxImpExp)
        self.pushButtonImport.setObjectName("pushButtonImport")
        self.verticalLayout_10.addWidget(self.pushButtonImport)

        self.pushButtonImport.clicked.connect(self.f2data)

        self.label_4 = QtWidgets.QLabel(self.groupBoxImpExp)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_10.addItem(spacerItem4)
        self.label_3 = QtWidgets.QLabel(self.groupBoxImpExp)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_10.addWidget(self.label_3)
        self.pushButtonExp = QtWidgets.QPushButton(self.groupBoxImpExp)
        self.pushButtonExp.setObjectName("pushButtonExp")

        self.pushButtonExp.clicked.connect(self.data2f)

        self.verticalLayout_10.addWidget(self.pushButtonExp)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_10.addItem(spacerItem5)
        self.horizontalLayout_3.addWidget(self.groupBoxImpExp)
        self.groupBoxCurrentdata = QtWidgets.QGroupBox(self.tabData)
        self.groupBoxCurrentdata.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBoxCurrentdata.setFlat(True)
        self.groupBoxCurrentdata.setObjectName("groupBoxCurrentdata")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.groupBoxCurrentdata)
        self.verticalLayout_9.setContentsMargins(50, -1, 50, -1)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.plainTextEditCurrentdata = QtWidgets.QPlainTextEdit(self.groupBoxCurrentdata)
        self.plainTextEditCurrentdata.setPlainText("")
        self.plainTextEditCurrentdata.setObjectName("plainTextEditCurrentdata")
        self.verticalLayout_9.addWidget(self.plainTextEditCurrentdata)
        self.horizontalLayout_3.addWidget(self.groupBoxCurrentdata)
        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 2)
        self.tabWidget.addTab(self.tabData, "")

        #Analysis tab is created
        self.tabAnalysis = QtWidgets.QWidget()
        self.tabAnalysis.setObjectName("tabAnalysis")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tabAnalysis)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBoxTop = QtWidgets.QGroupBox(self.tabAnalysis)
        self.groupBoxTop.setFlat(True)
        self.groupBoxTop.setObjectName("groupBoxTop")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.groupBoxTop)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.groupBox_14 = QtWidgets.QGroupBox(self.groupBoxTop)
        self.groupBox_14.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_14.setObjectName("groupBox_14")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBox_14)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.comboBoxModelform = QtWidgets.QComboBox(self.groupBox_14)
        self.comboBoxModelform.setCurrentText("")
        self.comboBoxModelform.setObjectName("comboBoxModelform")
        self.comboBoxModelform.addItem("logit")
        self.comboBoxModelform.addItem("probit")

        self.comboBoxModelform.activated.connect(self.outmodel)

        self.horizontalLayout_4.addWidget(self.comboBoxModelform)
        self.horizontalLayout_6.addWidget(self.groupBox_14)
        self.groupBox_15 = QtWidgets.QGroupBox(self.groupBoxTop)
        self.groupBox_15.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_15.setObjectName("groupBox_15")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.groupBox_15)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.comboBoxDesign = QtWidgets.QComboBox(self.groupBox_15)
        self.comboBoxDesign.setFrame(False)
        self.comboBoxDesign.setModelColumn(0)
        self.comboBoxDesign.setObjectName("comboBoxDesign")
        self.comboBoxDesign.addItem("c optimal")
        self.comboBoxDesign.addItem("d optimal")
        self.comboBoxDesign.addItem("sigma optimal")

        self.comboBoxDesign.activated.connect(self.outdesign)

        self.horizontalLayout_5.addWidget(self.comboBoxDesign)
        self.horizontalLayout_6.addWidget(self.groupBox_15)
        self.groupBox_16 = QtWidgets.QGroupBox(self.groupBoxTop)
        self.groupBox_16.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_16.setObjectName("groupBox_16")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.groupBox_16)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.frame_4 = QtWidgets.QFrame(self.groupBox_16)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.checkBoxBiasreduction = QtWidgets.QCheckBox(self.frame_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBoxBiasreduction.sizePolicy().hasHeightForWidth())
        self.checkBoxBiasreduction.setSizePolicy(sizePolicy)
        self.checkBoxBiasreduction.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.checkBoxBiasreduction.setText("")
        self.checkBoxBiasreduction.setIconSize(QtCore.QSize(50, 50))
        self.checkBoxBiasreduction.setCheckable(True)
        self.checkBoxBiasreduction.setTristate(False)
        self.checkBoxBiasreduction.setObjectName("checkBoxBiasreduction")
        self.horizontalLayout_14.addWidget(self.checkBoxBiasreduction)

        self.checkBoxBiasreduction.stateChanged.connect(self.resuggest)

        self.horizontalLayout_10.addWidget(self.frame_4)
        self.horizontalLayout_6.addWidget(self.groupBox_16)
        self.verticalLayout.addWidget(self.groupBoxTop)
        self.groupBoxMiddle = QtWidgets.QGroupBox(self.tabAnalysis)
        self.groupBoxMiddle.setFlat(True)
        self.groupBoxMiddle.setObjectName("groupBoxMiddle")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBoxMiddle)
        self.gridLayout.setObjectName("gridLayout")
        self.labelPassfailholder = QtWidgets.QLabel(self.groupBoxMiddle)
        self.labelPassfailholder.setAlignment(QtCore.Qt.AlignCenter)
        self.labelPassfailholder.setObjectName("labelPassfailholder")
        self.gridLayout.addWidget(self.labelPassfailholder, 1, 1, 1, 3)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem6, 0, 0, 1, 1)
        self.groupBox_17 = QtWidgets.QGroupBox(self.groupBoxMiddle)
        self.groupBox_17.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_17.setObjectName("groupBox_17")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.groupBox_17)
        self.horizontalLayout_9.setContentsMargins(20, -1, 20, -1)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.lineEditSuggestedstimulus = QtWidgets.QLineEdit(self.groupBox_17)
        self.lineEditSuggestedstimulus.setObjectName("lineEditSuggestedstimulus")
        self.horizontalLayout_9.addWidget(self.lineEditSuggestedstimulus)
        self.gridLayout.addWidget(self.groupBox_17, 0, 1, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem7, 0, 2, 1, 1)
        self.groupBox_18 = QtWidgets.QGroupBox(self.groupBoxMiddle)
        self.groupBox_18.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_18.setObjectName("groupBox_18")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.groupBox_18)
        self.horizontalLayout_8.setContentsMargins(20, -1, 20, -1)
        self.horizontalLayout_8.setSpacing(10)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.pushButtonSuccess = QtWidgets.QPushButton(self.groupBox_18)
        self.pushButtonSuccess.setObjectName("pushButtonSuccess")
        self.horizontalLayout_8.addWidget(self.pushButtonSuccess)

        self.pushButtonSuccess.clicked.connect(self.addsuccess)

        self.pushButtonFailure = QtWidgets.QPushButton(self.groupBox_18)
        self.pushButtonFailure.setObjectName("pushButtonFailure")
        self.horizontalLayout_8.addWidget(self.pushButtonFailure)

        self.pushButtonFailure.clicked.connect(self.addfailure)

        self.gridLayout.addWidget(self.groupBox_18, 0, 3, 1, 1)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem8, 0, 4, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 3)
        self.gridLayout.setColumnStretch(2, 1)
        self.gridLayout.setColumnStretch(3, 3)
        self.gridLayout.setColumnStretch(4, 1)
        self.verticalLayout.addWidget(self.groupBoxMiddle)
        self.groupBoxBottom = QtWidgets.QGroupBox(self.tabAnalysis)
        self.groupBoxBottom.setFlat(True)
        self.groupBoxBottom.setObjectName("groupBoxBottom")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.groupBoxBottom)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")

        self.pushButtonCalculate = QtWidgets.QPushButton(self.groupBoxBottom)
        self.pushButtonCalculate.setObjectName("pushButtonCalculate")
        self.horizontalLayout_7.addWidget(self.pushButtonCalculate)

        self.pushButtonCalculate.clicked.connect(self.getclevels)
        self.tabWidget.currentChanged.connect(self.changeTabFocus)

        self.frame = QtWidgets.QFrame(self.groupBoxBottom)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_11.setContentsMargins(50, -1, -1, -1)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.label_7 = QtWidgets.QLabel(self.frame)
        self.label_7.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_11.addWidget(self.label_7)
        self.label_8 = QtWidgets.QLabel(self.frame)
        self.label_8.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_11.addWidget(self.label_8)
        self.label_9 = QtWidgets.QLabel(self.frame)
        self.label_9.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_11.addWidget(self.label_9)
        self.horizontalLayout_7.addWidget(self.frame)
        self.verticalLayout.addWidget(self.groupBoxBottom)
        self.tabWidget.addTab(self.tabAnalysis, "")

        #Plot tab is created
        self.tabPlot = QtWidgets.QWidget()
        self.tabPlot.setObjectName("tabPlot")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.tabPlot)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.frameLeft = QtWidgets.QFrame(self.tabPlot)
        self.frameLeft.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameLeft.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameLeft.setObjectName("frameLeft")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frameLeft)
        self.verticalLayout_2.setContentsMargins(-1, 10, -1, 10)
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox_19 = QtWidgets.QGroupBox(self.frameLeft)
        self.groupBox_19.setObjectName("groupBox_19")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_19)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.checkBoxMlmodelslogit = QtWidgets.QCheckBox(self.groupBox_19)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.checkBoxMlmodelslogit.setFont(font)
        self.checkBoxMlmodelslogit.setObjectName("checkBoxMlmodelslogit")
        self.verticalLayout_4.addWidget(self.checkBoxMlmodelslogit)
        self.checkBoxMlmodelsprobit = QtWidgets.QCheckBox(self.groupBox_19)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.checkBoxMlmodelsprobit.setFont(font)
        self.checkBoxMlmodelsprobit.setObjectName("checkBoxMlmodelsprobit")
        self.verticalLayout_4.addWidget(self.checkBoxMlmodelsprobit)
        self.verticalLayout_2.addWidget(self.groupBox_19)
        self.groupBox_20 = QtWidgets.QGroupBox(self.frameLeft)
        self.groupBox_20.setObjectName("groupBox_20")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.groupBox_20)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.checkBoxLessbiasedlogit = QtWidgets.QCheckBox(self.groupBox_20)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.checkBoxLessbiasedlogit.setFont(font)
        self.checkBoxLessbiasedlogit.setObjectName("checkBoxLessbiasedlogit")
        self.verticalLayout_14.addWidget(self.checkBoxLessbiasedlogit)
        self.checkBoxLessbiasedprobit = QtWidgets.QCheckBox(self.groupBox_20)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.checkBoxLessbiasedprobit.setFont(font)
        self.checkBoxLessbiasedprobit.setObjectName("checkBoxLessbiasedprobit")
        self.verticalLayout_14.addWidget(self.checkBoxLessbiasedprobit)
        self.verticalLayout_2.addWidget(self.groupBox_20)
        self.groupBox_21 = QtWidgets.QGroupBox(self.frameLeft)
        self.groupBox_21.setObjectName("groupBox_21")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.groupBox_21)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.checkBoxShowmargin = QtWidgets.QCheckBox(self.groupBox_21)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.checkBoxShowmargin.setFont(font)
        self.checkBoxShowmargin.setObjectName("checkBoxShowmargin")
        self.verticalLayout_13.addWidget(self.checkBoxShowmargin)
        self.checkBoxFreezeaxes = QtWidgets.QCheckBox(self.groupBox_21)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.checkBoxFreezeaxes.setFont(font)
        self.checkBoxFreezeaxes.setObjectName("checkBoxFreezeaxes")
        self.verticalLayout_13.addWidget(self.checkBoxFreezeaxes)
        self.checkBoxWritevalues = QtWidgets.QCheckBox(self.groupBox_21)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.checkBoxWritevalues.setFont(font)
        self.checkBoxWritevalues.setObjectName("checkBoxWritevalues")
        self.verticalLayout_13.addWidget(self.checkBoxWritevalues)
        self.verticalLayout_2.addWidget(self.groupBox_21)
        self.groupBox_22 = QtWidgets.QGroupBox(self.frameLeft)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.groupBox_22.setFont(font)
        self.groupBox_22.setObjectName("groupBox_22")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.groupBox_22)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.label_11 = QtWidgets.QLabel(self.groupBox_22)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.verticalLayout_12.addWidget(self.label_11)
        self.lineEditXaxislabel = QtWidgets.QLineEdit(self.groupBox_22)
        self.lineEditXaxislabel.setObjectName("lineEditXaxislabel")
        self.verticalLayout_12.addWidget(self.lineEditXaxislabel)
        self.label_10 = QtWidgets.QLabel(self.groupBox_22)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_12.addWidget(self.label_10)
        self.lineEditYaxislabel = QtWidgets.QLineEdit(self.groupBox_22)
        self.lineEditYaxislabel.setObjectName("lineEditYaxislabel")
        self.verticalLayout_12.addWidget(self.lineEditYaxislabel)
        self.verticalLayout_2.addWidget(self.groupBox_22)
        self.pushButtonRefresh = QtWidgets.QPushButton(self.frameLeft)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pushButtonRefresh.setFont(font)
        self.pushButtonRefresh.setObjectName("pushButtonRefresh")
        self.verticalLayout_2.addWidget(self.pushButtonRefresh)

        self.pushButtonRefresh.clicked.connect(self.freshplot)

        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 1)
        self.verticalLayout_2.setStretch(2, 1)
        self.verticalLayout_2.setStretch(3, 1)
        self.verticalLayout_2.setStretch(4, 1)
        self.horizontalLayout_12.addWidget(self.frameLeft)
        ##Matplotlib
        self.widgetPlotholder = QtWidgets.QWidget(self.tabPlot)
        self.widgetPlotholder.setObjectName("widgetPlotholder")
        self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        self.sc.axes.plot([0,1,2,3,4],[10,1,20,3,40] )
        ##Create toolbar, passing canvas as first parameter parent (self, the MainWindow) as second
        toolbar = NavigationToolbar(self.sc, MainWindow)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.sc)
        ##Create a placeholder widget to hold the toolbar and canvas
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.horizontalLayout_12.addWidget(widget)
        ##Matplotlib end
        self.horizontalLayout_12.setStretch(0, 1)
        self.horizontalLayout_12.setStretch(1, 3)
        self.tabWidget.addTab(self.tabPlot, "")

        #Navbar and tabwidget are added to MainWindow
        self.horizontalLayout_2.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def updatevariableDict(self):
        try:
            self.variableDict['muBest'] = float(self.lineEditMubestguess.text())
        except:
            MainWindow.statusBar().showMessage('Cannot calculate: Mu Best Guess is empty') 
            return False         
        try:
            self.variableDict['muMax'] = float(self.lineEditMumaxguess.text())
        except:
            MainWindow.statusBar().showMessage('Cannot calculate: Mu Max Guess is empty') 
            return False   
        try:
            self.variableDict['muMin'] = float(self.lineEditMuminguess.text())
        except:
            MainWindow.statusBar().showMessage('Cannot calculate: Mu Min Guess is empty') 
            return False
        try:
            self.variableDict['muPrec'] = float(self.lineEditMuprecision.text())
        except:
            MainWindow.statusBar().showMessage('Cannot calculate: Mu Precision is empty') 
            return False         
        try:
            self.variableDict['sigmaBest'] = float(self.lineEditSigmabestguess.text())
        except:
            MainWindow.statusBar().showMessage('Cannot calculate: Sigma Best Guess is empty') 
            return False   
        try:
            self.variableDict['designStim'] = float(self.lineEditDesignstim.text())
        except:
            MainWindow.statusBar().showMessage('Cannot calculate: Design Stimulus is empty') 
            return False  
        try:
            self.rexopt()
            self.variableDict['designProb'] = float(self.lineEditDesignprob.text())
        except:
            MainWindow.statusBar().showMessage('Cannot calculate: Design Probability is empty') 
            return False
        #TODO make sure user can remove suggestionStimulus then tries to add/fail. This is allowed to be blank        
        # try:
        #     self.variableDict['suggestionStimulus'] = float(self.lineEditSuggestedstimulus.text())
        # except:
        #     MainWindow.statusBar().showMessage('Cannot calculate: Suggested Stimulus is empty') 
        #     return False   
  
        self.variableDict['experimentModel'] = float(self.comboBoxModelform.currentIndex())
        self.variableDict['experimentDesign'] = float(self.comboBoxDesign.currentIndex())
        self.variableDict['experimentBias'] = bool(self.checkBoxBiasreduction.isChecked())
        return True

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "trueSIG"))
        self.groupBoxConfigureTop.setTitle(_translate("MainWindow", "MU - 50% threshhold parameter"))
        self.label_6.setText(_translate("MainWindow", "Max Guess"))
        self.label_12.setToolTip(_translate("MainWindow", "tooool"))
        self.label_12.setStatusTip(_translate("MainWindow", "hello there"))
        self.label_12.setText(_translate("MainWindow", "Best Guess"))
        self.label_5.setText(_translate("MainWindow", "Min Guess"))
        self.label.setText(_translate("MainWindow", "Precision - # of digits after the decimal"))
        self.groupBoxConfigureMiddle.setTitle(_translate("MainWindow", "SIGMA - length scale parameter"))
        self.groupBox_6.setTitle(_translate("MainWindow", "Best Guess"))
        self.groupBoxConfigureBottom.setTitle(_translate("MainWindow", "TEST - design specifications"))
        self.groupBox_5.setTitle(_translate("MainWindow", "% design probability"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Design stimulus"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabConfigure), _translate("MainWindow", "Configure"))
        self.groupBoxImpExp.setTitle(_translate("MainWindow", "Import/Export Data"))
        self.label_2.setText(_translate("MainWindow", "Get data from file"))
        self.pushButtonImport.setText(_translate("MainWindow", "Import"))
        self.label_4.setText(_translate("MainWindow", "[Caution: Overwrites Data]"))
        self.label_3.setText(_translate("MainWindow", "Write data to file"))
        self.pushButtonExp.setText(_translate("MainWindow", "Export"))
        self.groupBoxCurrentdata.setTitle(_translate("MainWindow", "Current Data"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabData), _translate("MainWindow", "Data"))
        self.groupBoxTop.setTitle(_translate("MainWindow", "Experimental design parameters"))
        self.groupBox_14.setTitle(_translate("MainWindow", "Model Form"))
        self.groupBox_15.setTitle(_translate("MainWindow", "Design"))
        self.groupBox_16.setTitle(_translate("MainWindow", "Bias Reduction"))
        self.groupBoxMiddle.setTitle(_translate("MainWindow", "Suggestion for next stimulus"))
        self.labelPassfailholder.setText(_translate("MainWindow", ""))
        self.groupBox_17.setTitle(_translate("MainWindow", "Suggested stimulus"))
        self.groupBox_18.setTitle(_translate("MainWindow", "Add to data"))
        self.pushButtonSuccess.setText(_translate("MainWindow", "Success"))
        self.pushButtonFailure.setText(_translate("MainWindow", "Failure"))
        self.groupBoxBottom.setTitle(_translate("MainWindow", "Confidence in design probability at design stimulus"))
        self.pushButtonCalculate.setText(_translate("MainWindow", "Calculate"))
        self.label_7.setText(_translate("MainWindow", "xx.xx% asymptotic confidence level, likely too optimistic"))
        self.label_8.setText(_translate("MainWindow", "xx.xx% confidence using observed likelihood"))
        self.label_9.setText(_translate("MainWindow", "Using stimulus of x and probability of xx.xx%"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabAnalysis), _translate("MainWindow", "Analysis"))
        self.groupBox_19.setTitle(_translate("MainWindow", "ML models"))
        self.checkBoxMlmodelslogit.setText(_translate("MainWindow", "logit"))
        self.checkBoxMlmodelsprobit.setText(_translate("MainWindow", "probit"))
        self.groupBox_20.setTitle(_translate("MainWindow", "Less biased models"))
        self.checkBoxLessbiasedlogit.setText(_translate("MainWindow", "logit"))
        self.checkBoxLessbiasedprobit.setText(_translate("MainWindow", "probit"))
        self.groupBox_21.setTitle(_translate("MainWindow", "Plot options"))
        self.checkBoxShowmargin.setText(_translate("MainWindow", "show margin"))
        self.checkBoxFreezeaxes.setText(_translate("MainWindow", "freeze axes"))
        self.checkBoxWritevalues.setText(_translate("MainWindow", "write values"))
        self.groupBox_22.setTitle(_translate("MainWindow", "Labels"))
        self.label_11.setText(_translate("MainWindow", "x-axis"))
        self.label_10.setText(_translate("MainWindow", "y-axis"))
        self.pushButtonRefresh.setText(_translate("MainWindow", "Refresh"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabPlot), _translate("MainWindow", "Plot"))

    def changeTabFocus(self):
        prevIndex = self.previousTab
        currentIndex = self.tabWidget.currentIndex()
             
        # Lost focus
        if prevIndex == 0: self.getdconf()
        if prevIndex == 1: pass
        if prevIndex == 2: pass
        if prevIndex == 3: pass
        
        # Gained focus
        if currentIndex == 0: self.setconf()
        if currentIndex == 1: pass
        if currentIndex == 2: self.suggestion()
        if currentIndex == 3: pass

        self.previousTab = self.tabWidget.currentIndex()

    def initialImport(self, MainWindow):
        #TODO fix font scaling
        try:
            print("trying to load")
            finput=open("tsconfig.txt","r")
            lines=finput.readlines()
            finput.close()
            print("trying to load - reading over imported text")
            for aline in lines:
                print("1")
                vals=aline.split()
                print(vals)
                if vals[0][0] != '#':
                    print("2")
                    if vals[0].find("muguess") > -1:
                        print("inmuguess")
                        self.lineEditMubestguess.setText(vals[1].strip())
                    if vals[0].find("mugmin") > -1:
                        print("inmumin")
                        self.lineEditMuminguess.setText(vals[1].strip())
                    if vals[0].find("mugmax") > -1:
                        self.lineEditMumaxguess.setText(vals[1].strip())
                    if vals[0].find("precision") > -1:
                        self.lineEditMuprecision.setText(vals[1].strip()) 
                    if vals[0].find("sigmaguess") > -1:
                        self.lineEditSigmabestguess.setText(vals[1].strip())
                    if vals[0].find("designstim") > -1:
                        self.lineEditDesignstim.setText(vals[1].strip())
                    if vals[0].find("designprob") > -1:
                        self.lineEditDesignprob.setText(vals[1].strip())
                    if vals[0].find("datafile") > -1:
                        fname=(vals[1].strip())
                        self.f2fdata(fname)
                    if vals[0].find("modelform") > -1:
                        self.comboBoxModelform.setCurrentText(vals[1].strip())
                    if vals[0].find("reducebias") > -1:
                        self.checkBoxBiasreduction.setChecked(int(vals[1].strip())) 
                    if vals[0].find("nclint") > -1:
                        itest=int(vals[1].strip())
                        if itest < 2: itest=2
                        thistest.nint=itest
                    if vals[0].find("designmatrix") > -1:
                        if (vals[1].strip())[0]=='c':
                            self.comboBoxDesign.setCurrentText("c optimal")
                        elif (vals[1].strip())[0]=='d':
                            self.comboBoxDesign.setCurrentText("d optimal")
                        elif (vals[1].strip())[0]=='s':
                            self.comboBoxDesign.setCurrentText("sigma optimal")
                    # if vals[0].find("fontsize") > -1:
                    #     font.nametofont('TkDefaultFont').configure(size=vals[1].strip())
                    if vals[0].find("guisize") > -1:
                        size=vals[1].strip().split('x')
                        MainWindow.resize(int(size[0]), int(size[1]))
                    if vals[0].find("debug") > -1:
                        thistest.debug=int(vals[1].strip())
        except:
            pass

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.initialImport(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

