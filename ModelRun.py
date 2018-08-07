from Model import *
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx

# Give the model the number of agents you want
# and the standard deviation/mean of the normal
# distribution you want to draw harvests from
model = MoneyModel(100, 30, 90)

# Specify how many steps you want
steps = 3


for i in range(steps):
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


''' NEED TO ADD CODE THAT SORTS OUT WHICH AGENTS ARE IN STEP ONE BUT NOT STEP 0'''


def create_edges(graph):
    for i in range(1, steps):
        for agent in list_of_agents.xs(i, level="Step")["ID"].values:
            agent_info = list_of_agents.xs((i, agent), level=["Step", "AgentID"])
            lineage = agent_info["Lineage"].values[0]
            ID = agent_info["ID"].values[0]
            graph.add_edge(int(ID), int(lineage))




# Add the relationships to the graph
# for i in range(len(list_of_agents.index)):
#     for j in range(steps):
#         if i in list_of_agents.xs(j, level="Step")["ID"]:
#             agent_info = list_of_agents.xs((j, i), level=["Step", "AgentID"])
#             lineage = agent_info["Lineage"].values[0]
#             ID = agent_info["ID"].values[0]
#             print(lineage)
#             print(ID)
            # G.add_edge(ID, lineage)
    # if i in list_of_agents.xs(0, level="Step")["ID"]:
    #     agent_info = list_of_agents.xs((0, i), level=["Step", "AgentID"])
    #     lineage = agent_info["Lineage"].values[0]
    #     ID = agent_info["ID"].values[0]
    #     G.add_node(ID)
    # if i in list_of_agents.xs(1, level="Step")["ID"]:
    #     agent_info = list_of_agents.xs((1, i), level=["Step", "AgentID"])
    #     lineage = agent_info["Lineage"].values[0]
    #     ID = agent_info["ID"].values[0]
    #     G.add_node(ID)
    #     G.add_edge(ID, lineage)

G = nx.Graph()
G.add_nodes_from(list_of_agents.xs(0, level="Step")["ID"].values)
G.add_nodes_from(list_of_agents.xs(1, level="Step")["ID"].values)
G.add_nodes_from(list_of_agents.xs(2, level="Step")["ID"].values)
create_edges(G)


# pos = nx.circular_layout(G, dim=2, scale=1)
# pos = nx.drawing.nx_agraph.graphviz_layout(G, prog='dot')
shells = [list_of_agents.xs(0, level="Step")["ID"].values,
          list_of_agents.xs(1, level="Step")["ID"].values,
          list_of_agents.xs(2, level="Step")["ID"].values]
pos = nx.shell_layout(G, shells)
plt.figure(figsize=(8, 8))
plt.axis('equal')
nx.draw(G, pos, node_size=20, alpha=0.5, node_color="blue", with_labels=False)

plt.show()
