// The Nature of Code
// Daniel Shiffman
// http://natureofcode.com

// Interactive Selection
// http://www.genarts.com/karl/papers/siggraph91.html

//import java.awt.Rectangle;

class Button {
  Rectangle r;  // Button's rectangle
  String txt;   // Button's text
  boolean clickedOn;  // Did i click on it?
  boolean rolloverOn; // Did i rollover it?
  boolean mouthOpen; // was my mouth open? (if it's open, then 'click button')

  Button(int x, int y, int w, int h, String s) {
    r = new Rectangle(x,y,w,h);
    txt = s;
  }

  void display() {
    // Draw rectangle and text based on whether rollover or clicked
    rectMode(CORNER);
    stroke(0); noFill();
    // if mouse is hovering over the square, background is grey.
    if (rolloverOn) fill(0.5);
    if (MOUTH_POS==1) fill(255);

    // if it's clicked on or mouth open, box background is black.
    if (clickedOn) fill(0);
    if (MOUTH_POS==2) fill(0);
    
    rect(r.x,r.y,r.width,r.height);
    float b = 0.0;
    if (clickedOn) b = 1;
    else if (rolloverOn) b = 0.2;
    else b = 0;
    fill(b);
    textAlign(LEFT);
    text(txt,r.x+10,r.y+14);
  }
   
  // Methods to check rollover, clicked, or released (must be called from appropriate
  // Places in draw, mousePressed, mouseReleased
 
  boolean rollover(int mx, int my) {
    if (r.contains(mx,my)) rolloverOn = true;
    else rolloverOn = false;
    return rolloverOn;
  }
  boolean clicked(int mx, int my) {
    if (r.contains(mx,my)) clickedOn = true;
    return clickedOn;
  }
  void released() {
    clickedOn = false;
  }

}