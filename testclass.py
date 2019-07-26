from scipy.special import erf
import scipy.optimize as opt
from numpy.random import rand
from math import *
import datetime

class dettest:
 """
 includes all data and functions necessary for sensitivity data analysis
 initialization takes text data separated by white space or commas
 and expects a newline '\n' between data points
 """

 def __init__(self):
  """initialize dettest variables"""
  fout=open("tsoutput.txt","a")
  now=datetime.datetime.now()
  fout.write(now.strftime("%Y-%m-%d %H:%M")+"\n")
  self.fv=1E11
  self.sx=[]; self.sy=[]; self.fx=[]; self.fy=[];
  self.xmin=self.fv
  self.xmax=-self.fv
  self.mufuzz=0.1
  self.muguess=0.0
  self.mumax=0.0
  self.mumin=0.0
  self.sguess=0.0
  self.dstimulus=0.0
  self.dprob=99.9
  self.reducebias=1
  self.model="logit"
  self.xopt=2.0
  self.nint=3
  self.npoints=0
  self.nlastnext=0
  self.phase="0"
  self.debug=1
  if self.debug == 1:
   fout.write("\n\nstarting trueSIG at ")
  fout.close()
  self.neyer=False

 def list2design(self, designlist):
  """takes design info from first page/tab of GUI app"""
  self.muguess=designlist[0] 
  self.mumax=designlist[1]
  self.mumin=designlist[2]
  self.mufuzz=pow(10.0,-designlist[3])
  self.sguess=designlist[4]
  self.dstimulus=designlist[5]
  self.dprob=designlist[6]

 def text2data(self, textdata):
  """turn text box from app into data in dettest class"""
  self.sx=[]; self.sy=[]; self.fx=[]; self.fy=[];
  self.xmin=self.fv
  self.xmax=-self.fv
  lines=textdata.split('\n')
  if self.debug:
   fout=open("tsoutput.txt","a")
   fout.write("data now:\n")
  for aline in lines:
   if len(aline) > 0:
    if aline[0] != '#':
     if aline.find(',') > 0: pts=aline.split(',')
     else: pts=aline.split()
     px=float(pts[0])
     py=float(pts[1])
     if self.debug: fout.write(pts[0]+"  "+pts[1]+"\n")
     if py > 0.5: self.sx.append(px); self.sy.append(py)
     else: self.fx.append(px); self.fy.append(py)
     if px > self.xmax: self.xmax=px
     if px < self.xmin: self.xmin=px
  if self.xmin==self.fv: self.xmin=0
  if self.xmax==-self.fv: self.xmax=0
  self.npoints=len(self.sx)+len(self.fx)
  if self.debug: fout.close()

 def checkdata(self):
  """finds min and max stimuli and number of points in data"""
  self.xmin=self.fv
  self.xmax=-self.fv
  for tsx in self.sx:
   if tsx > self.xmax: self.xmax=tsx
   if tsx < self.xmin: self.xmin=tsx
  for tfx in self.fx:
   if tfx > self.xmax: self.xmax=tfx
   if tfx < self.xmin: self.xmin=tfx
  if self.xmin==self.fv: self.xmin=0
  if self.xmax==-self.fv: self.xmax=0
  self.npoints=len(self.sx)+len(self.fx)

 def xspread(self):
  """Find maximum difference in values of stimuli"""
  if self.npoints==0: return 0
  else:
   xmin=1E11
   xmax=-1E11
   for xval in self.fx+self.sx:
    if xval > xmax: xmax=xval
    if xval < xmin: xmin=xval
   spread=xmax-xmin
  if spread==2E11: spread=0
  return spread

 def smin(self):
  """Find minimum success stimulus"""
  if len(self.sx)==0: return 1E11
  else:
   xmin=1E11
   for xval in self.sx:
    if xval < xmin: xmin=xval
   return xmin

 def fmax(self):
  """Find maximum failure stimulus"""
  if len(self.fx)==0: return -1E11
  else:
   xmax=-1E11
   for xval in self.fx:
    if xval > xmax: xmax=xval
   return xmax

 def logmu(self):
  """Find best value of mu assuming sigma=(spread of data)/2 in logit model
  """
  sigma=self.xspread()/2.0
  def ll(x0):
   i=0
   llv=0.0
   mu=x0[0]
   while i < len(self.sx):
    llv-=log(1.0+exp(-(self.sx[i]-mu)/sigma))
    i+=1
   i=0
   while i < len(self.fx):
    llv-=log(1.0+exp((self.fx[i]-mu)/sigma))
    i+=1
   return -llv
  smt=self.smin()
  fmt=self.fmax()
  if smt != -self.fv and fmt != self.fv:
   mutest=(smt+fmt)/2.0
   x0=[mutest]
   fx0=opt.fmin(ll,x0,disp=False, maxiter=200)
   return fx0[0],sigma
  else:
   return 0,0

 def logmufixsig(self, sigma):
  """Find best value of mu assuming fixed sigma in logit model"""
  def ll(x0):
   i=0
   llv=0.0
   mu=x0[0]
   while i < len(self.sx):
    llv-=log(1.0+exp(-(self.sx[i]-mu)/sigma))
    i+=1
   i=0
   while i < len(self.fx):
    llv-=log(1.0+exp((self.fx[i]-mu)/sigma))
    i+=1
   return -llv
  smt=self.smin()
  fmt=self.fmax()
  if smt != -self.fv and fmt != self.fv:
   mutest=(smt+fmt)/2.0
   x0=[mutest]
   fx0=opt.fmin(ll,x0,disp=False, maxiter=200)
   return fx0[0],sigma
  else:
   return 0,0

 def logmusig(self):
  """Find maximum likelihood mu, sigma using logit model"""
  if self.npoints!=0:
   if len(self.sx) == 0:
    return self.fmax()+self.mufuzz,self.mufuzz
   elif len(self.fx) == 0:
    return self.smin()-self.mufuzz,self.mufuzz
   elif self.smin() < self.fmax():
    sg=(self.fmax()-self.smin())
    mg=(self.fmax()+self.smin())/2.0
    def ll(x0):
     llv=0.0
     mu=x0[0]
     sigma=x0[1]
     i=0
     while i < len(self.sx):
      try:
       llv-=log(1.0+exp(-(self.sx[i]-mu)/sigma))
      except: llv-=self.fv
      i+=1
     i=0
     while i < len(self.fx):
      try:
       llv-=log(1.0+exp((self.fx[i]-mu)/sigma))
      except: llv-=self.fv
      i+=1
     return -llv
    x0=[mg,sg]
    fx0=opt.fmin(ll,x0,disp=False, maxiter=200)
    if fx0[0] < self.xmin: fx0[0]=self.xmin
    if fx0[0] > self.xmax: fx0[0]=self.xmax
    if fx0[1] > self.xspread(): fx0[1]=self.xspread()
    return fx0[0],fx0[1]
   else:
    return (self.smin()+self.fmax())/2.0,(self.smin()-self.fmax())/10.0
  else:
   return 0,0

 def probmu(self):
  """Find best value of mu assuming sigma=(spread of data)/2"""
  sigma=self.xspread()/2.0
  rt2=sqrt(2.0)
  def ll(x0):
   i=0
   llv=1.0
   mu=x0[0]
   while i < len(self.sx):
    llv*=(0.5+0.5*erf((self.sx[i]-mu)/sigma/rt2))
    i+=1
   i=0
   while i < len(self.fx):
    llv*=(0.5-0.5*erf((self.fx[i]-mu)/sigma/rt2))
    i+=1
   try: 
    llv=-log(llv)
   except: 
    llv=self.fv
   return llv
  smt=self.smin()
  fmt=self.fmax()
  if smt != -self.fv and fmt != self.fv:
   mutest=(smt+fmt)/2.0
   x0=[mutest]
   fx0=opt.fmin(ll,x0,disp=False, maxiter=200)
   return fx0[0],sigma
  else:
   return 0,0

 def probmufixsig(self,sigma):
  """Find best value of mu assuming fixed sigma in probit model"""
  rt2=sqrt(2.0)
  def ll(x0):
   i=0
   llv=1.0
   mu=x0[0]
   while i < len(self.sx):
    llv*=(0.5+0.5*erf((self.sx[i]-mu)/sigma/rt2))
    i+=1
   i=0
   while i < len(self.fx):
    llv*=(0.5-0.5*erf((self.fx[i]-mu)/sigma/rt2))
    i+=1
   try: 
    llv=-log(llv)
   except: 
    llv=self.fv
   return llv
  smt=self.smin()
  fmt=self.fmax()
  if smt != -self.fv and fmt != self.fv:
   mutest=(smt+fmt)/2.0
   x0=[mutest]
   fx0=opt.fmin(ll,x0,disp=False, maxiter=200)
   return fx0[0],sigma
  else:
   return 0,0

 def probmusig(self):
  """Find maximum likelihood mu, sigma"""
  rt2=sqrt(2.0)
  if self.npoints!=0:
   if len(self.sx) == 0:
    return self.fmax()+self.mufuzz,self.mufuzz
   elif len(self.fx) == 0:
    return self.smin()-self.mufuzz,self.mufuzz
   elif self.smin() < self.fmax():
    sg=(self.fmax()-self.smin())
    mg=(self.fmax()+self.smin())/2.0
    def ll(x0):
     llv=1.0
     mu=x0[0]
     sigma=x0[1]
     i=0
     while i < len(self.sx):
      llv*=(0.5+0.5*erf((self.sx[i]-mu)/sigma/rt2))
      i+=1
     i=0
     while i < len(self.fx):
      llv*=(0.5-0.5*erf((self.fx[i]-mu)/sigma/rt2))
      i+=1
     try:
      llv=-log(llv)
     except:
      llv=self.fv
     return llv
    x0=[mg,sg]
    fx0=opt.fmin(ll, x0, disp=False, xtol=0.001, maxiter=200)
    if fx0[0] < self.xmin: fx0[0]=self.xmin
    if fx0[0] > self.xmax: fx0[0]=self.xmax
    if fx0[1] > self.xspread(): fx0[1]=self.xspread()
    return fx0[0],fx0[1]
   else:
    return (self.smin()+self.fmax())/2.0,(self.smin()-self.fmax())/5.0
  else:
   return 0,0

 def brlog(self):
  """returns mu, bias reduced sigma for logit model"""
  mu0,sig0=self.logmusig()
  def ll(x0):
   i=0
   llv=1.0
   mu=x0[0]
   sigma=x0[1]
   while i < len(self.sx):
    try:
     pval=1.0/(1.0+exp(-(self.sx[i]-mu)/sigma))
    except:
     if self.sx[i] > mu: pval=1.0
     else: pval=0.0
    llv*=pval
    i+=1
   i=0
   while i < len(self.fx):
    try:
     pval=1.0/(1.0+exp((self.fx[i]-mu)/sigma))
    except:
     if self.fx[i] > mu: pval=0.0
     else: pval=1.0
    i+=1
    llv*=pval
   return llv
  p0=ll([mu0,sig0])
  if self.fmax() == self.smin() and p0 < 1.0/2.0**(self.npoints-2):
   mu0=self.fmax()
   sig0=self.mufuzz
   p0=ll([mu0,sig0])
  sigm=sig0-self.mufuzz
  p=ll([mu0,sigm])
  while p > p0/2.0 and sigm > 0:
   sigm-=self.mufuzz
   try: p=ll([mu0,sigm])
   except: p=0.0
  if sigm < 0: sigm=0
  sigp=sig0+self.mufuzz
  p=ll([mu0,sigp])
  ppow=self.npoints-2
  if ppow <= 0: ppow=1.0
  while (p > p0/2.0) and (p > 1.0/2.0**ppow):
   sigp+=self.mufuzz
   p=ll([mu0,sigp])
  return mu0,(sigm+sigp)/2.0
  
 def brprob(self):
  """returns mu, bias reduced sigma for probit model"""
  mu0,sig0=self.probmusig()
  def ll(x0):
   rt2=sqrt(2.0)
   i=0
   llv=1.0
   mu=x0[0]
   sigma=x0[1]
   if sigma==0: sigma=self.mufuzz
   while i < len(self.sx):
    llv*=(0.5+0.5*erf((self.sx[i]-mu)/sigma/rt2))
    i+=1
   i=0
   while i < len(self.fx):
    llv*=(0.5-0.5*erf((self.fx[i]-mu)/sigma/rt2))
    i+=1
   return llv
  p0=ll([mu0,sig0])
  if self.fmax() == self.smin() and p0 < 1.0/2.0**(self.npoints-2):
   mu0=self.fmax()
   sig0=self.mufuzz
   p0=ll([mu0,sig0])
  sigm=sig0-self.mufuzz
  p=ll([mu0,sigm])
  while p > p0/2.0 and sigm > 0:
   sigm-=self.mufuzz
   p=ll([mu0,sigm])
  if sigm < 0: sigm=0
  sigp=sig0+self.mufuzz
  p=ll([mu0,sigp])
  ppow=self.npoints-2
  if ppow <= 0: ppow=1.0
  while p > p0/2.0 and (p > 1.0/2.0**ppow):
   sigp+=self.mufuzz
   p=ll([mu0,sigp])
  return mu0,(sigm+sigp)/2.0

 def fishlog(self,mu,sigma):
  """returns a0,a1,a2 Fisher information for logit model"""
  a0=a1=a2=0.0
  if sigma==0: sigma=self.mufuzz
  i=0
  while i < len(self.sx):
   xr=(self.sx[i]-mu)/sigma
   try:
    pl=1.0/(1.0+exp(-xr)) 
   except:
    pl=0.0
   ql=1.0-pl
   wt=pl*ql/sigma/sigma
   a0+=wt
   a1+=wt*xr
   a2+=wt*xr**2
   i+=1
  i=0
  while i < len(self.fx):
   xr=(self.fx[i]-mu)/sigma
   try:
    pl=1.0/(1.0+exp(xr)) 
   except:
    pl=0
   ql=1.0-pl
   wt=pl*ql/sigma/sigma
   a0+=wt
   a1+=wt*xr
   a2+=wt*xr**2
   i+=1
  return a0,a1,a2
       
 def fishprob(self,mu,sigma):
  """returns a0,a1,a2 Fisher information for probit model"""
  if sigma==0: sigma=self.mufuzz
  rt2=sqrt(2.0)
  a0=a1=a2=0.0
  i=0
  while i < len(self.sx):
   arg=(self.sx[i]-mu)/sigma
   pg=0.5+0.5*erf(arg/rt2)
   qg=1.0-pg
   if pg==0 or qg==0:
    wt=0.0
   else:
    try: 
     wt=exp(-arg*arg)/pg/qg/sigma/sigma/2.0/pi
    except: 
     wt=0.0
   a0+=wt
   a1+=wt*arg
   a2+=wt*arg**2
   i+=1
  i=0
  while i < len(self.fx):
   arg=(self.fx[i]-mu)/sigma
   pg=0.5+0.5*erf(arg/rt2)
   qg=1.0-pg
   if pg==0 or qg==0:
    wt=0.0
   else:
    try: 
     wt=exp(-arg*arg)/pg/qg/sigma/sigma/2.0/pi
    except: 
     wt=0.0
   a0+=wt
   a1+=wt*arg
   a2+=wt*arg**2
   i+=1
  return a0,a1,a2
  
 def arr2pg(self, xa,mu,sigma):
  """returns array of cumulative gaussian values with mean mu and 
     standard deviation sigma from array of argument values xa
  """
  apg=[]
  rt2=sqrt(2.0)
  for x in xa:
   apg.append(0.5+0.5*erf((x-mu)/rt2/sigma))
  return apg

 def arr2pl(self, xa,mu,sigma):
  """returns array of logistic function values with mean mu and 
     scale parameter sigma from array of argument values xa
  """
  apl=[] 
  for x in xa:
   try: p=1.0/(1.0+exp(-(x-mu)/sigma))
   except:
    if x > mu: p=1.0
    else: p=0.0
   apl.append(p)
  return apl

 def tval(self):
  """Finds c optimal design value in units of t=(x-mu)/sigma
     for either lobit or probit, whichever is being used
  """
  if self.model=="probit":
   tstr="pr"
   def pdiff(x0):
    x=x0[0]
    return abs(self.dprob*0.01-(0.5+0.5*erf(x/sqrt(2.0))))
   x0=[1]
   fx0=opt.fmin(pdiff, x0, disp=False)
   t=fx0[0]
   def invunc(x0):
    x=x0[0]
    p=0.5+0.5*erf(x/sqrt(2.0))
    q=1.0-p
    return p*q*exp(x**2)*(1.0+t**2/x**2)
   x0=[1]
   fx0=opt.fmin(invunc, x0, disp=False)
   t=fx0[0]
  elif self.model=="logit":
   tstr="lo"
   def pdiff(x0):
    x=x0[0]
    return abs(self.dprob*0.01-(1.0/(1.0+exp(-x))))
   x0=[1]
   fx0=opt.fmin(pdiff, x0, disp=False)
   t=fx0[0]
   def invunc(x0):
    x=x0[0]
    p=1.0/(1.0+exp(-x))
    q=1.0-p
    return (1.0+t**2/x**2)/p/q
   x0=[1]
   fx0=opt.fmin(invunc, x0, disp=False)
   t=fx0[0] 
  else:
   tstr="fu"
   t=2.0
  self.xopt=t
  return tstr

 def tripod(self):
  """tripod phase 1 algorithm from Wu paper
     leads to quicker initial unique MLEs
  """
  if self.npoints > 1 and self.phase=="0":
   self.phase="2"
  if 6*self.sguess > self.mumax-self.mumin:
   self.sguess = (self.mumax-self.mumin)/6.0
  pnext=self.fv
  if self.phase=="0":
   if self.npoints==0:
    pnext=0.25*self.mumin+0.75*self.mumax
   if self.npoints==1:
    pnext=0.75*self.mumin+0.25*self.mumax
    self.phase="1"
  elif self.phase[0]=="1":
   if self.npoints==1:
    pnext=0.75*self.mumin+0.25*self.mumax
    self.phase="1"
   elif len(self.sx)==0:
    pnext=self.mumax+1.5*(self.npoints-1)*self.sguess
   elif len(self.fx)==0:
    pnext=self.mumin-1.5*(self.npoints-1)*self.sguess
   elif (self.smin() < self.fmax() and self.npoints==2) or self.phase=="1iv":
    if self.npoints==2:
     pnext=self.mumin-3*self.sguess
     self.phase="1iv"
    else:
     pnext=self.mumax+3*self.sguess
     self.phase="2"
   else:
    self.phase="2"
  if self.phase[0]=="2" and pnext==self.fv:
   if self.smin() < self.fmax():
    self.phase="3"
   if self.phase=="2ec":
    if self.nlastnext == self.npoints:
     self.nlastnext=self.npoints-1
     self.phase="2c"
    else:
     self.phase="2e"
   if self.phase=="2ed":
    if self.nlastnext == self.npoints:
     self.phase="2d"
     self.nlastnext=self.npoints-1 
    else:
     self.phase="2e"
   if self.phase=="2e":
    if self.nlastnext < self.npoints:
     self.sguess=2.0*self.sguess/3.0
    self.phase="2"
   if self.smin()-self.fmax() > 1.5*self.sguess:
    if self.model=="logit":
     pnext,blah=self.logmufixsig(self.sguess)
    elif self.model=="probit":
     pnext,blah=self.probmufixsig(self.sguess) 
   else:
    if len(self.sx) >= len(self.fx):
     if self.phase=="2" or \
        (self.phase=="2c" and self.nlastnext == self.npoints):
      pnext=self.smin()+0.3*self.sguess
      self.phase="2c"
     elif self.phase=="2c":
      pnext=self.fmax()-0.3*self.sguess
      self.phase="2ec"
    else:
     if self.phase=="2" or \
        (self.phase=="2d" and self.nlastnext == self.npoints):
      pnext=self.fmax()-0.3*self.sguess
      self.phase="2d"
     elif self.phase=="2d":
      pnext=self.smin()+0.3*self.sguess
      self.phase="2ed"
  if self.phase[0]=="3":
   if self.fmax()-self.smin() >= self.sguess:
    pnext=(self.fmax()+self.smin())/2.0
    self.phase="4"
   else:
    if self.phase=="3" or \
       (self.phase=="3b" and self.nlastnext == self.npoints):
     pnext=(self.fmax()+self.smin())/2.0+0.5*self.sguess
     self.phase="3b"
    elif self.phase=="3b":
     pnext=(self.fmax()+self.smin())/2.0-0.5*self.sguess 
     self.phase="3c"
    elif self.phase=="3c" and self.nlastnext==self.npoints:
     pnext=(self.fmax()+self.smin())/2.0-0.5*self.sguess 
    else:
     self.phase="4"
  if pnext==self.fv: 
   self.phase="4"
   pnext=self.nextpointn()
  self.nlastnext=self.npoints
  return pnext

 def nextpointn(self):
  """get next recommended stimulus for experiment
     modeled after Neyer but generalized to c-optimal and optionally
     uses bias reduced scale parameter estimate
  """
  sigma=self.fv
  mu=self.fv
  if self.npoints == 0:
   pnext=(self.mumin+self.mumax)/2.0
  elif len(self.fx)==0:
   x1=(self.mumin+self.xmax)/2.0
   x2=(self.xmin-2.0*self.sguess)
   x3=2.0*self.xmin-self.xmax 
   if x1 < x2:
    pnext=x1
   else:
    pnext=x2
   if x3 < pnext: pnext=x3
  elif len(self.sx)==0:
   x1=(self.mumax+self.xmax)/2.0
   x2=self.xmax+2.0*self.sguess
   x3=2.0*self.xmax-self.xmin
   if x1 > x2:
    pnext=x1
   else:
    pnext=x2
   if x3 > pnext: pnext=x3
  else:
   diff=self.smin()-self.fmax()
   if diff > self.sguess and self.sguess > 0:
     pnext=(self.smin()+self.fmax())/2.0
   else:
    if self.model=="probit":
     mu,sigma=self.probmusig()
    elif self.model=="logit":
     mu,sigma=self.logmusig() 
    if sigma  < self.mufuzz:
     mu=(self.smin()+self.fmax())/2.0
     sigma=self.sguess
     if self.nlastnext < self.npoints: self.sguess=self.sguess*0.8
    if self.reducebias and diff < 0:
     if self.model=="probit":
      mu,sigma=self.brprob()
     if self.model=="logit":
      mu,sigma=self.brlog()
    #test for unreasonable values of mu
    if self.xmax < mu: mu=self.xmax
    if self.xmin > mu: mu=self.xmin
    #test for unreasonable vavlues of sigma
    if sigma > self.xmax-self.xmin: sigma=self.xmax-self.xmin
    if self.model=="probit":
     a0,a1,a2=self.fishprob(mu,sigma)
    elif self.model=="logit":
     a0,a1,a2=self.fishlog(mu,sigma)
    if a1 > 0: pnext=mu-sigma*self.xopt
    else: pnext=mu+sigma*self.xopt 
  if self.mufuzz > 0.0: pnext=self.mufuzz*int(pnext/self.mufuzz) 
  self.nlastnext=self.npoints
  return pnext

 def nextpoint(self):
  """choose which algorithm to use for next stimulus"""
  if self.debug:
   fout=open("tsoutput.txt","a")
   fout.write("mu min "+str(self.mumin)+"\n")
   fout.write("mu max "+str(self.mumax)+"\n")
   fout.write("sigma guess "+str(self.sguess)+"\n")
   fout.write("neyer? "+str(self.neyer)+"\n")
   fout.write("pre-phase is now "+str(self.phase)+"\n")
  #the following "if" is to help with recalcitrant users
  if self.phase != "0" and self.npoints == 0:
   self.phase="0"
  if self.fmax() <= self.smin() and \
     (self.phase[0]=="3" or self.phase[0]=="4"): 
   self.phase="0"
  #use modified neyer if we have achieved robust overlap
  if self.neyer or self.phase=="4":
   pnext=self.nextpointn()
  #start with Wu's tripod
  else:
   pnext=self.tripod()
  if self.debug:
   fout.write("post-phase is now "+str(self.phase)+"\n")
   fout.write("suggesting data at "+str(pnext)+"\n")
   fout.close()
  return pnext 

 def cltcl(self):
  """central limit theorem confidence level
     -assumes no correlation
     -could add correlation since it is not too much more effort
  """
  nint=self.nint
  clint=0.0
  normint=0.0
  if self.model=="probit":
   def pdiff(x0):
    x=x0[0]
    return abs(self.dprob*0.01-(0.5+0.5*erf(x/sqrt(2.0))))
   x0=[1]
   fx0=opt.fmin(pdiff, x0, disp=False)
   t=fx0[0]
   if self.reducebias:
    mu,sigma=self.brprob()
   else:
    mu,sigma=self.probmusig()
   a0,a1,a2=self.fishprob(mu,sigma) 
  elif self.model=="logit":
   def pdiff(x0):
    x=x0[0]
    return abs(self.dprob*0.01-1.0/(1.0+exp(-x)))
   x0=[1]
   fx0=opt.fmin(pdiff, x0, disp=False)
   t=fx0[0]
   if self.reducebias:
    mu,sigma=self.brlog()
   else:
    mu,sigma=self.logmusig()
   a0,a1,a2=self.fishlog(mu,sigma)
  #print("a0,1,2="+str(a0)+" "+str(a1)+" "+str(a2))
  dmu=1.0/sqrt(a0)/(1.0*nint)
  dsig=1.0/sqrt(a2)/(1.0*nint)
  imu=-4*nint
  if sigma-4*nint*dsig < 0.0:
   isigmin=-int(sigma/dsig)
  else:
   isigmin=-4*nint
  while imu < 4*nint+1:
   isig=isigmin
   while isig < 4*nint+1:
    xmu=mu+dmu*imu
    xsig=sigma+dsig*isig
    arg=(self.dstimulus-xmu)/xsig
    ea1=(xmu-mu)**2*a0/2.0
    ea2=(xsig-sigma)**2*a2/2.0
    amp=exp(-ea1-ea2)
    if arg >= t:
     clint+=amp
    normint+=amp
    isig+=1 
   imu+=1
  return clint/normint

 def lklhdcl(self):
  """confidence level from observed likelihood
  """
  nint=self.nint
  clint=0.0
  normint=0.0
  def plog(pmu,psigma):
   i=0
   pv=1.0
   while i < len(self.sx):
    try:
     pt=1.0/(1.0+exp(-(self.sx[i]-pmu)/psigma))
    except: 
     if self.sx[i] > pmu: 
      pt=1.0
     else:
      pt=0.0
    pv*=pt
    i+=1
   i=0
   while i < len(self.fx):
    try:
     pt=1.0/(1.0+exp((self.fx[i]-pmu)/psigma))
    except: 
     if self.fx[i] < pmu:
      pt=1.0
     else:
      pt=0.0
    pv*=pt
    i+=1
   return pv
  def pprob(pmu,psigma):
   i=0
   pv=1.0
   while i < len(self.sx):
    pt=0.5+0.5*erf((self.sx[i]-pmu)/psigma/sqrt(2.0))
    pv*=pt
    i+=1
   i=0
   while i < len(self.fx):
    pt=0.5-0.5*erf((self.fx[i]-pmu)/psigma/sqrt(2.0))
    pv*=pt
    i+=1
   return pv
  if self.model=="probit":
   mu,sigma=self.probmusig()
   a0,a1,a2=self.fishprob(mu,sigma) 
   pnow=pprob(mu,sigma)
  elif self.model=="logit":
   mu,sigma=self.logmusig()
   a0,a1,a2=self.fishlog(mu,sigma)
   pnow=plog(mu,sigma)
  dmu=1.0/sqrt(a0)/(1.0*nint)
  dsig=1.0/sqrt(a2)/(1.0*nint)
  imu=-4*nint
  if sigma-4*nint*dsig < 0.0:
   isigmin=-int(sigma/dsig)
  else:
   isigmin=-4*nint
  while imu < 4*nint+1:
   isig=isigmin
   while isig < 4*nint+1 or pnow > 2.0**(-(self.npoints-2)):
    xmu=mu+dmu*imu
    xsig=sigma+dsig*isig
    if self.model=="logit":
     pnow=plog(xmu,xsig)
     try: pd=1.0/(1.0+exp(-(self.dstimulus-xmu)/xsig))
     except:
      if self.dstimulus > xmu: pd=1.0
      else: pd=0.0
    elif self.model=="probit":
     pnow=pprob(xmu,xsig)
     pd=0.5+0.5*erf((self.dstimulus-xmu)/xsig/sqrt(2.0))
    if pd > 0.01*self.dprob: clint+=pnow
    normint+=pnow
    isig+=1 
   imu+=1
  return clint/normint

 def rp(self,x,mu,sigma):
  """return a random sample following a cumulative Gaussian"""
  pval=0.5+0.5*erf((x-mu)/sqrt(2.0)/sigma)
  if rand() <= pval:
   y=1.0
  else:
   y=0.0
  return y

 def rl(self,x,mu,sigma):
  """return a random sample following a logistic function"""
  pval=1.0/(1.0+exp(-(x-mu)/sigma))
  if rand() <= pval:
   y=1.0
  else:
   y=0.0
  return y

 def addpoint(self,x,y):
  """add a point to a data set"""
  if self.debug:
   fout=open("tsoutput.txt","a")
   fout.write("adding data: "+str(x)+"  "+str(y)+"\n")
   fout.close()
  if y==0.0:
   self.fx.append(x)
   self.fy.append(y)
  else:
   self.sx.append(x)
   self.sy.append(y)
  self.checkdata()

 def reset(self, sguess):
  """removes all data, meant for use with simulations"""
  self.fx=[]; self.fy=[]; self.sx=[]; self.sy=[]
  self.sguess=sguess
  self.phase="0"
  self.checkdata()
