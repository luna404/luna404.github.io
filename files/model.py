# -*- coding: utf-8 -*-
"""
Title: Agent based model - Model
Created on Sat Sep 15 18:02:05 2018
Author: caro

Description: Example of an agent based model using wolves and sheep. 
The script will generate an animated plot using matplotlib's pyplot module displaying 
a herd of sheep grazing the field and being chased by wolves.

More information on the abilities of the two agent groups (sheep and wolves) can be found in the
description of the agentframework. 

User input parameters If the the script is run through the command line, the user has the ability to define the following
parameters:

	num_of_sheep (int): Number of sheep at the beginning of the model.
	num_of_wolves (int): Number of sheep at the beginning of the model.
	num_of_iterations (int): Number of iterations after which the model will be updated.
	neighbourhood (int): Size of the neighbourhood in which sheep can share grass.
	max_iterations (int): Maximum number of iterations after which the model will stop.  

"""


import sys
import matplotlib.pyplot as plt
import matplotlib.animation as anm
import agentframework as af
import random as rnd


global carry_on 
environment = [] 
"""list: Empty list to store environment raster data."""
herd = []
"""list: Empty list to store location and attributes for each sheep."""
wolves = []
"""list: Empty list to store location and attributes for each wolf."""



ctrl = af.SheepPopControl()
"""Import class Sheep_pop_control from agentframework."""

for i in sys.argv:
    """Define model parameters.
    
        num_of_sheep (int): Number of sheep at the beginning of the model.
        num_of_wolves (int): Number of sheep at the beginning of the model.
        num_of_iterations (int): Number of iterations after which the model will be updated.
        neighbourhood (int): Size of the neighbourhood in which sheep can share grass.
        max_iterations (int): Maximum number of iterations after which the model will stop.
        
    """ 
    if i in ['Help','help','h']:
        """If user requests help print input requirements and exists the script."""
        print('The program requires four arguments\nnumber of agents (int)\nnumber of wolfs (int)\n' +
          'number of iterations (int)\n maximum number of iterations (int)\nsize of neighbourhoood (int)')
        sys.exit()
    else:
        """ Define model parameters based on user input value.
        
            Assign default values for missing input parameters.            
            Throw error message if user submits variable type other than integer.
        """
        try:
            num_of_sheep = int(sys.argv[1]) if len(sys.argv)>1 else 10
            num_of_wolves = int(sys.argv[2]) if len(sys.argv)>2 else 2
            num_of_iterations = int(sys.argv[3]) if len(sys.argv)>3 else 10
            neighbourhood = int(sys.argv[5]) if len(sys.argv)>4 else 20 
            max_iterations = int(sys.argv[4]) if len(sys.argv)>5 else 1000
            
        except ValueError:
            print('The program requires four arguments\nnumber of sheep (int)\nnumber of wolves (int)\n' +
            'number of iterations (int)\n maximum number of iterations (int)\nsize of neighbourhoood (int)')


with open("in.txt", "r", newline='\n') as file: 
    """ Read environment raster data from file.
        
        rowlist (list): temporary list to store environment raster data        
        Loop through each line in the file and add data to rowlist. 
        
    """
    for line in file:
        rowlist  = []
        line = line.replace('\n','').split(',')
        """Remove line-breaks and convert comma separated values into a list. """
        for value in (line):
            """Loop through each value in line."""
            rowlist.append(int(value))
            """Add each value to the list."""
        environment.append(rowlist)
        """Add raster to the environment list."""
    file.close()


for i in range(num_of_sheep):
    """Generate sheep herd.
    
       Loop through the number of sheep to be generated and add each sheep 
       to the herd list. Use the Sheep class from the agentframework to 
       create the x/y coordinates for each sheep.
       
       The __str__ class has been overridden to print the original location 
       of each sheep.
       
    """
    herd.append(af.Sheep(environment,herd))
    herd[i].__str__()
    """Print original location of each sheep."""

   
#: Make the wolves
for j in range(num_of_wolves):
    """Generate wolves.
    
    Loop through the number of wolves to be generated and add each wolf 
    to the list of wolves. Use the Wolf class from the agentframework to 
    create the x/y coordinates for each wolf.
    
    """
    wolves.append(af.Wolf(wolves))

