# -*- coding: utf-8 -*-
"""
Title: Agent based model - Agent Framework 
Created on Sat Sep 15 18:02:42 2018
@author: caro

Description: The agent framework contains the three classes specifying the abilities of each agent (sheep and wolves)
and how their are interacting with each other. 

Class Sheep: Generates sheep agents and defines actions of each agent and interaction inbetween agents of the same class.
Each sheep is moving across the field randomly, eating grass(the environment). Sheep who eat more
than 100 units become sick and will sicken up. Sick sheep empty their stored environment at the current location. Sheep also
have the ability to share the environment they collected (ate) with another sheep if the sheep is within a user-defined proximity.
Each sheep has been assigned a sex randomly. If a female sheep meets a male sheep (are within 5px radius) it will reproduce. After reproducing the female 
sheep will become unfertile for at least one iteration. After that the female sheep has a 5% chance of becoming fertile again.
To avoid overpopulation, sheep can be eaten by wolves. In addition if the sheep population exceeds 100 individuals a disease
outbreak will occur that has an 80% chance of killing any sheep.

Class Wolf: Defines the action exclusively concerning agents of the wolf class. Wolves are are trying to hunt the sheep. A like sheep, wolves are moving around independently 
and randomly every iteration of the model. Wolfs who do not manage to catch a sheep after
100 iteration of the model will starve and are removed from the field. Unlike sheep, wolves can not reproduce. 
However, there is a 1% chance of a new wolf appearing.


Class SheepPopControl: The third class of the agentframework contains control mechanisms to avoid the sheep population 
growing exponentially. This includes two function, the first will randomly introduce new wolves while the second is reducing
the sheep population through the introduction of a disease after the herd exceed a threshold. 

"""

import random

class Sheep:
    """Generate and define action for each sheep and the iteration of sheep within the herd.
    
    Args:
        environment (list): Nested list of integers. Each integer represent one pixel of the environment raster.
        herd (dict): Dictionary containing all sheep, their location and attributes.
        
    Attributes:
        y (float): Randomly assigned initial value of y coordinate.
        x (float): Randomly assigned initial value of x coordinate. 
        environment (list): Environment raster, passed through from model.
        store (int): Integer to store the amount of grass (environment) consumed by a sheep.
        herd (dict): Dictionary containing all sheep, their location and attributes.
        alive (boolean): Status of sheep. By default, all sheep are alive when they are created.
        sex (str): Randomly assigned sex, m = male, f= female. Each sheep has a 50% chance of being female.
        reproduce (boolean): States whether sheep can mate. Only females can mate. By default
        all females can mate at the start of the model.
            
    """
    
    def __init__(self, environment,herd):
        """Generate sheep."""
        self.y = random.randint(0,99) 
        self.x = random.randint(0,99)   
        self.environment =  environment
        self.store = 0 
        self.herd = herd
        self.alive = True
        self.sex = 'm' if random.random() <0.5 else 'f'
        self.reproduce = True if self.sex == 'f' else False

        
    def __str__(self):
        """Override __str__ to print location.
        
        Attributes:
            org_location (str): Original x and y coordinates of the sheep.
        
        """
        
        try:
            print(self.org_location)
            """Try to print the location of the sheep."""
        except:
            """ store original location of agents.
            
            If the sheep's attribute which stores the original location has not been 
            assigned, create the string variable and assign it the values of the x
            and y coordinate and print the location.
            
            """
            self.org_location =  str(self.y) + '/' + str(self.x)
            print('y: ' + str(self.y) + ' x: ' + str(self.x))

           
    def move(self):
        """Use random number to determine in what direction a sheep is moving. 
        
        Increment the x and y coordinate by 1 if the random number generated is greater 
        than 0.5. If the number is smaller than 0.5 subtract 1 from the current x or y 
        coordinate.
        
        """
        self.x = (self.x + 1) % 100 if random.random() < 0.5 else (self.x - 1) % 100
        self.y = (self.y + 1) % 100 if random.random() < 0.5 else (self.y - 1) % 100
        
            
    def distance_between(sheep_a, sheep_b):
        """Calculate the distance between two sheep.
        
        Calculate the distance between two points using the formula:
            sqrt((x1 - x2)^2 + (y1 - y2)^2)
            
        arg:
            sheep_a (dict): Dictionary containing location and attributes of a sheep.
            sheep_b (dict): Dictionary containing location and attributes of a sheep.
            
        return:
            float: Distance between sheep a and sheep b.
        
        """
        
        return (((sheep_a.x - sheep_b.x)**2) +  ((sheep_a.y - sheep_b.y)**2))**0.5
            
            
    def eat(self): 
        """Sheep eat the environment.
        
        Defines the amount of environment consumed by a sheep. By default a sheep
        eats 10 unit form the environment at the current location of the sheep.
        If the remaining environment is less than 10 units, the sheep will eat the
        remaining environment.
        
        Sheep who ate 100 or more units become sick and empty their environment at the
        current location of the sheep.
        
        """
        
        if self.environment[self.y][self.x] > 10:
            """If the environment is greater 10.""" 
            self.environment[self.y][self.x] -= 10
            """Subtract 10 from the environment."""
            self.store += 10
            """Add 10 to the sheep's store."""
        else:
            """If the environment is smaller 10."""
            self.store += self.environment[self.y][self.x]
            """Add the remaining environment to the sheep's store."""
            self.environment[self.y][self.x] = 0
            """Set the environment to 0."""
        if self.store>100:
            """ if agents ate more than 100, sicken up."""
            self.environment[self.y][self.x] += self.store
            """Add store to the environment."""
            self.store = 0
            """Reset store to 0."""
           
            
    def share_with_neighbours(self,neighbourhood):
        """Share environment with neighbours.
        
        Sheep within the user-defined neighbourhood share their store.
        
        arg: 
            neighbourhood (int): User-defined parameter, defining the distance within which sheep can share with each other.
                
        """
        
        for sheep in self.herd:
            if self.distance_between(sheep) <= neighbourhood:
                """If sheep is within the neighbourhood equally divide their combined store."""
                average = (self.store + sheep.store ) / 2
                self.store = average
                sheep.store = average
            
  
    def escape_wolves(self,wolves):
        """Try to escape wolf.
        
            Wolf can eat sheep within a radius of 5px. A sheep's probability of escaping the
            wolf depends on it's fitness (i.e store). Sheep with a store above 80 units and sheep
            are slow and will be caught by a wolf. Similarly, sheep with an empty store are weak
            and also don't manage to escape the wolf. 

            args:
                wolves (dict): Dictionary of the location and attributes of all wolves.
                
        """
        for wolf in wolves:
            if (self.x - 2.5 <= wolf.x <= self.x + 2.5) and (self.y - 2.5 <= wolf.y <= self.y + 2.5):
                """If sheep within 5px radius of a wolf check the sheep's store."""
                if self.store == 0 or self.store>=80:
                    """If the sheep's store is 0 or above 80 set set the alive status to false."""
                    self.alive = False
                    wolf.starving = 0
                    """Reset the wolf's starving countdown."""

    def mate(self):
        """Female sheep mate if meeting male sheep.
        
        If a female sheep is within a distance of 5px of a male sheep it will mate.
        After mating with a male sheep the female sheep becomes infertile for at least one iteration.
        After the first infertile iteration, the female sheep has a 5% chance of become fertile again.
        
        attr:
            mate (boolean): Indicates whether a sheep can mate. Is false by default.
        
        return: True if sheep did mate.
        
        """
        
        mate = False
        if self.reproduce:
            """Evaluate if sheep is fertile."""
            for sheep in self.herd:
                """Loop through the herd to find a male sheep within a distance of 5px."""
                if sheep.sex == 'm' and  self.distance_between(sheep) <= 5:
                    mate = True
                    """Change mating status to true."""
                    self.reproduce = False
                    """Change fertility status to false."""
                    break
                    """Break out of the loop as female sheep can only mate with one male per iteration."""
        elif self.sex =='f':
            """If female sheep is infertile use a randomly generate number to evaluate if sheep becomes fertile."""
            if random.random() <0.05:
                """Sheep has a 5% chance of becoming fertile."""
                self.reproduce = True
                """Change fertility status to true."""
        return mate


