// Modified by Sofian Audry
// The Nature of Code
// Daniel Shiffman
// http://natureofcode.com

// Interactive Selection
// http://www.genarts.com/karl/papers/siggraph91.html

// The class for our "face", contains DNA sequence, fitness value, position on screen

// Fitness Function f(t) = t (where t is "time" mouse rolls over face)

class Face extends EvolvableObject {
  color pattern[][];
  
  // Create a new face
  Face(DNA dna_, int id_, float x_, float y_) {
    super(dna_, id_, x_, y_);
    pattern = new color[size][size];
    
    // Once we calculate all the above properties, we use those variables to draw rects, ellipses, etc.
   // noStroke();
    // adapted from https://www.funprogramming.org/53-Create-a-pattern-by-drawing-150000-pixels.html
  //  colorMode(HSB, 10);
    
    //int unit = size/15; // a unit of measure. Syntax: map(value, start1, stop1, start2, stop2)
    float vertx      = floor(map(dna.genes[0],0,1,0,30)); 
    float verty      = floor(map(dna.genes[1],0,1,0,20));
    float sinx       = floor(map(dna.genes[2],0,1,0,13));
    float siny       = floor(map(dna.genes[3],0,1,0,23));
    float gcolor     = map(dna.genes[4],0,1,0,1);
    float bcolor     = map(dna.genes[5],0,1,0,1);
    float tancos     = floor(map(dna.genes[6],0,1,0,1));
    
    for(int x = -140; x < size/2; x++) {      
      for(int y = -140; y < size/2; y++) {
        float v;
        if (tancos == 1) {
          v = sin(x/vertx + y/verty) * sin(x/sinx - y/siny);
        } else {
          v = cos(x/vertx + y/verty) * cos(x/sinx - y/siny);
        }
        float rcolor = map(v, -1, 1, 0, 1);
        pattern[x + 140][y + 140] = color(rcolor, gcolor, bcolor);
      }      
    }
  }
  
  // Display the face
  void displayObject() {
    int unit = size/28; // a unit of measure. Syntax: map(value, start1, stop1, start2, stop2)
    
    rectMode(CENTER);
        // Once we calculate all the above properties, we use those variables to draw rects, ellipses, etc.
    noStroke();
    // adapted from https://www.funprogramming.org/53-Create-a-pattern-by-drawing-150000-pixels.html
   // colorMode(HSB, 10);
    
    for (int x = 0; x < size; x=x+unit) {
      for (int y = 0; y < size; y=y+unit) {
        fill(pattern[x][y]);
        rect(x - 140, y - 140, unit, unit);
      }
    }
    
    
    /*
    // We are using the face's DNA to pick properties for this face
    // such as: head size, color, eye position, etc.
    // Now, since every gene is a floating point between 0 and 1, we map the values
    int unit = size/15; // a unit of measure. Syntax: map(value, start1, stop1, start2, stop2)
    float vertx     = floor(map(dna.genes[0],0,1,0,30)); 
    float verty     = floor(map(dna.genes[1],0,1,0,20));
    float sinx      = floor(map(dna.genes[2],0,1,0,13));
    float siny      = floor(map(dna.genes[3],0,1,0,23));
    float gbhsb     = floor(map(dna.genes[4],0,1,0,8));
    float tancos     = floor(map(dna.genes[5],0,1,0,1));


    // Once we calculate all the above properties, we use those variables to draw rects, ellipses, etc.
    noStroke();
    // adapted from https://www.funprogramming.org/53-Create-a-pattern-by-drawing-150000-pixels.html
    colorMode(HSB, 10);

    // draw random pattern based on sin or tangent function by cycling through all x,y locations within the 
    // bounding box.
    for(int x = -130; x < size/2.15; x++) {      
      for(int y = -130; y < size/2.15; y++) {
        float v;
        if (tancos == 1) {
          v = sin(x/vertx + y/verty) * sin(x/sinx - y/siny);
        } else {
          v = tan(x/vertx + y/verty) * tan(x/sinx - y/siny);
        }
        float redhsb = map(v, -1, 1, 0, 10);
        fill(redhsb,gbhsb,gbhsb);
        rectMode(CENTER);
        rect(x, y, unit, unit);
      }      
    }
    */
  }
}

class FaceFactory extends EvolvableObjectFactory {
  
  EvolvableObject create(DNA dna, int id, float x, float y) {
    return new Face(dna, id, x, y);
  }
}