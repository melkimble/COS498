
import oscP5.*;

// a single tracked face from FaceOSC
class FaceOSC {
  
  // num faces found
  int found;
  
  // pose
  float poseScale;
  PVector posePosition = new PVector();
  PVector poseOrientation = new PVector();
  
  // gesture
  float mouthHeight, mouthWidth;
  float eyeLeft, eyeRight;
  float eyebrowLeft, eyebrowRight;
  float jaw;
  float nostrils;
  
  FaceOSC() {}

  // parse an OSC message from FaceOSC
  // returns true if a message was handled
  boolean parseOSC(OscMessage theMessage) {
    
    if(theMessage.checkAddrPattern("/found")) {
        found = theMessage.get(0).intValue();
        return true;
    }      
          
    // pose
    else if(theMessage.checkAddrPattern("/pose/scale")) {
        poseScale = theMessage.get(0).floatValue();
        return true;
    }
    else if(theMessage.checkAddrPattern("/pose/position")) {
        posePosition.x = theMessage.get(0).floatValue();
        posePosition.y = theMessage.get(1).floatValue();
        return true;
    }
    else if(theMessage.checkAddrPattern("/pose/orientation")) {
        poseOrientation.x = theMessage.get(0).floatValue();
        poseOrientation.y = theMessage.get(1).floatValue();
        poseOrientation.z = theMessage.get(2).floatValue();
        return true;
    }
    
    // gesture
    else if(theMessage.checkAddrPattern("/gesture/mouth/width")) {
        mouthWidth = theMessage.get(0).floatValue();
        return true;
    }
    else if(theMessage.checkAddrPattern("/gesture/mouth/height")) {
        mouthHeight = theMessage.get(0).floatValue();
        return true;
    }
    else if(theMessage.checkAddrPattern("/gesture/eye/left")) {
        eyeLeft = theMessage.get(0).floatValue();
        return true;
    }
    else if(theMessage.checkAddrPattern("/gesture/eye/right")) {
        eyeRight = theMessage.get(0).floatValue();
        return true;
    }
    else if(theMessage.checkAddrPattern("/gesture/eyebrow/left")) {
        eyebrowLeft = theMessage.get(0).floatValue();
        return true;
    }
    else if(theMessage.checkAddrPattern("/gesture/eyebrow/right")) {
        eyebrowRight = theMessage.get(0).floatValue();
        return true;
    }
    else if(theMessage.checkAddrPattern("/gesture/jaw")) {
        jaw = theMessage.get(0).floatValue();
        return true;
    }
    else if(theMessage.checkAddrPattern("/gesture/nostrils")) {
        nostrils = theMessage.get(0).floatValue();
        return true;
    }
    
    return false;
  }
 
  // get the current face values as a string (includes end lines)
  String toString() {
    return "found: " + found + "\n"
           + "pose" + "\n"
           + " scale: " + poseScale + "\n"
           + " position: " + posePosition.toString() + "\n"
           + " orientation: " + poseOrientation.toString() + "\n"
           + "gesture" + "\n"
           + " mouth: " + mouthWidth + " " + mouthHeight + "\n"
           + " eye: " + eyeLeft + " " + eyeRight + "\n"
           + " eyebrow: " + eyebrowLeft + " " + eyebrowRight + "\n"
           + " jaw: " + jaw + "\n"
           + " nostrils: " + nostrils + "\n";
  }
  
};