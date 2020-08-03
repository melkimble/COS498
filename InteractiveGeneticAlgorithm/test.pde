// Modified by Sofian Audry
// The Nature of Code
// Daniel Shiffman
// http://natureofcode.com

// Interactive Selection
// http://www.genarts.com/karl/papers/siggraph91.html

// The class for our "face", contains DNA sequence, fitness value, position on screen

// Fitness Function f(t) = t (where t is "time" mouse rolls over face)

class Test extends EvolvableObject {

  // Create a new face
  Test(DNA dna_, float x_, float y_) {
    super(dna_, x_, y_);
  }

  // Display the face
  void displayObject() {
    // We are using the face's DNA to pick properties for this face
    // such as: head size, color, eye position, etc.
    // Now, since every gene is a floating point between 0 and 1, we map the values
    int unit = size/15; // a unit of measure
    float r          = map(dna.genes[0],0,1,0,size);
    color c          = color(dna.genes[1],dna.genes[2],dna.genes[3]);

    float eye_y      = map(dna.genes[4],0,1,0,unit);
    float eye_x      = map(dna.genes[5],0,1,0,2*unit);
    float eye_size   = map(dna.genes[5],0,1,0,2*unit);
    color eyecolor   = color(dna.genes[4],dna.genes[5],dna.genes[6]);
    
    color mouthcolor = color(dna.genes[7],dna.genes[8],dna.genes[9]);
    float mouth_y    = map(dna.genes[5],0,1,0,5*unit);
    float mouth_x    = map(dna.genes[5],0,1,-5*unit,5*unit);
    float mouthw     = map(dna.genes[5],0,1,0,10*unit);
    float mouthh     = map(dna.genes[5],0,1,0,2*unit);
    
    float hatm_y     = map(dna.genes[4],0,1,-7*unit,7*unit);
    float hatm_x     = map(dna.genes[5],0,1,0,unit);
    
    float hatb_y     = map(dna.genes[4],0,1,-5*unit,5*unit);
    float hatb_x     = map(dna.genes[5],0,1,0,unit);
    
    float hatm_h     = map(dna.genes[0],0,1,0,1.5*unit);
    
    float hatb_w     = map(dna.genes[0],0,1,0,size);
    float hatb_h     = map(dna.genes[0],0,1,0,2*unit);
    
    float hat_size   = map(dna.genes[0],0,1,0,size/2);
    float hatcolor   = color(dna.genes[6],dna.genes[7],dna.genes[8]);

    // Once we calculate all the above properties, we use those variables to draw rects, ellipses, etc.
    noStroke();

    // Draw the head
    fill(c);
    ellipseMode(CENTER);
    ellipse(0, 0, r, r);
    
    // Draw the hat about 50% of the time.
    if (hat_size > (unit*5)/2) {
      // draw the top of the hat
      fill(hatcolor);
      rectMode(CENTER);
      rect(hatm_x, hatm_y, hat_size, hat_size);
      
      // draw the middle band of the hat
      fill(mouthcolor);
      rectMode(CENTER);
      rect(hatm_x, hatm_y, hat_size, hatm_h);
      
     // draw the bottom of the hat
      fill(hatcolor);
      rectMode(CENTER);
      rect(hatb_x, hatb_y, hatb_w, hatb_h);
    }

    // Draw the eyes
    fill(eyecolor);
    rectMode(CENTER);
    rect(-eye_x, -eye_y, eye_size, eye_size);
    rect( eye_x, -eye_y, eye_size, eye_size);

    // Draw the mouth
    fill(mouthcolor);
    rectMode(CENTER);
    rect(mouth_x, mouth_y, mouthw, mouthh);
  }

}

class TestFactory extends EvolvableObjectFactory {
  
  EvolvableObject create(DNA dna, float x, float y) {
    return new Test(dna, x, y);
  }
}
