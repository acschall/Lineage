from Model import *
import matplotlib.pyplot as plt
import networkx as nx

# Give the model the number of agents you want
# and the standard deviation/mean of the normal
# distribution you want to draw harvests from
model = MoneyModel(100, 30, 90)

# Specify how many steps you want
steps = 10


for i in range(steps):
    print('Step: ' + str(i))
    print(model.schedule.get_agent_count())
    model.step()

# Plot the number of households fed
# num_fed = model.datacollector.get_model_vars_dataframe()
# num_fed.plot()

list_of_agents = model.datacollector.get_agent_vars_dataframe()


def create_edges(graph):
    for i in range(1, steps):
        for agent in list_of_agents.xs(i, level="Step").index.values:
            agent_info = list_of_agents.xs((i, agent), level=["Step", "AgentID"])
            lineage = agent_info["Lineage"].values[0]
            graph.add_edge(int(lineage), agent)


# Plot the family trees
G = nx.DiGraph()
for i in range(steps):
    G.add_nodes_from(list_of_agents.xs(i, level="Step")[list_of_agents.xs(i, level="Step")["Generation"] == i].index.values,
                     generation=i)

create_edges(G)
values = [G.node[node]['generation'] for node in G.nodes]
pos = nx.nx_pydot.graphviz_layout(G, prog='neato')
plt.figure(figsize=(14, 14))
plt.axis('equal')
nx.draw(G, pos, node_size=20, alpha=0.5, node_color=values, with_labels=False, cmap=plt.get_cmap('jet'))
sm = plt.cm.ScalarMappable(cmap=plt.get_cmap('jet'), norm=plt.Normalize(vmin=0, vmax=steps))
sm._A = []
plt.colorbar(sm)

plt.show()
