/*
 * Interactive selection exercise
 * 
 * (c) 2014 Sofian Audry -- info(@)sofianaudry(.)com
 *
 * Adapted from Daniel Shiffman The Nature of code
 * Interactive Selection
 * http://www.genarts.com/karl/papers/siggraph91.html
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

// Genetic population.
Population population;

// Factories for evolvable objects.
ArrayList<EvolvableObjectFactory> factories;

// Current factory.
int currentFactoryIdx;

// Next generation button.
Button button;

// Number of individuals.
static final int POPULATION_MAX = 10;

// A pretty high mutation rate here, our population is rather small we need to enforce variety
static final float MUTATION_RATE = 0.05;

void setup() {
  size(800,200);
  colorMode(RGB,1.0);
  
  // Creates the factories.
  currentFactoryIdx = 0;
  factories = new ArrayList<EvolvableObjectFactory>();
  factories.add(new TestFactory());
  
  // Initializes the population.
  initPopulation();
  
  // A simple button class
  button = new Button(15,150,160,20, "evolve new generation");
}

void draw() {
  background(1.0);
  
  // Display the objects.
  population.display();
  population.rollover(mouseX,mouseY);
  // Display some text
  textAlign(LEFT);
  fill(0);
  text("Generation #:" + population.getGenerations(),15,190);

  // Display the button
  button.display();
  button.rollover(mouseX,mouseY);

}

// Creates a population with a target phrase, mutation rate, and population max
void initPopulation() {
  population = new Population(MUTATION_RATE, POPULATION_MAX, factories.get(currentFactoryIdx));
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

void keyPressed() {
  if (key == '+') {
    currentFactoryIdx = (currentFactoryIdx + 1) % factories.size();
    initPopulation();
  }
}
