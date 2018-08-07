from Model import *
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx

# Give the model the number of agents you want
# and the standard deviation/mean of the normal
# distribution you want to draw harvests from
model = MoneyModel(100, 30, 90)

# Specify how many steps you want
for i in range(3):
    print('Step: ' + str(i))
    print(model.schedule.get_agent_count())
    model.step()


# Plot the number of households fed
# num_fed = model.datacollector.get_model_vars_dataframe()
# num_fed.plot()

list_of_agents = model.datacollector.get_agent_vars_dataframe()
# with pd.option_context('display.max_rows', None, 'display.max_columns', 3):
    # print(list_of_agents)
    # print(list_of_agents.xs(0, level="Step")["Lineage"])
    # print(list_of_agents.xs((0, 1), level=['Step', 'Step'])["Lineage"])
    # print(list_of_agents(12, level="AgentID")["Lineage"])

G = nx.DiGraph()

# Add the initial generation of agents to the graph
for i in range(len(list_of_agents.index)):
    if i in list_of_agents.xs(0, level="Step")["ID"]:
        agent_info = list_of_agents.xs((0, i), level=["Step", "AgentID"])
        lineage = agent_info["Lineage"].values[0]
        ID = agent_info["ID"].values[0]
        G.add_node(ID)
    if i in list_of_agents.xs(1, level="Step")["ID"]:
        agent_info = list_of_agents.xs((1, i), level=["Step", "AgentID"])
        lineage = agent_info["Lineage"].values[0]
        ID = agent_info["ID"].values[0]
        G.add_node(ID)
        G.add_edge(ID, lineage)




# pos = nx.circular_layout(G, dim=2, scale=1)
# pos = nx.drawing.nx_agraph.graphviz_layout(G, prog='dot')
plt.figure(figsize=(8, 8))
plt.axis('equal')
nx.draw(G, node_size=20, alpha=0.5, node_color="blue", with_labels=False)

plt.show()
