import random
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector


class Robot(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.x = self.random.randrange(self.model.grid.width)
        self.y = self.random.randrange(self.model.grid.height)

    def move(self):
        """Move the agent randomly."""
        possible_steps = self.model.grid.get_neighborhood(
            (self.x, self.y), moore=True, include_center=False
        )
        '''print("Robot id: ", self.unique_id, "\n")
        print("Actual Position: ", (self.x, self.y), "\n")
        print(possible_steps,"\n")'''
        new_position = self.random.choice(possible_steps)
       # print(new_position,"\n")
        self.model.grid.move_agent(self, new_position)
        
        self.x, self.y = new_position
       # print("New Position: ", (self.x, self.y), "\n")

    def step(self):
        """Move the agent during each step."""
        self.move()


class RobotModel(Model):
    def __init__(self, width, height, num_agents):
        self.num_agents = num_agents
        # Create a MultiGrid of specified width and height (2D grid)
        self.grid = MultiGrid(width, height, False)  # True means toroidal (wraps around)
        self.schedule = RandomActivation(self)

        for i in range(self.num_agents):
                a = Robot(i, self)
                self.schedule.add(a)
                
                # Randomly place each agent on the grid
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                self.grid.place_agent(a, (x, y))
            
        # Data collector (optional, to collect data during the simulation)
        self.datacollector = DataCollector(
            agent_reporters={"X": "x", "Y": "y"}
        )

    def step(self):
        """Advance the model by one step."""
        self.datacollector.collect(self)
        self.schedule.step()

model = RobotModel(width=20, height=20, num_agents=5)

for i in range(5):
    model.step()
    
    # Print the positions of all agents after each step
    print(f"Step {i+1}:")
    for agent in model.schedule.agents:
        print(f"Agent {agent.unique_id} Position: ({agent.x}, {agent.y})")


