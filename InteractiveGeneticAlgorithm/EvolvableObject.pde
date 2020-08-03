// Modified by Sofian Audry
// The Nature of Code
// Daniel Shiffman
// http://natureofcode.com
/**
 * This class represents an object that can be evolved using a genetic algorithm.
 */
abstract class EvolvableObject {
  DNA dna;            // The object's DNA
  float fitness;      // How good is this object?
  float x, y;         // Position on screen
  int size;           // Size of square enclosing face
  boolean rolloverOn; // Are we rolling over this face?

  // Bounding rectangle.
  Rectangle r;

  // Create a new face
  EvolvableObject(DNA dna_, float x_, float y_) {
    dna = dna_;
    x = x_; 
    y = y_;
    fitness = 1;
    size = 70;
    r = new Rectangle(int(x-size/2), int(y-size/2), size, size);
  }
  
  float getFitness() {
    return fitness;
  }

  DNA getDNA() {
    return dna;
  }

  // Increment fitness if mouse is rolling over face
  void rollover(int mx, int my) {
    if (r.contains(mx, my)) {
      rolloverOn = true;
      fitness += 0.25;
    } else {
      rolloverOn = false;
    }
  }

  // Display the object.
  void display() {
    pushMatrix();
    translate(x, y);
    displayObject();
    popMatrix();
    
    displayBox();
    displayFitness();
  }
  
  // This method should be overriden by subclasses to display the actual object
  abstract void displayObject();
  
  // Draws the bounding box
  void displayBox() {
    pushMatrix();
    translate(x, y);
    stroke(0.25);
    if (rolloverOn) fill(0, 0.25);
    else noFill();
    rectMode(CENTER);
    rect(0, 0, size, size);    
    popMatrix();
  }
  
  // Displays fitness value
  void displayFitness() {
    textAlign(CENTER);
    if (rolloverOn) fill(0);
    else fill(0.25);
    text(int(fitness), x, y+55);
  }
  
}
