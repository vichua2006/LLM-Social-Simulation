from Main.Individual import Individual
from Main.System import System
from Main.AutoGen import converse, add_memory_after_conversation
from Main.Memory import ConceptNode

POPULATION = 5

# similar initialization as simulation
individuals = [Individual(i, f"person_{i}") for i in range(POPULATION)]
land = [f"land {i}" for i in range(POPULATION)]
system = System(individuals, land)


# add some random memory for testing
for i, person in enumerate(individuals):
    person.memorystream.add_concept_node(ConceptNode(1,"rob",1,0,"rob",[1],10, f"person {i} rob person {(i + 1) % POPULATION}", 6))

characteristics = [
    "gets picked a lot",
    "gets picked a lot",
    "does not get picked often",
    "gets picked a lot",
    "does not get picked often",
] # gpt generated personalities

# topic = "talk about the world you live in"
topic = "a policy that provides a 20 percent subsidy for people who create luxury goods."

conversation = converse(individuals, system, topic, characteristics)

# add_memory_after_conversation(individuals, conversation)

# print(individuals[0].memorystream.concept_nodes[-1].description )