import AgentBasedModel
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import VisualizationElement


# Define how to portray each agent on the grid
def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",  # Shape of the agent
        "r": 0.5,           # Radius of the circle (visual size)
        "Filled": "true",    # Filled circle
        "Color": "blue"      # Color of the agent
    }
    portrayal["x"] = agent.x
    portrayal["y"] = agent.y
    return portrayal

# Create a grid (10x10) and define the size of the canvas (500x500)
canvas_element = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

# Create a visualization object and add the canvas module
from mesa.visualization.ModularVisualization import ModularVisualization

# Setup the model parameters
model_params = {"width": 10, "height": 10, "num_agents": 5}
visualization = ModularVisualization()
visualization.add_module("Canvas", canvas_element)
visualization.load_model(AgentBasedModel.RobotModel, model_params)

# Launch the visualization app (set port)
visualization.port = 8521
visualization.launch()
