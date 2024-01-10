from Main.Individual import Individual

POPULATION = 5

individuals = [Individual(i, f"person {i}") for i in range(POPULATION)]

person1 = individuals[0]

person1.update_agent_prompt("Your name is bob")



print(person1.agent.system_message)