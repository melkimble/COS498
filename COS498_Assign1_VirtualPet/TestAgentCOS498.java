// COS 498 
// Hiearchical Finite State Machine, Behavior Trees
// 

//limited range of named states
enum State {
	SLEEPING,
	HAPPY,
	ANGRY
}	
class Agent {
	final float BASE_CHANGE =0.01;
	// current state
	State state;
	float energy;
	//boolean isSleeping;
	//boolean isAngry;
	Agent(){
		energy = 0;
		state=State.SLEEPING;
		isSleeping = true;
	}
	
// safe way to set the range of a value
void setEnergy(float newEnergy) {
	// if you try to set it greater than 1 or less than 0, it will constrain it to these values.
	energy = constrain(newEnergy, 0, 1);
}

float getEnergy(){return energy;}

void update() {
	// state: sleeping
	//if(isSleeping) {
	if(state==State.SLEEPING)
		updateSleeing();
	// State: happy
	else if (state==State.HAPPY)
		updateHappy();
	else 
		updateAngry();
}
void updateSleeping() {
	// update or actions
	setEnergy(getEnergy()+BASE_CHANGE);
	// transition check - checks if need to change transition, 
	// which is applied in the next loop
	if (mousePressed) 
		if (getEnergy() > 0.8)
			state=State.HAPPY;
		else
			state.State=ANGRY;
	//energy += 0.01; -- increase energy by 1% each loop
	//if(mousePressed && energy > 0.8)
	//if(mousePressed && getEnergy() > 0.8)
	//	state=State.HAPPY;
	//else if (mousePressed && getEnergy() <0.8)
	//	state=State.ANGRY;
		//isSleeping=false;
}

void updateHappy() {
	setEnergy(getEnergy() - BASE_CHANGE);
	//if(mousePressed)
	//	setEnergy(getEnergy() + BASE_CHANGE/2);
	if (getEnergy() <0.2)
		state = State.SLEEPING;
	else if (!mousePressed)
		state = State.ANGRY;
}

void updateAngry() {
	setEnergy(0);
	if(mousePressed)
		setEnergy(get
}	
	
void draw() {
	if (state == State.SLEEPING)
		fill(0);
	else if (state == State.ANGRY)
		fill(255,255,255)
	else
		fill(0,200,0);
	ellipse(width/2, height/2, 50, 50);
	fill(255);
	--in the corner
	textSize(50);
	text((int)(energy*100),width/4, height/4);
	}
}

Agent myAgent;

