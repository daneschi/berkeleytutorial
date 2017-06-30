// =====================================================
// TUTORIAL EXCERCISE 3
// Estimating the parameters of a simple quadratic model
// =====================================================

# include "mpi.h"
# include "cmModel.h"
# include "cmTutorial.h"
# include "daData.h"
# include "daData_Scalar_MultiplePatients.h"
# include "acAction.h"
# include "acActionDREAM.h"

using namespace std;


// =============
// MAIN FUNCTION
// =============
int main(int argc, char* argv[]){

  int num_procs = 0;
  int id = 0;

  try{

    // INIT MPI
    MPI_Init(&argc,&argv);
    MPI_Comm_size(MPI_COMM_WORLD,&num_procs);
    MPI_Comm_rank(MPI_COMM_WORLD,&id);

    // Assign Dataset
    daData* data = new daData_Scalar_MultiplePatients();
    string fileName("../datasets/tutorial.csv");
    data->readFromFile(fileName);

    // Create a generic model
    cmModel* myModel;
    myModel = new cmTutorial();  

    // ASSIGN DATASET
    int currColumn = 1;
    myModel->setData(data,currColumn);

    // DREAM PARAMETERS
    int totChains = num_procs;
    int totGenerations = 100;
    int totalCR = 3;
    int totCrossoverPairs = 5;

    double dreamGRThreshold = 1.2;
    int dreamJumpStep = 10;
    int dreamGRPrintStep = 10;

    // OUTPUT FILES
    string dreamChainFileName("chain_GR_000000.txt");
    string dreamGRFileName("gr_GR.txt");

    // RESTART
    // No restart Simulation
    string dreamRestartReadFileName = "";
    string dreamRestartWriteFileName = "restart_write_GR.txt";

    // SET PRIOR INFORMATION
    bool usePriorFromFile = false;
    string priorFileName("");
    int priorModelType = 0;

      // Initialize DREAM ACTION
    acActionDREAM dream(totChains,
                        totGenerations,
                        totalCR,
                        totCrossoverPairs,
                        dreamChainFileName,
                        dreamGRFileName,
                        dreamGRThreshold,
                        dreamJumpStep,
                        dreamGRPrintStep,
                        dreamRestartReadFileName,
                        dreamRestartWriteFileName,
                        usePriorFromFile,
                        priorFileName,
                        priorModelType);
  
    // Set the current model
    dream.setModel(myModel);

    // Run the MCMC Simulations
    dream.go();

    // Add Barrier
    MPI_Barrier(MPI_COMM_WORLD);

    // Post process results
    if(id == 0){
      bool debugMode = false;
      double burnInPercent = 0.1;
      dream.postProcess(debugMode,burnInPercent);
    }

  }catch(exception &e){
    // ERROR: TERMINATED!
    if(id == 0){
      printf("\n");
      printf("Msg: %s\n",e.what());
      printf("TERMINATED!\n");
    }
    // FINALIZE MPI CALL
    MPI_Finalize();
    return 0;
  }

  // COMPLETED
  if(id == 0){
    printf("\n");
    printf("COMPLETED!\n");
  }
  // FINALIZE MPI CALL
  MPI_Finalize();
  return 0;
}