class Wolf:
    """Generate and define action for each wolf.

    Arg:
        wolves (dict): Dictionary containing all wolves and their attributes.
        
    Attributes:
        y (float): Randomly assigned initial value of y coordinate.
        x (float): Randomly assigned initial value of x coordinate. 
        starving (int): Environment raster, passed through from model.
        alive (boolean): Status of sheep. By default, all wolves are alive when they are created.
        wolves (dict): Dictionary containing all wolves and their attributes.
        
    """
    
    def __init__(self,wolves):
        self.y = random.randint(0,99) 
        self.x = random.randint(0,99)
        self.starving = 0
        self.alive = True
        self.wolves = wolves
        
    
    def hunt_sheep(self): 
        """Use a random number to determine in what direction a wolf is moving. 
        
        Increment the x and y coordinate by 2.5 if the random number generated is greater 
        than 0.5. If the number is smaller than 0.5 subtract 2.5 from the current x or y 
        coordinate.
        
        After every move, the risk of starving for the wolf increase. This is reflected
        by incrementing the starving variable by one. 
        
        """
        
        self.x = (self.x + 2.5) % 100 if random.random() < 0.5 else (self.x - 2.5) % 100
        self.y = (self.y + 2.5) % 100 if random.random() < 0.5 else (self.y - 2.5) % 100
        self.starving +=1
        
    def starve(self):
        """Wolves who do not catch a sheep for 100 iterations will starve."""
        if self.starving>=100:
            """If a wolf reaches 100 iteration without catching a sheep set the alive status to false."""
            self.alive = False
            
            
class SheepPopControl():
    """Intorduces control mechanisms to prevent exponential growth of sheep population."""
    
    def diease_outbreak(self,herd):
        """Prevent the sheep from growing exponentially by introducing diseases.
        
        If the sheep population exceeds 100 a disease outbreak will occur to diminish the 
        sheep population. 
        
        arg:
            herd (dict): Dictionary containing all sheep and their attributes of the herd.
        
        """
        
        if len(herd)>100:
            """If herd size exeeds 100, introduce disease."""
            for i in herd:
                """"Loop through each sheep in the herd."""
                if random.random() <0.8:
                    """Each sheep has an 80% chance of dying."""
                    i.alive = False
                    """Change alive status to false for dying sheep."""
             
    def new_wolfs(self):
        """Introduce new wolf.
        
        Generate a random number to decide if a new wolf is being introduced.
        
        return: True if new wolf is being introduced.
        
        """
        
        if random.random() <0.01: return True
            
                    
                
                
        
        
        