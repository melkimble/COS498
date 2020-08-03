/**
 * Title: ASSIGNMENT 2 - The Geneticator
 * Name: Melissa Kimble
 * Date: 2018-03-19
 * Description: Must have FaceOSC.exe and WekinatorProject_Hw2 running. The FaceOSC class parses input from FaceOSC.exe and sends it to Wekinator with 
 * sendOSC. Wekinator is trained to categorically recognize whether your head is to the left, right, or center, and if your mouth is
 * opened or closed. Opening and closing your mouth will evolve a new generation, and tilting your head will select the pattern to add fitness to.
 */
//
// a template for receiving face tracking osc messages from
// Kyle McDonald's FaceOSC https://github.com/kylemcdonald/ofxFaceTracker
//
// this example includes a class to abstract the Face data
//
// 2012 Dan Wilcox danomatika.com
// for the IACD Spring 2012 class at the CMU School of Art
//
// adapted from from Greg Borenstein's 2011 example
// http://www.gregborenstein.com/
// https://gist.github.com/1603230
//
import oscP5.*;
import netP5.*;

OscP5 oscP5;
NetAddress myRemoteLocation;
Population population; // Genetic population.
Button button; // Next generation button.

// our FaceOSC tracked face dat
FaceOSC face = new FaceOSC();

boolean send; // either true or false
boolean mouthOpened; // whether mouth is opened or closed
ArrayList<EvolvableObjectFactory> factories; // Factories for evolvable objects.
int currentFactoryIdx; // Current factory.
float mouth_osc;
float headtilt_osc;
int[] mouths = new int[10];
int i = 0;

static float MOUTH_POS; // declaring the output value, which gets filled in the Osc Message theMessage
static float HEAD_POS = -1; // declaring the output value, which gets filled in the Osc Message theMessage

static final int POPULATION_MAX = 4; // Number of individuals.
static final float MUTATION_RATE = 0.08; // A pretty high mutation rate here, our population is rather small we need to enforce variety

void setup() {
  size(1300,400);  
  colorMode(RGB,1.0);

  oscP5 = new OscP5(this, 12000);
  myRemoteLocation = new NetAddress("127.0.0.1",6448);
  send = false;
  mouthOpened = false;

  // Creates the factories.
  currentFactoryIdx = 0;
  factories = new ArrayList<EvolvableObjectFactory>();
  factories.add(new FaceFactory());
  
  // Initializes the population.
  initPopulation();
  
  // A simple button class
  button = new Button(15,350,160,20, "evolve new generation");
}

void draw() {  
  background(1.0);
  //  stroke(0);
  text("To start/stop press [spacebar]. Must have FaceOSC and Wekinator running.", 25, 15);
  if (send == true) {
    /* Every time send is true, then it will call sendOsc(); */
    sendOsc();
    // fill the mouths array
    mouthOpenedFill();
    headtiltFill();
    population.headover();
    fill(255, 0, 0); // this is red; the internal red color
    ellipse(35, 25, 15, 15); // red dot in the center of the screen
    text("Sending...", 45, 30);
  }
  
  /*
  if(face.found > 0) {
    print(face.toString());
  }
  */
  
  // Display the objects.
  population.display();
  population.rollover(mouseX,mouseY);
  
  // Display some text
  textAlign(LEFT);
  fill(0);
  text("Generation #:" + population.getGenerations(),15,390);

  // Display the button
  button.display();
  button.rollover(mouseX,mouseY); 
}

void mouthOpenedFill(){
  // array of mouth values sent from FaceOSC through Wekinator
  mouths[i] = int(mouth_osc);
  //println(mouths[i]);
  MOUTH_POS = mouth_osc;
   // if mouth is open generate a new population (same as clicking the button)
  if (i > 0) {
    // if i is 1 or greater, then grab the value of the array before i and at i. If the sequence is
    // 2 and 1, then mouth was opened then closed. If opened and closed, "click" and generate new population.
    if (mouths[i-1] == 2 & mouths[i] == 1) {
      mouthOpened = !mouthOpened;
    }
  } else {
    // if i is 0, then the previous value is the end of the array since the array is constantly refilled sequentially from
    // 0 to 9.
    if (mouths[mouths.length-1] == 2 & mouths[i] == 1) {
      mouthOpened = !mouthOpened; 
    } 
  }  
  if (mouthOpened) {
    // if mouth opened then closed, then submit fitness values for selection and create new population.
    population.selection();
    population.reproduction(); 
    mouthOpened = !mouthOpened;
  }
  i++;
  if (i == 10) i = 0;
}

