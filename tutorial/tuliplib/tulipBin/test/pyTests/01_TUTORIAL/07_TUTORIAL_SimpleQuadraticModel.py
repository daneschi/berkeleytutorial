# Imports
import sys
sys.path.insert(0, '../../py')

import tulipUQ as uq
import tulipDA as da
import tulipCM as cm
import numpy as np
import matplotlib.pyplot as plt

# =============
# MAIN FUNCTION
# =============
if __name__ == "__main__":

  # Assign Dataset
  data = da.daData_Scalar_MultiplePatients()
  data.readFromFile('tutorial.csv')
    
  # Construct Specific Model
  myModel = cm.cmTutorial();

  # Assign Dataset
  currentColumn = 1;
  myModel.setData(data,currentColumn);

  # Get Default Input Parameter Values
  inputs = uq.stdVec()
  myModel.getDefaultParams(inputs)

  # Solve Model
  outputs = uq.stdVec()
  errorCodes = uq.stdIntVec()
  ll = myModel.evalModelError(inputs,outputs,errorCodes)

  print 'Model Results'
  print ''
  print 'Final Location: %f' % (outputs[0])
  print 'Total Time: %f' % (outputs[1])
  print 'Maximum Height: %f' % (outputs[2])
  print ''
  print 'Resulting Log-likelihod: %f' % (ll)
