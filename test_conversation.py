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
    "You are enduring and optimistic, always maintaining a positive outlook. You are shy",
    "You are detail-oriented, with a strong focus on order and quality.",
    "You are generous and community-minded, always willing to help others.",
    "You are business-savvy and strategic in trade and negotiations.",
    "You are determined and hardworking, with a strong sense of dedication to your work.",
] # gpt generated personalities

topic = "a policy that offers 20 percent subsidy to those who produce luxury goods."
# topic = "talk about who recently robbed you. simply list off who robbed you, do not go in depth or apologise"

conversation = converse(individuals, system, topic, characteristics)

add_memory_after_conversation(individuals, conversation)

print(individuals[0].memorystream.concept_nodes[-1].description)