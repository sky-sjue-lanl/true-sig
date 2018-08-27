#!/usr/bin/python
try:
  from Tkinter import *
  import ttk
  import tkFont as font
  from ScrolledText import ScrolledText
  import tkFileDialog as getfile
except ImportError:
  from tkinter import *
  from tkinter import ttk
  import tkinter.font as font
  from tkinter.scrolledtext import ScrolledText
  from tkinter import filedialog as getfile
import matplotlib as mpl
import numpy as np
mpl.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

from testclass import *

thistest=dettest()

main=Tk()
main.title("trueSIG")
main.geometry("800x550")
style=ttk.Style()
style.configure('TNotebook.Tab', padding=(20,8,20,0))
font.nametofont('TkDefaultFont').configure(size=12)

rows=0
while rows < 50:
  main.rowconfigure(rows, weight=1)
  main.columnconfigure(rows, weight=1)
  rows+=1

nb=ttk.Notebook(main)
nb.grid(row=1, column=0, columnspan=50, rowspan=49, sticky="NESW")

page1=ttk.Frame(nb)
nb.add(page1, text="Configure   ")
p1l0a=ttk.Label(page1, text="       ")
p1l0a.grid(row=0, column=0, columnspan=7, sticky="NESW")
p1l0aa=ttk.Label(page1, text="       ")
p1l0aa.grid(row=1, column=0, columnspan=7, sticky="NESW")

#mu configuration
p1l1=ttk.Label(page1, text="MU - 50% threshold parameter  ")
p1l1.grid(row=2, column=3, columnspan=4, sticky="W")
p1l0b=ttk.Label(page1, text="       ")
p1l0b.grid(row=3, column=0, columnspan=7, sticky="NESW")

muguess=StringVar()
mumax=StringVar()
mumin=StringVar()
p1r3t=ttk.Label(page1, text="          ")
p1r3t.grid(row=4, column=0, sticky="W")
p1e0=ttk.Entry(page1, width=8, textvariable=muguess)
p1e0.grid(row=4, column=1, sticky="W")
p1l2=ttk.Label(page1, text=" best guess     ")
p1l2.grid(row=4, column=2, sticky="W")
p1e1=ttk.Entry(page1, width=8, textvariable=mumin)
p1e1.grid(row=4, column=3, sticky="W")
p1l3=ttk.Label(page1, text=" min guess      ")
p1l3.grid(row=4, column=4, sticky="W")
p1e2=ttk.Entry(page1, width=8, textvariable=mumax)
p1e2.grid(row=4, column=5, sticky="W")
p1l4=ttk.Label(page1, text=" max guess      ")
p1l4.grid(row=4, column=6, sticky="W")

p1l0c=ttk.Label(page1, text="       ")
p1l0c.grid(row=5, column=1, columnspan=7, sticky="NESW")

mufuzz=StringVar()
p1r5t=ttk.Label(page1, text="          ")
p1r5t.grid(row=6, column=0, sticky="W")
p1e3=ttk.Entry(page1, width=8, textvariable=mufuzz)
mufuzz.set(int(log10(1.0/thistest.mufuzz)))
p1e3.grid(row=6, column=1, sticky="W")
p1l5=ttk.Label(page1, text=" precision - # of digits to keep after decimal")
p1l5.grid(row=6, column=2, columnspan=5, sticky="W")

p1l0d=ttk.Label(page1, text="       ")
p1l0d.grid(row=7, column=3, columnspan=7, sticky="NESW")
p1l0e=ttk.Label(page1, text="       ")
p1l0e.grid(row=8, column=4, columnspan=7, sticky="NESW")

#sigma configuration
p1l6=ttk.Label(page1, text="SIGMA - length scale parameter")
p1l6.grid(row=9, column=3, columnspan=4, sticky="W")

p1l0f=ttk.Label(page1, text="       ")
p1l0f.grid(row=10, column=0, columnspan=7, sticky="NESW")

sguess=StringVar()
p1r10t=ttk.Label(page1, text="          ")
p1r10t.grid(row=11, column=0, sticky="W")
p1e4=ttk.Entry(page1, width=8, textvariable=sguess)
p1e4.grid(row=11, column=1, sticky="W")
p1l7=ttk.Label(page1, text=" best guess     ")
p1l7.grid(row=11, column=2, sticky="W")

