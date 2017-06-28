# Imports
import sys
sys.path.insert(0, '../../py')
import tulipUQ as uq
import numpy as np

if __name__ == "__main__":

  # Set Quadrature Order and type of support
  quadOrder = 9
  suppType = uq.kLegendreRange

  # Contruct the three rules
  firstRule  = uq.uq1DQuadratureRule_CC(quadOrder,suppType);
  secondRule = uq.uq1DQuadratureRule_CCDouble(quadOrder,suppType);
  thirdRule  = uq.uq1DQuadratureRule_Regular(quadOrder,suppType);

  # Generate Points and Weights
  firstRule.generatePointsAndWeights();
  secondRule.generatePointsAndWeights();
  thirdRule.generatePointsAndWeights();

  # Get Points and Weights
  point1  = np.array(firstRule.getPoints());
  weight1 = np.array(firstRule.getWeights());
  point2  = np.array(secondRule.getPoints());
  weight2 = np.array(secondRule.getWeights());
  point3  = np.array(thirdRule.getPoints());
  weight3 = np.array(thirdRule.getWeights());

  print 'Point1: ',point1
  print 'Weight1: ',weight1

  print 'Point2: ',point2
  print 'Weight2: ',weight2

  print 'Point3: ',point3
  print 'Weight3: ',weight3


