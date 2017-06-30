// TEST CASE 1 - RUN LPN Model with RK4 Integrator
// DES, March 2017

# include <stdlib.h>
# include <stdio.h>
# include <iostream>
# include <fstream>
# include <math.h>
# include <string>
# include <vector>

# include "uqTypes.h"
# include "uqConstants.h"

# include "odeModel.h"
# include "odeNormalAdultSimplePA.h"

# include "odeIntegrator.h"
# include "odeIntegratorRK4.h"

# include "cmException.h"
# include "cmUtils.h"
# include "cmModel.h"
# include "cmLPNModel.h"

# include "daData.h"
# include "daData_multiple_Table.h"

# include "acAction.h"
# include "acActionOPT_NM.h"


using namespace std;

int main(int argc, char* argv[]){

  double ll = 0.0;
    
  try{

    // Create new data object
    int keyColumn = 0;
    int timeStampColumn = 0;
    string currPatientFile("heartFailure.dat");
    daData* data = new daData_multiple_Table();
    data->readFromFile(currPatientFile);

    // Create a ODE Model
    odeModel* ode = new odeNormalAdultSimplePA();

    // Create a ODE Model Integrator
    double timeStep = 0.01;
    int totalCycles = 5;
    odeIntegrator* rk4 = new odeIntegratorRK4(ode,timeStep,totalCycles);

    // Create new LPN model
    cmModel* lpnModel;
    lpnModel = new cmLPNModel(rk4);

    // Assign Dataset to model
    int currPatient = 0;
    lpnModel->setData(data,currPatient);

    // Set Optimizer Parameters
    // Total Number of iterations
    int totIterations = 5;
    // Convergence Tolerance
    double convTol = 1.0e-6;
    // Check Convergence every convUpdateIt iterations
    int convUpdateIt = 1;
    // Maximum Iterations
    int maxOptIt = 100;
    // Coefficient for Step increments
    double stepCoefficient = 0.01;
    // File with initial starting point
    bool useStartingParameterFromFile = false;
    bool startFromCentre = false;
    string startParameterFile("");

    // Construct Action
    acAction* nm = new acActionOPT_NM(convTol, 
                                      convUpdateIt,
                                      maxOptIt,
                                      stepCoefficient);
    
    // Set Model
    nm->setModel(lpnModel);

    // SET INITIAL GUESS
    ((acActionOPT_NM*)nm)->setInitialParamGuess(useStartingParameterFromFile,
                                                startFromCentre,
                                                startParameterFile);        

    for(int loopA=0;loopA<totIterations;loopA++){
      
      // PERFORM ACTION
      nm->go();

      if(loopA == 0){
        ((acActionOPT_NM*)nm)->setInitialPointFromFile(true);
        ((acActionOPT_NM*)nm)->setInitialPointFile(string("optParams.txt"));
      }
    }

  }catch(exception &e){
    // ERROR: TERMINATED!
    printf("\n");
    printf("TERMINATED!\n");
    return 0;
  }

  // COMPLETED
  printf("\n");
  printf("Obj: %f\n",ll);
  printf("COMPLETED!\n");
  return 0;
}