p1l0g=ttk.Label(page1, text="       ")
p1l0g.grid(row=12, column=0, columnspan=7, sticky="NESW")
p1l0h=ttk.Label(page1, text="       ")
p1l0h.grid(row=13, column=0, columnspan=7, sticky="NESW")

#design parameters
p1l8=ttk.Label(page1, text="TEST - design specifications")
p1l8.grid(row=14, column=3, columnspan=4, sticky="W")

dstimulus=StringVar()
dprob=StringVar()
p1l0i=ttk.Label(page1, text="       ")
p1l0i.grid(row=15, column=0, columnspan=7, sticky="NESW")
p1r15t=ttk.Label(page1, text="          ")
p1r15t.grid(row=16, column=0, sticky="W")
p1e5=ttk.Entry(page1, width=8, textvariable=dstimulus)
p1e5.grid(row=16, column=1, sticky="W")
p1l9=ttk.Label(page1, text=" design stimulus")
p1l9.grid(row=16, column=2, sticky="W")
p1l0j=ttk.Label(page1, text="       ")
p1l0j.grid(row=17, column=0, columnspan=7, sticky="NESW")
p1r17t=ttk.Label(page1, text="          ")
p1r17t.grid(row=18, column=0, sticky="W")
p1e6=ttk.Entry(page1, width=8, textvariable=dprob)
dprob.set(str(thistest.dprob))
p1e6.grid(row=18, column=1, sticky="W")
p1l10=ttk.Label(page1, text="% design probability")
p1l10.grid(row=18, column=2, sticky="W")
p1l11=ttk.Label(page1, text="")
p1l11.grid(row=19, column=1, columnspan=5, sticky="W")
dprobwarn=StringVar()
dprobwarn.set("")
p1l12=ttk.Label(page1, textvariable=dprobwarn)
p1l12.grid(row=20, column=1, columnspan=5, sticky="W")

#tslogo=PhotoImage(file="tslogo.gif")
#p1l13=ttk.Label(page1, image=tslogo)
#p1l13.grid(row=21, column=0, columnspan=6, sticky="W")

def rexopt(event):
 try: ptest=float(dprob.get())
 except: ptest=1.0
 if ptest > 50.0 and ptest < 100.0:
  thistest.dprob=ptest
  dprobwarn.set("")
 else: 
  thistest.dprob=99.9
  dprob.set("99.9")
  dprobwarn.set("DESIGN PROBABILITY MUST BE BETWEEN 50 and 100%")
 thistest.tval()

p1e6.bind('<FocusOut>',rexopt)

#0 muguess, 1 mumax, 2 mumin, 3 mufuzz, 4 sguess, 5 dstimulus, 6 dprob
lconfig=[0,0,0,1,1,0,0]

def getconf():
 while 10.0**(-float(mufuzz.get())) > float(sguess.get())/5.0:
  mufuzz.set(str(int(mufuzz.get())+1))
 try: lconfig[0]=float(muguess.get())
 except: lconfig[0]=0.0
 try: lconfig[1]=float(mumax.get())
 except: lconfig[1]=0.0
 try: lconfig[2]=float(mumin.get())
 except: lconfig[2]=0.0
 try: lconfig[3]=float(mufuzz.get())
 except: lconfig[3]=0.0
 try: lconfig[4]=float(sguess.get())
 except: lconfig[4]=0.0
 try: lconfig[5]=float(dstimulus.get())
 except: lconfig[5]=0.0
 try: lconfig[6]=float(dprob.get())
 except: lconfig[6]=0.0
 thistest.list2design(lconfig)

def getdconf(event):
 getconf()

def setconf(event):
 blah="{:."+mufuzz.get()+"f}"
 aguess=blah.format(thistest.sguess)
 sguess.set(aguess)

page1.bind('<FocusOut>',getdconf)

page1.bind('<FocusIn>',setconf)

#TAB WITH READING/WRITING/EDITING DATA CAPABILITIES
page2=ttk.Frame(nb)
nb.add(page2, text="   Data     ")

p2l2=ttk.Label(page2, text="                                           ")
p2l2.grid(row=0, column=0, columnspan=2, sticky=W)

p2l1=ttk.Label(page2, text="[Import data, add data points, export data]")
p2l1.grid(row=1, column=0, columnspan=2, sticky=W)

p2l2=ttk.Label(page2, text="                                           ")
p2l2.grid(row=2, column=0, columnspan=2, sticky=W)

