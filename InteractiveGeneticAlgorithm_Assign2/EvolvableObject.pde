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
  int id;             // id of the rectangle
  int size;           // Size of square enclosing face
  boolean rolloverOn; // Are we rolling over this face?
  boolean headoverOn; // is my head tilted to the left?
  
  // Bounding rectangle.
  Rectangle r;

  // Create a new face
  EvolvableObject(DNA dna_, int id_, float x_, float y_) {
    dna = dna_;
    id = id_;
    x = x_; 
    y = y_;
    fitness = 1;
    size = 280;
    r = new Rectangle(int(x-size/2), int(y-size/2), size, size);
  }
  
  float getFitness() {
    return fitness;
  }
  
  float getId() {
    return id;
  }

  DNA getDNA() {
    return dna;
  }

  // Increment fitness if mouse is rolling over face
  void rollover(int mx, int my) {
    if (r.contains(mx, my)) {
      rolloverOn = true;
      // if you hover over the square, add 0.25 to 'fitness' every cycle
      fitness += 0.25;
     // print(id);
    } else {
      rolloverOn = false;
    }
  }
  
  // Increment fitness if head is tilted to the left or right
  void headover() {
    if (floor(HEAD_POS) == float(id)) {
      headoverOn = true;
      // if you hover over the square, add 0.25 to 'fitness' every cycle
      fitness += 0.25;
    } else {
      headoverOn = false;
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
    if (headoverOn) fill(0, 0.25);
    else noFill();
    rectMode(CENTER);
    rect(0, 0, size, size); 
    popMatrix();
  }
  
  // Displays fitness value
  void displayFitness() {
    textAlign(CENTER);
    if (rolloverOn) fill(0);
    if (headoverOn) fill(0);
    else fill(0.25);
    // add 
    text(int(fitness), x, y+165);
  }
  
}