#: Generate plot layout (figure)
fig =plt.figure(figsize=(7, 7))
"""Figure: Define figure size."""
ax = fig.add_axes([0, 0, 1, 1])
"""Axes: Define figure axes."""
fig.patch.set_facecolor('#dedede')
"""Set figure background color to grey."""                        

                       
def update(frame_number):
    """Update the model"""
    fig.clear()   
    """Clear figure before rebuilding it."""
    
    for j in range(num_of_iterations):        
        try:
            for j in range(len(wolves)):
                """Loop through the list of wolves."""
                wolves[j].wolves = rnd.sample(wolves[j].wolves, k=len(wolves[j].wolves)) 
                wolves[j].hunt_sheep()
                """Wolf moves to hunt sheep."""
                wolves[j].starve()
                """If wolf is not able to catch sheep, it will starve"""
               
                if wolves[j].alive == False:
                    """ remove dead wolves """
                    wolves.pop(j)
            
            for i in range(len(herd)): 
                """Loop through the sheep herd."""
                herd[i].escape_wolves(wolves)
                """Sheep tries to escape wolf."""
                if herd[i].alive == False:
                    """Remove dead sheep."""
                    herd.pop(i)
                else:
                    herd[i].herd = rnd.sample(herd[i].herd, k=len(herd[i].herd)) 
                    """reorder sheep randomly."""
                    herd[i].move()
                    """Sheep moves."""
                    herd[i].eat()
                    """Sheep eats and sickens up with overeaten."""
                    herd[i].share_with_neighbours(neighbourhood)
                    if herd[i].mate():
                        """If female sheep try to mate."""
                        herd.append(af.Sheep(environment,herd))
                                            
            # control sheep population 
            if ctrl.new_wolves(): wolves.append(af.Wolf(wolves))
            """There is a 1% chance a new wolf is introduced."""
            ctrl.disease_outbreak(herd)
            """ If sheep herd exceeds 100, a disease outbreak occurs. Sheep have a 20% chance of surviving the disease."""
        except IndexError:
            pass 

    #: Map environment, sheep and wolves
    pos = plt.imshow(environment,cmap='summer_r')
    """Plot environment raster."""
    plt.colorbar(pos, orientation="horizontal")
    """Add color bar to the figure. """
    
    for i in range(len(herd)):
        """Loop through the herd and plot sheep."""
        plt.scatter(herd[i].x, herd[i].y,color ='white')
    for j in range(len(wolves)):
        """Loop through the wolves and plot wolves."""
        plt.scatter(wolves[j].x, wolves[j].y, color ='red')
   
    #: Style plot
    plt.scatter(102, 102,color ='white',label="Sheep #("+ str(len(herd)) +')')
    plt.scatter(102, 102,color ='red',label="Wolf #("+ str(len(wolves)) +')')
    """Create two fakes points outside the plot area. These points will be used for the legend."""

    plt.legend(loc=9, bbox_to_anchor=(0.5, -0.1),ncol=2,frameon=False) 
    """ Add plot legend."""
        
    plt.xlim(0, 99)
    plt.ylim(0, 99)
    """ restrict plot area to 100px """
    
    plt.suptitle('Sheep and Wolves', fontsize=20,color='#0d6d13')
    plt.title('(Agent Based Model)', fontsize=12,loc='center',color='#4b4f4c')
    """ Add plot title and subtitle """


def gen_function(b = [0]):
    """Define stopping point for the model.
    
    The animation will stop when any of the three criteria are true:
    1. Sheep have eaten all the grass (Environment is zero).
    2. All sheep have died.
    3. The maximum number of iterations has been reached. 
    
    """
    a = 0
    env_sum = 0
    for i, row in enumerate(environment):
        """Loop through the first 100  square pixels to calculate the remaining environment."""
        env_sum +=sum(row[:100])
        if i == 99:
            break
    carry_on = True if len(herd)>0 and env_sum>0 else False 
    """Boolean: If neither conditions 1 and 2 are set carry on variable to true."""
    while  (a < max_iterations) & (carry_on): 
        yield a			#: Returns control and waits next call.
        a = a + 1


animation = anm.FuncAnimation(fig, update, frames=gen_function, repeat=False)
"""Create animated plot. Continues to update the plot until stopping criteria was met.""" 

plt.show()
"""Display the plot."""



#: Write out the environment as a file.
with open('environment_out.txt', "w") as f1,open('environment_row_sum.txt', "a")  as f2: 
    """Write the environment raster to files. 
    
    Write the raster data to a new file or overwrite the existing file if present.
    Append the sum of each row to a second file. 
    
    """           
    for line in environment:
        f1.write(str(line)+'\n')
        """ write the value of each pixel in a line to file."""
        f2.write(str(sum(line))+'\n')
        """ write sum of each line to file."""
f1.close(), f2.close()
"""Close both files."""

try:
	for i in range(num_of_sheep):
		""" print start and end location of each agent """
		print('start:' + herd[i].org_location + ' end: ' + str(herd[i].y) +'/' + str(herd[i].x))
except:
	pass


print('End of script.')
