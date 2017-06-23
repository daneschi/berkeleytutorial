# Import tulip
import sys
sys.path.insert(0, '/home/dschiava/Development/CApps/tulipApp/libBin/py')
import numpy as np
# Import UQ Library
import tulipUQ as uq
# Import Computational Model Library
import tulipCM as cm
# Import Data Library
import tulipDA as da
# Import Action Library
import tulipAC as ac

# READ DATASET
data = da.daData_multiple_Table()
data.readFromFile('heartFailure.dat')

# CREATE ODE MODEL
ode = cm.odeNormalAdultSimplePA()

# CREATE ODE INTEGRATOR
timeStep = 0.01
totalCycles = 10
rk4 = cm.odeIntegratorRK4(ode,timeStep,totalCycles)

# Create new LPN model
lpnModel = cm.cmLPNModel(rk4)

# ASSIGN DATA OBJECT TO MODEL
lpnModel.setData(data,0)

# SET OPTIMIZER PARAMETERS
# Total Number of iterations
totIterations   = 2
# Convergence Tolerance
convTol         = 1.0e-6
# Check Convergence every convUpdateIt iterations
convUpdateIt    = 1
# Maximum Iterations
maxOptIt        = 200
# Coefficient for Step increments
stepCoefficient = 0.1;    

# INIT ACTION
nm = ac.acActionOPT_NM(convTol,convUpdateIt,maxOptIt,stepCoefficient)
    
# ASSIGN MODEL TO ACTION
nm.setModel(lpnModel)

# SET INITIAL GUESS - DEFAULT PARAMETER VALUES
useStartingParameterFromFile = False
startFromCentre              = False
startParameterFile           = ''
nm.setInitialParamGuess(useStartingParameterFromFile,startFromCentre,startParameterFile)

for loopA in range(totIterations):      
  # PERFORM ACTION
  nm.go()
  # SET RESTART CONDITION
  if(loopA == 0):
    nm.setInitialPointFromFile(True)
    nm.setInitialPointFile('optParams.txt')
