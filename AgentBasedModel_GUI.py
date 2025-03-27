from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.ModularVisualization import ModularServer

class RandomWalker(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        possible_moves = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_moves)
        self.model.grid.move_agent(self, new_position)

class RandomModel(Model):
    def __init__(self, N, width, height, max_steps=10):
        self.num_agents = N
        self.grid = MultiGrid(width, height, torus=True)
        self.schedule = RandomActivation(self)
        self.running = True  # Flag to indicate if the model is running
        self.step_count = 0  # Counter for steps
        self.max_steps = max_steps  # Maximum number of steps

        for i in range(self.num_agents):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            agent = RandomWalker(i, self)
            self.grid.place_agent(agent, (x, y))
            self.schedule.add(agent)

    def step(self):
        self.schedule.step()
        self.step_count += 1
        if self.step_count >= self.max_steps:
            self.running = False  # Stop the model

def agent_portrayal(agent):
    return {"Shape": "circle", "Color": "red", "Filled": "true", "Layer": 0, "r": 0.5}

# Add sliders to set parameters interactively
model_params = {
    "N": UserSettableParameter("slider", "Number of Robots", 5, 1, 20, 1),
    "width": 20, "height": 20,
    "max_steps": UserSettableParameter("slider", "Number of Steps", 10, 1, 100, 1), }

grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)
#server = ModularServer(RandomModel, [grid], "Robot Model", {"N": 10, "width": 10, "height": 10})
server = ModularServer(RandomModel, [grid], "Robot Model", model_params)

if __name__ == "__main__":
    server.launch()
