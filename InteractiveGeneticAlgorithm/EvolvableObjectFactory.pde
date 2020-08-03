/**
 * This abstract class represents an object that can create a new EvolvableObject.
 */
abstract class EvolvableObjectFactory {
  
  // Creates and returns an EvolvableObject.
  abstract EvolvableObject create(DNA dna, float x, float y);
}