p2l3=ttk.Label(page2, text="Current data")
p2l3.grid(row=3, column=1, sticky=W)
databox=ScrolledText(page2, width=40, height=22)
databox.grid(row=4, column=1, sticky=W)

def f2data():
 fname=getfile.askopenfilename(initialdir="./", title="Select file")
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
  databox.delete(1.0, END)
  databox.insert(INSERT, astring)

def f2fdata(fname):
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
  databox.delete(1.0, END)
  databox.insert(INSERT, astring)

p2b1=ttk.Button(page2, text="Get data from file", command=f2data)
p2b1.grid(row=3, column=0, sticky=W)
p2l4=ttk.Label(page2, text="[Caution: overwrites data]    ")
p2l4.grid(row=4, column=0, sticky=NW)

def data2f():
 fname=getfile.asksaveasfilename(initialdir="./", title="Choose filename")
 if str(fname) != "()":
  fout=open(fname,"w")
  dtext=databox.get(1.0,END)
  fout.write(dtext)
  fout.close()

p2b2=ttk.Button(page2, text="Write data to file", command=data2f)
p2b2.grid(row=5, column=1, sticky=W)

def mkdataobj():
 """turn text box data from page2 into organized data in object thisclass"""
 dtext=databox.get(1.0,END) 
 thistest.text2data(dtext)

#PAGE 3 DESIGN INFO AND ANALYSIS
modelval=StringVar()
designval=StringVar()
ibias=IntVar()
ibias.set(1)
stimval=StringVar()
clevela=StringVar()
clevelub=StringVar()
clevela.set("xx.xx%")
clevelub.set("xx.xx%")
datacomment=StringVar()
expconf=StringVar()
expconf.set("")

def suggestion(event):
 getconf()
 mkdataobj()
 thesug=thistest.nextpoint()
 blah="{:."+mufuzz.get()+"f}"
 testsug=blah.format(thesug)
 stimval.set(str(testsug)) 

def resuggest():
 mkdataobj()
 thistest.reducebias=ibias.get()
 thesug=thistest.nextpoint()
 blah="{:."+mufuzz.get()+"f}"
 testsug=blah.format(thesug)
 stimval.set(str(testsug)) 

def outmodel(event):
 thistest.model=(modelval.get()).strip()
 thistest.tval()
 resuggest()

def outdesign(event):
 teststring=(designval.get()).strip()
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
  resuggest()

def getclevels():
 c1=thistest.cltcl()
 c1=0.01*int(c1/0.0001)
 c2=thistest.lklhdcl()
 c2=0.01*int(c2/0.0001)
 c1s="{:5.2f}".format(c1)
 c2s="{:5.2f}".format(c2)
 clevela.set(c1s+"%") 
 clevelub.set(c2s+"%")
 expconf.set("Using stimulus of "+dstimulus.get()+" and probability "+\
             dprob.get()+"%.")

page3=ttk.Frame(nb)
nb.add(page3, text="Analysis    ")
p3l0=ttk.Label(page3, text="   ")
p3l0.grid(row=0, column=0, columnspan=6)
p3l1=ttk.Label(page3, text="   ")
p3l1.grid(row=1, column=0, columnspan=6)
p3l2=ttk.Label(page3, text="Experimental design parameters")
p3l2.grid(row=2, column=0, columnspan=6)
p3l1b=ttk.Label(page3, text="   ")
p3l1b.grid(row=3, column=0, columnspan=6)
p3l3=ttk.Label(page3, text=" Model form: ")
p3l3.grid(row=4, column=0, sticky="E")
modelforms=["logit  ", "probit"]
p3om1=ttk.OptionMenu(page3, modelval, modelforms[0], *modelforms, \
                     command=outmodel)
p3om1.grid(row=4, column=1)
p3l4=ttk.Label(page3, text="  design: ")
p3l4.grid(row=4, column=2, sticky="E")
ourdesigns=["c optimal      ",\
            "sigma optimal",\
            "d optimal      "]
p3om2=ttk.OptionMenu(page3, designval, ourdesigns[0], *ourdesigns, \
                     command=outdesign)
p3om2.grid(row=4, column=3, columnspan=2, sticky="W")
p3bcb=ttk.Checkbutton(page3, text=" use bias reduction", \
                      variable=ibias, command=resuggest)
