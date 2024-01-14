import Main.Memory

from Main.Individual import Individual
from Main.Memory import ConceptNode

person = Individual(0,"a")

rob_memory = ConceptNode(1,"rob",1,0,"rob",[1],10,"person 0 rob person 1", 6)
#farm_memory = ConceptNode(2,"farm",2, 0, "farm", [], 10, "person 0 farms and receives 10 units of food", 3)
#chat_memory = ConceptNode(3, "chat", 2, 0, "chat", [1,2], 0, "person 0 said \'Good Morning\' to person 1,2", 5)

person.memorystream.add_concept_node(rob_memory)
#person.memorystream.add_concept_node(rob_memory)
#person.memorystream.add_concept_node(rob_memory)

#print(person.memorystream)

print(person.memorystream.emotion)
