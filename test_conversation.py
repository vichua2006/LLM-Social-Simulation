from random import randint
from Main.Individual import Individual
from Main.System import System
from Main.Conversation import converse, add_memory_after_conversation, evaluate_speaking_tendencies
from Main.Memory import ConceptNode
from Main.Retrieve import new_retrieve

POPULATION = 5

# similar initialization as simulation
individuals = [Individual(i, f"person_{i + 1}") for i in range(POPULATION)]
land = [f"land {i}" for i in range(POPULATION)]
system = System(individuals, land)

# big 5 personality traits
openness = [
    "Very consistent, cautious, prefers routine and familiarity.",
    "Somewhat cautious, but occasionally open to new experiences.",
    "Balanced, sometimes open to new experiences and sometimes prefers consistency.",
    "Generally open to new experiences, curious, and inventive.",
    "Highly open to new experiences, very curious, and highly imaginative."
]

conscientiousness = [
    "Very easy-going, may tend to be disorganized and careless.",
    "Somewhat easy-going but can be organized when necessary.",
    "Balanced, generally organized, but can be flexible.",
    "Generally very organized and efficient, with a strong sense of duty.",
    "Extremely organized, detail-oriented, and efficient, possibly to the point of being a perfectionist."
]

extraversion = [
    "Very solitary and reserved, prefers to be alone.",
    "Somewhat reserved, but can be sociable in familiar settings.",
    "Balanced, enjoys social interaction but also values solitude.",
    "Generally outgoing and energetic, enjoys being around people.",
    "Extremely outgoing, loves being in social settings, and thrives on interactions."
]

agreeableness = [
    "More analytical and detached, may come off as less compassionate.",
    "Somewhat compassionate but tends to be analytical.",
    "Balanced, can be both compassionate and analytical depending on the situation.",
    "Generally friendly, compassionate, and cooperative.",
    "Extremely friendly, empathetic, and always ready to help others."
]

neuroticism = [
    "Very secure, confident, and emotionally stable.",
    "Mostly secure but can occasionally experience stress or emotional instability.",
    "Balanced, can be sensitive to stress but generally remains stable.",
    "Generally sensitive and can be prone to emotional ups and downs.",
    "Highly sensitive, often nervous, and prone to emotional challenges."
]



all_traits = [openness, conscientiousness, extraversion, agreeableness, neuroticism]
personalities = []

random_testing = True
if (random_testing):
    for i in range(POPULATION):
        descriptions = []
        for trait in all_traits:
            descriptions.append(trait[randint(0, 4)])
        personalities.append("\n".join(descriptions))

else:
    personalities = extraversion
 
# add some random memory for testing
    
for i, person in enumerate(individuals):
    person.memorystream.add_concept_node(ConceptNode(1,"rob",1,0,"rob",[1],10, f"person {i} rob person {(i + 1) % POPULATION}", 6))

individuals[3].memorystream.add_concept_node(ConceptNode(2,"rob",1,0,"rob",[1],10, "You REALLY want to produce luxury goods.", 6))


# topic = "people who want to produce luxury goods."
topic = "a policy that provides a 20 percent subsidy for people who create luxury goods"


conversation = converse(individuals, system, topic, personalities)

add_memory_after_conversation(individuals, conversation)

for person in individuals:
    print(f"{person.attributes['name']}: {person.memorystream.concept_nodes[-1].description}", end="\n\n\n")