p3bcb.grid(row=4, column=5)

p3l6=ttk.Label(page3, text="  ")
p3l6.grid(row=6, column=0, columnspan=6)
p3l7=ttk.Label(page3, text="  ")
p3l7.grid(row=7, column=0, columnspan=6)
p3l8=ttk.Label(page3, text="Suggestion for next stimulus (depends on design parameters)")
p3l8.grid(row=8, column=0, columnspan=6)
p3l9=ttk.Label(page3, text="  ")
p3l9.grid(row=9, column=0, columnspan=6)
p3l10=ttk.Label(page3, text=" Suggested stimulus: ")
p3l10.grid(row=10, column=0)
stimval.set("")
p3e1=ttk.Entry(page3, width=10, textvariable=stimval)
p3e1.grid(row=10, column=1, sticky="W")
p3l11=ttk.Label(page3, text="Add to data: ")
p3l11.grid(row=10, column=2, sticky="E")

def add2data(afloat):
 thestim=stimval.get()
 datastring=thestim+"  "+str(afloat)+"\n"
 datatext=databox.get(1.0,END)
 dlines=datatext.split('\n')
 newdatastring=""
 for aline in dlines:
  if len(aline) > 0:
   newdatastring+=aline
   newdatastring+="\n"
 newdatastring+=datastring
 databox.delete(1.0, END)
 databox.insert(INSERT, newdatastring)

def addsuccess():
 add2data(1.0)
 datacomment.set("added success at "+stimval.get())
 resuggest()

def addfailure():
 add2data(0.0)
 datacomment.set("added failure at "+stimval.get())
 resuggest()

p3btn1=ttk.Button(page3, text="success", command=addsuccess)
p3btn1.grid(row=10, column=3, sticky="W")
p3btn2=ttk.Button(page3, text="failure", command=addfailure)
p3btn2.grid(row=10, column=4, sticky="W")

p3l12=ttk.Label(page3, text="  ")
p3l12.grid(row=11, column=1, columnspan=5, sticky="W")
p3l13=ttk.Label(page3, textvariable=datacomment)
p3l13.grid(row=12, column=0, columnspan=6)

p3l14=ttk.Label(page3, text="  ")
p3l14.grid(row=13, column=0, columnspan=6)
p3l15=ttk.Label(page3, text="  ")
p3l15.grid(row=14, column=0, columnspan=6)

p3l16=ttk.Label(page3, text=\
                "Confidence in design probability at design stimulus")
p3l16.grid(row=15, column=0, columnspan=6)
p3l17=ttk.Label(page3, text="  ")
p3l17.grid(row=16, column=0, columnspan=6)
p3l17=ttk.Label(page3, text="  ")
p3l17.grid(row=17, column=0, columnspan=6)

p3btn3=ttk.Button(page3, text="calculate", command=getclevels)
p3btn3.grid(row=18, column=0, sticky="E")
p3l20=ttk.Label(page3, textvariable=clevela)
p3l20.grid(row=18, column=1, sticky="E")
p3l21=ttk.Label(page3, text=" asymptotic confidence level, likely too optimistic")
p3l21.grid(row=18, column=2, columnspan=4, sticky="W")
p3l22=ttk.Label(page3, text="  ")
p3l22.grid(row=19, column=0, columnspan=6)
p3l23=ttk.Label(page3, textvariable=clevelub)
p3l23.grid(row=20, column=1, sticky="E")
p3l24=ttk.Label(page3, text=" confidence using observed likelihood")
p3l24.grid(row=20, column=2, columnspan=4, sticky="W")
p3l25=ttk.Label(page3, text="")
p3l25.grid(row=21, column=0, columnspan=6)
p3l26=ttk.Label(page3, textvariable=expconf)
p3l26.grid(row=22, column=0, columnspan=6)

page3.bind('<FocusIn>',suggestion)

