from Main.Individual import Individual
from Main.System import System
from Main.Conversation import converse, add_memory_after_conversation
from Main.Memory import ConceptNode

POPULATION = 5

# similar initialization as simulation
individuals = [Individual(i, f"person_{i + 1}") for i in range(POPULATION)]
land = [f"land {i}" for i in range(POPULATION)]
system = System(individuals, land)


# add some random memory for testing
for i, person in enumerate(individuals):
    person.memorystream.add_concept_node(ConceptNode(1,"rob",1,0,"rob",[1],10, f"person {i} rob person {(i + 1) % POPULATION}", 6))

individuals[3].memorystream.add_concept_node(ConceptNode(1,"rob",1,0,"rob",[1],10, "You REALLY want to produce luxury goods.", 6))

characteristics = [
    "SELDOM",
    "SOMETIMES",
    "SELDOM",
    "FREQUENT",
    "FREQUENT",
]

topic = "talk about the world you live in"
# topic = "choose between a policy that provides a 20 percent subsidy for people who create luxury goods or a policy that reduces people's income by 5 percent"

conversation = converse(individuals, system, topic, characteristics)

# add_memory_after_conversation(individuals, conversation)

# for person in individuals:
#     print(f"{person.attributes['name']}: {person.memorystream.concept_nodes[-1].description}", end="\n\n\n")