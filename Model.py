from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import numpy as np
import random


class HouseholdAgent(Agent):
    """ An agent with a randomly drawn initial harvest."""
    def __init__(self, unique_id, model, lineage):
        super().__init__(unique_id, model)
        self.lineage = lineage
        self.food = self.model.standard_deviation * np.random.randn(1) + self.model.mean
        if self.food > 75:
            self.fed = 1
        else:
            self.fed = 0

    def eat(self):
        if self.food > 75:
            self.fed = 1
        else:
            self.fed = 0

    def harvest(self):
        self.food = self.model.standard_deviation * np.random.randn(1) + self.model.mean

    def step(self):
        self.harvest()
        self.eat()
        reproduce(self, self.model)
        die(self, self.model)


def reproduce(parent_agent, model):
    rep_prob = .45
    if random.uniform(0, 1) < rep_prob:
        model.num_agents = model.num_agents + 1
        a = HouseholdAgent(model.num_agents, model, str(parent_agent.unique_id))
        model.schedule.add(a)


def die(agent, model):
    death_prob = .45
    if random.uniform(0, 1) < death_prob:
        model.schedule.remove(agent)


def count_fed(model):
    number_fed = sum([agent.fed for agent in model.schedule.agents])
    return number_fed/model.schedule.get_agent_count()


class MoneyModel(Model):
    """A model with some number of agents."""
    def __init__(self, N, sd, mean):
        self.standard_deviation = sd
        self.mean = mean
        self.num_agents = N
        self.schedule = RandomActivation(self)

        # Create agents
        for i in range(self.num_agents):
            a = HouseholdAgent(i, self, str(i))
            self.schedule.add(a)

        self.datacollector = DataCollector(
            model_reporters={"Percent Households Fed": count_fed},
            agent_reporters={"ID": lambda a: a.unique_id, "Lineage": lambda a: a.lineage}
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