#PAGE 4
#GENERATE PLOTS HERE
page4=ttk.Frame(nb)
nb.add(page4, text="Plotting    ")
p4f0=ttk.Frame(master=page4)
p4f0.pack(side=LEFT, fill=BOTH, expand=0)
p4lm1=ttk.Label(p4f0, text="          ")
p4lm1.pack(side=TOP)
p4l0=ttk.Label(p4f0, text="ML models   ")
p4l0.pack(side=TOP)
iplotlog=IntVar()
p4cb1=ttk.Checkbutton(p4f0, text="logit", variable=iplotlog)
p4cb1.pack(side=TOP, anchor=W)
iplotprob=IntVar()
p4cb2=ttk.Checkbutton(p4f0, text="probit", variable=iplotprob)
p4cb2.pack(side=TOP, anchor=W)
p4l1=ttk.Label(p4f0, text="          ")
p4l1.pack(side=TOP)
p4l2=ttk.Label(p4f0, text="Less biased models")
p4l2.pack(side=TOP)
iplotbrlog=IntVar()
p4cb3=ttk.Checkbutton(p4f0, text="logit", variable=iplotbrlog)
p4cb3.pack(side=TOP, anchor=W)
iplotbrprob=IntVar()
p4cb4=ttk.Checkbutton(p4f0, text="probit", variable=iplotbrprob)
p4cb4.pack(side=TOP, anchor=W)
p4l3=ttk.Label(p4f0, text="          ")
p4l3.pack(side=TOP)
p4l4=ttk.Label(p4f0, text="Plot options")
p4l4.pack(side=TOP)
p4l5=ttk.Label(p4f0, text="          ")
p4l5.pack(side=TOP)
iplotmargin=IntVar()
p4cb5=ttk.Checkbutton(p4f0, text="show margin", variable=iplotmargin)
p4cb5.pack(side=TOP, anchor=W)
ifreezebounds=IntVar()
p4cb6=ttk.Checkbutton(p4f0, text="freeze axes", variable=ifreezebounds)
p4cb6.pack(side=TOP, anchor=W)
iwritevals=IntVar()
p4cb7=ttk.Checkbutton(p4f0, text="write values", variable=iwritevals)
p4cb7.pack(side=TOP, anchor=W)
p4l6=ttk.Label(p4f0, text="          ")
p4l6.pack(side=TOP, anchor=W)
###IGGY WORK HERE
xaxstr=StringVar()
p4l7=ttk.Label(p4f0, text="x axis label")
p4l7.pack(side=TOP, anchor=W)
p4e0=ttk.Entry(p4f0, width=20, textvariable=xaxstr)
p4e0.pack(side=TOP, anchor=W)
p4l8=ttk.Label(p4f0, text="          ")
p4l8.pack(side=TOP, anchor=W)
yaxstr=StringVar()
p4l9=ttk.Label(p4f0, text="y axis label")
p4l9.pack(side=TOP, anchor=W)
p4e1=ttk.Entry(p4f0, width=20, textvariable=yaxstr)
p4e1.pack(side=TOP, anchor=W)



p4f1=Frame(master=page4)
p4f1.pack(side=RIGHT, fill=BOTH, expand=1)
f=Figure(figsize=(6,4), dpi=100)
a=f.add_subplot(111)
t=np.arange(0.0,6.28,0.01)
s=np.sin(t)
a.plot(t,s)
mcanvas=FigureCanvasTkAgg(f, master=p4f1)
mcanvas.show()
mcanvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
toolbar=NavigationToolbar2TkAgg(mcanvas, p4f1)
toolbar.update()
mcanvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
def on_key_event(event):
 #print('you pressed %s' % event.key)
 key_press_handler(event, mcanvas, toolbar)
mcanvas.mpl_connect('key_press_event', on_key_event)

