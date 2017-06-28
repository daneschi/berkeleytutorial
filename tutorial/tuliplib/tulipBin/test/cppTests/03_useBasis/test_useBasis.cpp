// ====================
// TUTORIAL EXCERCISE 6
// Basiss
// ====================

# include "uqTypes.h"
# include "uqConstants.h"

# include "uqBasis.h"
# include "uqPolyBasis.h"
# include "uqOrthoPolyBasis.h"
# include "uqMWBasis.h"

# include "lpnUtils.h"

using namespace std;

// =============
// MAIN FUNCTION
// =============
int main(int argc, char* argv[]){

  // Set Parameters
  int steps = 50;
  double currOrder = 3;

  // Set Storage Matrix
  stdMat results;
  results.resize(steps);
  for(int loopA=0;loopA<steps;loopA++){
    results[loopA].resize(5);
  }

  try{

    // SIMPLE POLYNOMIALS
    uqBasis* polyIntMonomial;
    uqBasis* polyIntLegendre;
    uqBasis* polyIntHermite;

    polyIntMonomial = new uqPolyBasis(kPolyMonomials);
    polyIntLegendre = new uqPolyBasis(kPolyLegendre);
    polyIntHermite  = new uqPolyBasis(kPolyHermite);

    double currentLoc = 0.0;
    for(int loopA=0;loopA<steps;loopA++){
      currentLoc = loopA/(double)(steps - 1);
      results[loopA][0] = ((uqPolyBasis*)polyIntMonomial)->eval(currentLoc,currOrder);
      results[loopA][1] = ((uqPolyBasis*)polyIntLegendre)->eval(currentLoc,currOrder);
      results[loopA][2] = ((uqPolyBasis*)polyIntHermite)->eval(currentLoc,currOrder);
    }

    // ORTHOGONAL POLYNOMIALS
    uqBasis* orthoPolyInt;

    // Define the number of quadrature points
    int currLevel = 10;

    // Define the Uniform Measure
    stdVec measureAtQuadPoints(currLevel);
    for(int loopA=0;loopA<currLevel;loopA++){
      measureAtQuadPoints[loopA] = 1.0;
    }

    orthoPolyInt = new uqOrthoPolyBasis(currOrder+1,currLevel,measureAtQuadPoints);
    
    currentLoc = 0.0;
    for(int loopA=0;loopA<steps;loopA++){
      currentLoc = loopA/(double)(steps - 1);
      results[loopA][3] = ((uqOrthoPolyBasis*)orthoPolyInt)->eval(currentLoc,currOrder);
    }

    // MULTIWAVELETS
    uqBasis* mwInt;

    mwInt = new uqMWBasis(currOrder+1,currLevel);

    currentLoc = 0.0;
    for(int loopA=0;loopA<steps;loopA++){
      currentLoc = loopA/(double)(steps - 1);
      results[loopA][4] = ((uqMWBasis*)mwInt)->EvalMotherMW(currentLoc,currOrder);
    }

    // PRINT RESULT MATRIX
    writeTableToFile(string("tutorial_06.out"),results);
  
  }catch(exception &e){
    // ERROR: TERMINATED!
    printf("\n");
    printf("Msg: %s\n",e.what());
    printf("TERMINATED!\n");
    return 0;
  }

  // COMPLETED
  printf("\n");
  printf("COMPLETED!\n");
  return 0;
}
