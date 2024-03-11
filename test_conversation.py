from random import randint
from Main.Individual import Individual
from Main.System import System
from Main.Conversation import converse, add_memory_after_conversation, summarize_conversation
from Main.Memory import ConceptNode
from Main.Retrieve import new_retrieve
from Main.Query import generate_general_description
from Main.Soverign import Report
from Main.Simulation import simulate, initialize

POPULATION = 5

# similar initialization as simulation
individuals = [Individual(i, f"person_{i + 1}") for i in range(POPULATION)]
land = [f"land {i}" for i in range(POPULATION)]
system = System(individuals, land)

# add some random memory for testing
    
for i, person in enumerate(individuals):
    person.memorystream.add_concept_node(ConceptNode(1,"rob",1,0,"rob",[1],10, f"person {i} rob person {(i + 1) % POPULATION}", 6))

individuals[2].memorystream.add_concept_node(ConceptNode(2,"rob",1,0,"rob",[1],10, "You REALLY want to produce luxury goods.", 6))


# for i in individuals:
#     i.attributes["food"] = 1
#     i.attributes["land"] = 0

# individuals[0].attributes["food"] = 1000

# print([i.attributes['food'] for i in system.individuals])
# topic = "talk about how much resources you have, numerically specific, and compare it to the amount others have"
topic = "Share your perspectives on your life and the society. Are you happy? How is your daily life? Are you satisfied with it? What will make your life better?"
# topic = "a redistribution of resources for equality"

conversation = converse(individuals, system, topic)

# conversation = [{'content': "\n    System Message: Now, several members of the society have gathered to discuss their opinion about the world that they live in.\n    The topic is: Share your perspectives on your life and the society. Are you happy? How is your daily life? Are you satisfied with it? What will make your life better?\n    You are allowed to debate with other people for your opinions.\n    DO NOT use modern terms that are too abstract for the world setting.\n    Limit each response to 50 words.\n\n    Here are several examples of how your should structure your responses:\n    Example response 1: I'm quite satisfied with my life. As someone who mainly produces food from my land of 10 units, I'm self-sufficient. I also trade my food with others in exchange for luxury good. Consuming them brings me a lot of pleasures.\nExample response 2: I felt my life sucked. I have only 2 unit of land and produce food from there. I often felt starved. I can hardly sustain myself. I need more food to survive. If possible I also wish to get some luxury good for my pleasure.\nExample response 3: I have a mixed feeling about my life. I have a lot of food and land so I don't have to worry about my survival too much. But I have a poor ability to produce luxury good. I have to trade luxury goods from others with my food, which is quite costly. I hope the trade would be more fairer.\nExample response 4: I'm not quite happy with the society. Although I have 100 units of food and 50 units of luxury good, Someone else in our society has 500 units of food and 300 units of luxury good. That's not fair. I want to have more resources as well.\n    ", 'role': 'user', 'name': 'system'}, {'content': 'I am content with my life. I have 8 units of food and 5 units of land. I enjoy the pleasures of food and the security of my land. To improve, I aim to increase my social position by acquiring more resources than others.', 'role': 'user', 'name': 'person_1'}, {'content': 'I feel satisfied with my life. With 10 units of food and 6 units of land, I am self-sufficient. I prioritize my own pleasures and social position. To enhance my life, I will continue to focus on acquiring more resources and maintaining my advantage over others.', 'role': 'user', 'name': 'person_2'}, {'content': 'I am content with my life. I have 12 units of food and 7 units of land. I prioritize my own sensual pleasures and social position. To improve, I will focus on securing future goods, such as increasing my social position and acquiring luxury goods.', 'role': 'user', 'name': 'person_4'}, {'content': 'I feel dissatisfied with my life. I have 4 units of food and 3 units of land. I was recently robbed by person_4, which has affected my resources. To improve my situation, I need to focus on increasing my food and land to ensure my survival and social position.', 'role': 'user', 'name': 'person_5'}, {'content': 'As person_6, I am quite content with my life. With 30 units of food and 14 units of land, I feel secure and well-off. I prioritize my own pleasures and social position. To enhance my life, I will continue to focus on maintaining my advantage over others and securing future goods.', 'role': 'user', 'name': 'person_6'}, {'content': 'I am person_7. I am satisfied with my life, having 4 units of food and 3 units of land. I prioritize my own sensual pleasures and social position. To improve, I will focus on acquiring more resources and increasing my social position relative to others.', 'role': 'user', 'name': 'person_7'}, {'content': 'TERMINATE', 'role': 'user', 'name': 'person_3'}]

print(summarize_conversation([conversation]))

# add_memory_after_conversation(individuals, conversation)

# for person in individuals:
#     print(f"{person.attributes['name']}: {person.memorystream.concept_nodes[-1].description}", end="\n\n\n")