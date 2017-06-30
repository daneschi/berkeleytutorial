'''
Export Python Optimization Algorithm to tulip 

This file exposes the wrappers for the most popular
optimizers, i.e.: 

fmin(func, x0[, args, xtol, ftol, maxiter, ...])	
Minimize a function using the downhill simplex algorithm.

fmin_powell(func, x0[, args, xtol, ftol, ...])	
Minimize a function using modified Powell's method.

fmin_cg(f, x0[, fprime, args, gtol, norm, ...])	
Minimize a function using a nonlinear conjugate gradient algorithm.

fmin_bfgs(f, x0[, fprime, args, gtol, norm, ...])	
Minimize a function using the BFGS algorithm.

fmin_ncg(f, x0, fprime[, fhess_p, fhess, ...])	
Unconstrained minimization of a function using the Newton-CG method.
'''
# Imports
import sys
sys.path.insert(0, '/home/dschiava/Development/CApps/tulipApp/libBin/py/')
import numpy as np
# Import Computational Models from tulip
import tulipUQ as uq

# Import Optimizers
from scipy.optimize import fmin
from scipy.optimize import least_squares
from scipy.optimize import fmin_powell
from scipy.optimize import fmin_cg
from scipy.optimize import fmin_bfgs
from scipy.optimize import fmin_ncg

# Init Abstract Optimization Class
class poAction_OPT():
  # Constructor
  def __init__(self):
    self.model = None
    self.x0 = None
    self.paramsFromFile = False
    self.paramsFile = ''

  # Run Model Evaluation
  def runModel(self,x):
    inputs = uq.stdVec()
    for loopA in xrange(len(x)):
      inputs.push_back(x[loopA])
    outputs = uq.stdVec()
    errorCode = uq.stdIntVec()
    res = self.model.evalModelError(inputs,outputs,errorCode)
    return res

  # Set Model
  def setModel(self,model):
    self.model = model

  # Set Initial Parameters
  def setInitialParamGuess(self,useStartingParameterFromFile,startFromCentre,startParameterFile):
    if(useStartingParameterFromFile):
      # Set Boolean Variable
      self.paramsFromFile = True
      self.paramsFile = startParameterFile
      # Read Parameters from file
      self.x0 = np.loadtxt(startParameterFile)
    elif(startFromCentre):
      # Start from the average parameters
      limits = uq.stdVec()
      self.model.getParameterLimits(limits)
      numParams = self.model.getParameterTotal()
      self.x0 = np.zeros((numParams,))
      for loopA in xrange(numParams):
        self.x0[loopA] = 0.5*(limits[2*loopA + 0] + limits[2*loopA + 1])
    else:
      # Start from the default parameters
      params = uq.stdVec()
      self.model.getDefaultParams(params)
      self.x0 = params
  
  def setInitialPointFromFile(self,val):
    self.paramsFromFile = val
    
  def setInitialPointFile(self,fileName):
    self.paramsFile = fileName

# =======================
# CLASS TO IMPLEMENT FMIN
# =======================
class poAction_OPT_fmin(poAction_OPT):
  # Constructor
  def __init__(self, args=(), xtol=0.0001, ftol=0.0001, maxiter=None, maxfun=None, full_output=1, disp=0, retall=0, callback=None, initial_simplex=None):
    poAction_OPT.__init__(self)
    self.args = args
    self.xtol = xtol
    self.ftol = ftol
    self.maxiter = maxiter
    self.maxfun = maxfun
    self.full_output = full_output 
    self.disp = disp
    self.retall = retall
    self.callback = callback
    self.initial_simplex = initial_simplex    

  # Run Optimizer
  def go(self):
    
    # Write Header
    print '=================================='
    print 'fmin Optimizer from scipy.optimize'
    print '=================================='

    # Assign Initial Guess
    if(self.paramsFromFile):
      self.x0 = np.loadtxt(self.paramsFile)
    
    # Show Initial Parameter Guess
    print 'Initial Parameter Guess'
    for loopA in xrange(len(self.x0)):
      print '%5d %10.5e' % (loopA+1,self.x0[loopA])
    print 'Running Solver...',

    # Run Optimization
    xopt,fopt,iterDone,funcalls,warnflag  = fmin(self.runModel, \
                                                 self.x0, \
                                                 self.args, \
                                                 self.xtol, \
                                                 self.ftol, \
                                                 self.maxiter, \
                                                 self.maxfun, \
                                                 self.full_output, \
                                                 self.disp, \
                                                 self.retall, \
                                                 self.callback, \
                                                 self.initial_simplex)

    # Write Infos on Screen
    print 'OK.'
    print 'Optimal Parameter List'
    for loopA in xrange(len(xopt)):
      print '%5d %10.5e' % (loopA+1,xopt[loopA])

    print 'Optimal Function value: %10.5e' % (fopt)
    print 'Number of iterations: %d, Number of function evaluations: %d' % (iterDone,funcalls)
    print 'Warning flag: %d' % (warnflag)

    # Write Optimal Parameters to file
    np.savetxt('optParams.txt',xopt)

# ================================
# CLASS TO IMPLEMENT LEAST_SQUARES
# ================================
class poAction_OPT_lsSqr(poAction_OPT):

  # Constructor
  def __init__(self):
    poAction_OPT.__init__(self)

  # Run Optimizer
  def go(self):
    
    # Write Header
    print ''
    print '==========================================='
    print 'least_squares optimizer from scipy.optimize'
    print '==========================================='
    print ''

    # Assign Initial Guess
    if(self.paramsFromFile):
      self.x0 = np.loadtxt(self.paramsFile)
    
    # Show Initial Parameter Guess
    print 'Initial Parameter Guess'
    for loopA in xrange(len(self.x0)):
      print '%5d %10.5e' % (loopA+1,self.x0[loopA])
    print 'Running Least Squares Optimizer...',

    # Run Least Squares Optimizer
    res = least_squares(self.runModel,self.x0)

    # Write Infos on Screen
    print 'OK.'
    print 'Optimal Parameter List'
    for loopA in xrange(len(res.x)):
      print '%5d %10.5e' % (loopA+1,res.x[loopA])
    print 'Optimal Function value: %10.5e' % (res.cost)

    if(res.success):
      print 'Optimum successfully determined.'
    else:
      print 'Optimum NOT found.'
      print 'Error Message: ',message

    # Write Optimal Parameters to file
    np.savetxt('optParams.txt',res.x)

