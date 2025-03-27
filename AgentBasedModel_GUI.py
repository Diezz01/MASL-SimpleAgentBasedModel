from mesa import Agent, Model
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import CanvasGrid


class Robot(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.x = self.random.randrange(self.model.grid.width)
        self.y = self.random.randrange(self.model.grid.height)

    def move(self):
        """Move the agent randomly."""
        possible_steps = self.model.grid.get_neighborhood((self.x, self.y), moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        self.x, self.y = new_position

    def step(self):
        """Move the agent during each step."""
        self.move()


class RobotModel(Model):
    def __init__(self, width, height, num_agents, num_steps):
        self.num_agents = num_agents
        self.num_steps = num_steps  # Store the chosen number of steps
        self.grid = MultiGrid(width, height, False)
        self.schedule = RandomActivation(self)
        self.running = False  # Keeps the simulation running

        for i in range(self.num_agents):
            a = Robot(i, self)
            self.schedule.add(a)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

        self.datacollector = DataCollector(agent_reporters={"X": "x", "Y": "y"})

    def step(self):
        """Advance the model by one step and stop after num_steps."""
        if self.schedule.steps < self.num_steps:
            self.datacollector.collect(self)
            self.schedule.step()
        else:
            self.running = False  # Stop the simulation after num_steps


def agent_portrayal(agent):
    """Define how agents will be drawn on the grid."""
    return {"Shape": "circle", "Color": "red", "Filled": "true", "Layer": 1, "r": 0.5,  # radius of the circle
    }


# Create a CanvasGrid for visualization
grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)

# Add sliders to set parameters interactively
model_params = {"width": 20, "height": 20,
    "num_agents": UserSettableParameter("slider", "Number of Robots", 5, 1, 20, 1),
    "num_steps": UserSettableParameter("slider", "Number of Steps", 10, 1, 100, 1), }

# Create and launch the server for visualization
server = ModularServer(RobotModel, [grid], "Robot Model", model_params)
server.port = 8523  # Default Mesa port
server.launch()
