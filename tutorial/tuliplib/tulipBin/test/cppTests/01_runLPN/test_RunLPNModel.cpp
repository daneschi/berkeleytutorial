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

    // Get Default parameter set
    stdVec inputs;
    lpnModel->getDefaultParams(inputs);

    // Solve Model
    stdVec outputs;
    stdIntVec errorCodes;    
    ll = lpnModel->evalModelError(inputs,outputs,errorCodes);
    
  }catch(exception& e){
    // ERROR: TERMINATED!
    printf("\n");
    printf("Msg: %s\n",e.what());
    printf("TERMINATED!\n");
    return 0;
  }

  // COMPLETED
  printf("\n");
  printf("Obj: %f\n",ll);
  printf("COMPLETED!\n");
  return 0;
}





