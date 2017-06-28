// ===================================
// TUTORIAL EXCERCISE 2
// Optimizing a Simple Quadratic Model
// ===================================

# include "uqTypes.h"
# include "cmModel.h"
# include "cmTutorial.h"
# include "daData.h"
# include "daData_Scalar_MultiplePatients.h"
# include "acAction.h"
# include "acActionOPT_NM.h"

using namespace std;

// =============
// MAIN FUNCTION
// =============
int main(int argc, char* argv[]){
    
  try{

    // Assign Dataset
    daData* data = new daData_Scalar_MultiplePatients();
    string fileName("../datasets/tutorial.csv");
    data->readFromFile(fileName);

    // Construct Specific Model
    cmModel* myModel;
    myModel = new cmTutorial();

    // Assign Dataset to model
    int currColumn = 1;
    myModel->setData(data,currColumn);

    // Convergence Tolerance
    double convTol = 1.0e-1;
    // Check Convergence every convUpdateIt iterations
    int convUpdateIt = 10;
    // Maximum Iterations
    int maxOptIt = 200;
    // Coefficient for Step increments
    double stepCoefficient = 0.1;    

    // File with initial starting point
    bool useStartingParameterFromFile = false;
    bool startFromCentre = false;
    string startParameterFile("");

    // Construct Optimization Action
    acAction* nm = new acActionOPT_NM(convTol, 
                                      convUpdateIt,
                                      maxOptIt,
                                      stepCoefficient);

    // Set the model
    nm->setModel(myModel);

    // Set Initial Parameter Guess
    ((acActionOPT_NM*)nm)->setInitialParamGuess(useStartingParameterFromFile,
                                                startFromCentre,
                                                startParameterFile);        

    // Run the optimizer
    nm->go();

  }catch(exception &e){
    // ERROR: TERMINATED!
    printf("\n");
    printf("TERMINATED!\n");
    return 0;
  }

  // COMPLETED
  printf("\n");
  printf("COMPLETED!\n");
  return 0;
}