void headtiltFill(){
  // if head is tilted to the left, add fitness and hightlight left-boxes
  if (headtilt_osc == 3) {
    HEAD_POS = HEAD_POS-0.01;
  }
  // if head is in center, stop on currently selected box and continue highlighting and adding fitness
  if (headtilt_osc == 2) {
    HEAD_POS = floor(HEAD_POS);
  }
  // if head is tilted to the right, add fitness and highlight right-boxes
  if (headtilt_osc == 1) {
    HEAD_POS = HEAD_POS+0.01;
  }
  // if HEAD_POS is greater than the number of boxes, then set it to the number of boxes (right-most box)
  if (HEAD_POS>POPULATION_MAX-1) HEAD_POS = POPULATION_MAX-1;
  // if HEAD_POS is less than 0, set it back to 0, the left-most box
  if (HEAD_POS<0) HEAD_POS = 0;
 // println(HEAD_POS);
 // print(", head tilt: ");
 // print(headtilt_osc);
}

// Creates a population with a target phrase, mutation rate, and population max
void initPopulation() {
  population = new Population(MUTATION_RATE, POPULATION_MAX, factories.get(currentFactoryIdx));
}

void keyPressed() {
  /* if the key that is pressed == spacebar (' ' means spacebar) */
  if(key == ' ') {
    /* this is a clever way to toggle the value of send! 
    If send is true, then send will be false, and vice versa. */      
   send = !send;            
  }
  if (key == '+') {
    currentFactoryIdx = (currentFactoryIdx + 1) % factories.size();
    initPopulation();
  }
}

// If the button is clicked, evolve next generation
void mousePressed() {
  if (button.clicked(mouseX,mouseY)) {
    population.selection();
    population.reproduction();
  }
}
void mouseReleased() {
  button.released();
}

// OSC CALLBACK FUNCTIONS

void sendOsc() {
  /* in the following different ways of creating osc messages are shown by example
  "/test" is the address - We want this to be the same as Inputs: OSC message in wekinator. We 
  just need it to be the same - "/wek/inputs"*/
  OscMessage myMessage = new OscMessage("/wek/inputs");
  /* wekinator expects floats, so we have to cast mouseX as a float */
  myMessage.add((float) face.poseScale); /* add a float to the osc message */
  myMessage.add((float) face.posePosition.x); /* add a float to the osc message */
  myMessage.add((float) face.posePosition.y); /* add a float to the osc message */
  myMessage.add((float) face.poseOrientation.x); /* add a float to the osc message */
  myMessage.add((float) face.poseOrientation.y); /* add a float to the osc message */
  myMessage.add((float) face.poseOrientation.z); /* add a float to the osc message */
  myMessage.add((float) face.mouthWidth); /* add a float to the osc message */
  myMessage.add((float) face.mouthHeight); /* add a float to the osc message */
  myMessage.add((float) face.eyeLeft); /* add a float to the osc message */
  myMessage.add((float) face.eyeRight); /* add a float to the osc message */
  myMessage.add((float) face.eyebrowLeft); /* add a float to the osc message */
  myMessage.add((float) face.eyebrowRight); /* add a float to the osc message */
  myMessage.add((float) face.jaw); /* add a float to the osc message */
  myMessage.add((float) face.nostrils); /* add a float to the osc message */

  /* send the message */
  oscP5.send(myMessage, myRemoteLocation); 
}

void oscEvent(OscMessage theMessage) {
  face.parseOSC(theMessage);
  // you have to use .equals to do a string comparison
  if (theMessage.addrPattern().equals("/wek/outputs")) {
    //theOscMessage is a single value that we know, because we set output to 1
    // we have to put .floatValue() to explicitly tell it to expect a float value ...
    // this value will be between 0 and 1 (wekinator slider)
    mouth_osc = theMessage.get(0).floatValue(); // declared in beginning
    headtilt_osc = theMessage.get(1).floatValue(); // declared in beginning
  }
}