def freshplot():
 mkdataobj()
 iplotmodel=0
 if (iplotprob.get() or iplotlog.get()): iplotmodel=1
 if (iplotbrprob.get() or iplotbrlog.get()): iplotmodel=1
 if thistest.npoints > 0:
  if ifreezebounds.get():
   amin,amax=a.get_xlim()
   bmin,bmax=a.get_ylim()
  a.clear()
  a.plot(thistest.sx, thistest.sy, 'r^')
  a.plot(thistest.fx, thistest.fy, 'bv')
  if thistest.xmax < thistest.dstimulus:
   xul=thistest.dstimulus+thistest.mufuzz
  else:
   xul=thistest.xmax+thistest.mufuzz
  t=np.arange(thistest.xmin-thistest.mufuzz,xul,0.01)
  if iplotprob.get():
   vals=thistest.probmusig() 
   mu=vals[0]; sigma=vals[1]
   print("prob "+str(mu)+" "+str(sigma))
   f1=thistest.arr2pg(t, mu, sigma)
   a.plot(t,f1)
  if iplotlog.get():
   vals=thistest.logmusig()
   mu=vals[0]; sigma=vals[1]
   print("log "+str(mu)+" "+str(sigma))
   f1=thistest.arr2pl(t, mu, sigma)
   a.plot(t,f1) 
  if iplotbrprob.get():
   vals=thistest.brprob() 
   mu=vals[0]; sigma=vals[1]
   f1=thistest.arr2pg(t, mu, sigma)
   a.plot(t,f1)
  if iplotbrlog.get():
   vals=thistest.brlog()
   mu=vals[0]; sigma=vals[1]
   f1=thistest.arr2pl(t, mu, sigma)
   a.plot(t,f1)
  if ifreezebounds.get():
   a.set_xlim((amin,amax))
   a.set_ylim((bmin,bmax))
  if iplotmargin.get():
   marginstring=""
   stxsd=(dstimulus.get()).strip()
   stypd=(dprob.get()).strip()
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
     ymarlow,junk=a.get_ylim()
     a.plot([xmarlow,xmarlow],[ymarlow,thistest.dprob/100.0],color='black')
     a.plot([xsd,xsd],[ymarlow,ydstim],color='black')
     vmargin=xsd-xmarlow
     blah="{:."+mufuzz.get()+"f}"
     lmargin=blah.format(vmargin)
     marginstring=", margin$="+str(lmargin)+"$"
    else:
     marginstring=" NO MARGIN!"
  if iwritevals.get():
   amin,amax=a.get_xlim()
   bmin,bmax=a.get_ylim()
   #doesn't need 'r' in front of TeX string?
   if iplotmodel:
    blah="{:."+mufuzz.get()+"f}"
    lmu=blah.format(mu)
    lsig=blah.format(sigma)
    labelstring="$\mu="+str(lmu)+", \sigma="+str(lsig)+"$"
    if iplotmargin.get(): labelstring+=marginstring
    a.text(amin+0.05*(amax-amin), bmax-0.1*(bmax-bmin), labelstring)
  axlabel=xaxstr.get() 
  aylabel=yaxstr.get() 
  if len(axlabel) > 0:
   a.axes.set_xlabel(axlabel)
  if len(aylabel) > 0:
   a.axes.set_ylabel(aylabel)
  mcanvas.show()

p4l1=ttk.Label(p4f0, text="          ")
p4l1.pack(side=TOP)
p4b1=ttk.Button(p4f0, text="Refresh", command=freshplot)
p4b1.pack(side=TOP)

#initialize with input file
try:
 finput=open("tsconfig.txt","r")
 lines=finput.readlines()
 finput.close()
 for aline in lines:
  vals=aline.split()
  if vals[0][0] != '#':
   if vals[0].find("muguess") > -1:
    muguess.set(vals[1].strip())
   if vals[0].find("mugmin") > -1:
    mumin.set(vals[1].strip())  
   if vals[0].find("mugmax") > -1:
    mumax.set(vals[1].strip())  
   if vals[0].find("precision") > -1:
    mufuzz.set(vals[1].strip())   
   if vals[0].find("sigmaguess") > -1:
    sguess.set(vals[1].strip())
   if vals[0].find("designstim") > -1:
    dstimulus.set(vals[1].strip())
   if vals[0].find("designprob") > -1:
    dprob.set(vals[1].strip())
   if vals[0].find("datafile") > -1:
    fname=(vals[1].strip())
    f2fdata(fname)
   if vals[0].find("modelform") > -1:
    modelval.set(vals[1].strip())   
   if vals[0].find("reducebias") > -1:
    ibias.set(int(vals[1].strip()))   
   if vals[0].find("nclint") > -1:
    itest=int(vals[1].strip())
    if itest < 2: itest=2
    thistest.nint=itest
   if vals[0].find("designmatrix") > -1:
    if (vals[1].strip())[0]=='c':
     designval.set("c optimal      ")
    elif (vals[1].strip())[0]=='d':
     designval.set("d optimal      ")
    elif (vals[1].strip())[0]=='s':
     designval.set("sigma optimal")
   if vals[0].find("fontsize") > -1:
    font.nametofont('TkDefaultFont').configure(size=vals[1].strip())
   if vals[0].find("guisize") > -1:
    main.geometry(vals[1].strip())
   if vals[0].find("debug") > -1:
    thistest.debug=int(vals[1].strip())
except:
 6*7

main.mainloop()
