from random import randint
from Main.Individual import Individual
from Main.System import System
from Main.Conversation import converse, add_memory_after_conversation, evaluate_speaking_tendencies
from Main.Memory import ConceptNode
from Main.Retrieve import new_retrieve
from Main.Query import generate_general_description

POPULATION = 5

# similar initialization as simulation
individuals = [Individual(i, f"person_{i + 1}") for i in range(POPULATION)]
land = [f"land {i}" for i in range(POPULATION)]
system = System(individuals, land)

# add some random memory for testing
    
for i, person in enumerate(individuals):
    person.memorystream.add_concept_node(ConceptNode(1,"rob",1,0,"rob",[1],10, f"person {i} rob person {(i + 1) % POPULATION}", 6))

individuals[2].memorystream.add_concept_node(ConceptNode(2,"rob",1,0,"rob",[1],10, "You REALLY want to produce luxury goods.", 6))

individuals[0].attributes["food"] = 25
individuals[2].attributes["land"] = 15


# topic = "talk about how much resources you have, and whether or not the distribution is fair."
topic = "Is there anything you think that needs to be changed? What will make your life better?"
# topic = "a policy that provides a 20 percent subsidy for people who create luxury goods"

conversation = converse(individuals, system, topic)


# add_memory_after_conversation(individuals, conversation)

# for person in individuals:
#     print(f"{person.attributes['name']}: {person.memorystream.concept_nodes[-1].description}", end="\n\n\n")