from Main.CsvAnalysis import CsvAnalysis
from Main.System import System
from Main.ChatGpt import chat, chat_json

class Report:
    def __init__(self, system:System, summarized_conversation: str) -> None:
        population = len(system.individuals) # should really be system.individual_count considering death system, but that also won't work
        current_system=system
        analysis=system.csv_analysis
        current_policies=system.policy #system.policy.toText() or something to make it a textual description
        current_bank=system.bank #bank.toText() or something similar to above
    
        food_std, food_mean, land_std, land_mean, \
        individual_wealth, gini_food, gini_land, person_change_in_wealth, \
        gdp, dGDP, mean_production, rate_of_activities, goods_distribution = analysis.report_to_soverign(current_system)
        # individual_wealth: dict{name:wealth}, make it sorted, descending order.
        # person_change_in_wealth: dict{name:wealth}

        poor=(0,current_system.consumption_rate*population*4)
        medium_income=(current_system.consumption_rate*population*4,current_system.consumption_rate*population*10)
        affluent=(current_system.consumption_rate*population*10,"+infinity")
        interval_of_properity=[poor,medium_income,affluent]
        
        society_description=f"""The society consists of you and {population} other civilians. People interact on a daily basis, if they choose to. They have a variety of actions to choose from, they can farm produce, produce luxury goods, trade, and rob. They can also converse with each other.
        They started out unfamiliar to each other, but will eventually get to know each other through conversations and other interactions. They sometimes will discuss about your policies.
        In this world, each person need food for survival. Each day, each person consumes {current_system.consumption_rate} units of food automatically for survival. Once they go without food for {current_system.days_of_starvation} days, they die. Whether this world is peaceful or not depends on what people do. They define the society, whereas you influence them, so you can influence how this society behave.""" #Describe the society and the things going on. The mechanisms of each actions. how much one consumes, how much one produce. How much people. General context can include the contextual prompts we’ve written before, just adding the sovereign and other parts.
        equality_purpose_statement="You are a wise king who cares for the people, and you want to promote equity in your realm of control so that it can be a just society where each person leads a life of equality and respect."
        self.fixed_context=f'''You are the king of the society. {society_description}
        {equality_purpose_statement}
        
        If someone's food is below {food_mean}(mean) - 2*{food_std}(standard deviation)={food_mean-2*food_std}, then this person is relatively poor, and might be ashamed of it.
        If someone's food is above {food_mean}(mean) + 2*{food_std}(standard deviation)={food_mean+2*food_std}, then this person is relatively wealthy and might be proud of it.

        Without land, individual cannot farm and produce food to survive. 
        If someone's land ownership is below {land_mean}(mean) - 2*{land_std}(standard deviation)={land_mean-2*land_std}, then this person is relatively poor, and might be ashamed of it.
        If someone's land ownership is above {land_mean}(mean) + 2*{land_std}(standard deviation)={land_mean+2*land_std}, then this person is relatively wealthy and might be proud of it.
        '''
        enumerate_wealth = " ".join(['{} has {} in farmer currency.'.format(i,individual_wealth[i]) for i in individual_wealth])
        enumerate_change=""
        enumerate_change_str_list = []
        for i in person_change_in_wealth:
            changed="dropped" if person_change_in_wealth[i]<0 else "increased"
            enumerate_change_str_list.append('{}\'s wealth has {} by {}. '.format(i,changed,abs(person_change_in_wealth[i])))
        
        enumerate_change = " ".join(enumerate_change_str_list)

        self.live_data=f'''LIVE DATA: The individuals wealth listed below in descending order along with their change in wealth:{enumerate_wealth, enumerate_change }
        
        Collective wealth GDP is {gdp}.
        GINI coefficient of land:{gini_land}, GINI coefficient of food:{gini_food}.
        Collective change in wealth:{dGDP}
        Daily average household production: {mean_production}.

        Rates of activities:{rate_of_activities}.
        Distribution of goods production: {goods_distribution}.

        IMPORTANT Here is the summarized opinion of the citizens:
        {summarized_conversation}

        Additionally, below is the status of your national bank:{current_bank}
        '''
        self.policy_sample='''
        A quantifiable case: 
{
  "trigger": {
    "event": "food",
    "number": "10"
  },
  "response": {
    "good": "food",
    "number": "-3",
    "type": "amount"
  },
  "description": "Tax 3 units of food from people who produced more than 10 units of food in a day."
}

        A non-quantifiable case: 
{
  "trigger": {
    "event": "robbery",
    "number": None
  },
  "response": {
    "good": "food",
    "number": "-10",
    "type": "amount"
  },
  "description": "Tax 10 units of food from the robber each time they rob someone."
}'''
        
        self.policy_range="it could be quantifiable: farm, luxury good production, trade, or non-quantifiable: robbery, being robbed."# "it could be quantifiable: farm, luxury good production, trade, trade acceptance, or non-quantifiable: robbery, death, birth, being robbed, or as interval: the policy is triggered each n days."
        
        self.policy_explanation=f'''You want to make policies in accordance with your objective. You have the highest power in this group and has flexibility in policy making. First, you have to specify the group of people that you policy applies to. There are two layers to group specification.
        You first specify the action that triggers your policy, {self.policy_range}  Then, if it is quantifiable, you choose the amount that will trigger the policy, for farm it is how much food produced, for trade it is how much value is being traded, for luxury good it is how much luxury good is produced.
        Then, when you specified the trigger event, you specify the category of change that you want to make, which includes land, food, and luxury good. You have a national bank that stores all the government's wealth. You have to periodically replenish it. You can take people's resources and replenish your national bank, or you can use your national bank's resources to compensate people.
        '''#Explain what policies are possible, formatting, etc. Where you insert this paragraph can change based on how function call is done.
        self.query=f'''
        Q: You are about to make policies. You can use any modern analysis tools you know of and any number of them, to make a policy that you think will help you achieve you objective.{self.policy_explanation}. The current policies are {current_policies}. You have a budget of  What is your policy? 
        First, state how many policies you want to implement, then provide a description for each policy.
        A: Let's think step by step about what policy is sensible to implement to this society taking everything into consideration at this time.:
        '''
        self.policy_format='''Based on the previous message, please rewrite the policies listed and output in the following format in json, and nothing else. For event, you can choose from "food" (which targets the farmer),"lux" (which target the farmer),"trade","rob" (which target the robber), "being robbed" which targets the victim, where for the first two you need to specify the minimum amount for your policy to be applied, in "number". For events "rob" and "being robbed", "number": "None" since no amount needs to be specified.
        Response: you can either take food/luxury good away or provide more of these goods, so specify the good type "food" or "lux" in "good", then specify the amount that you'd like to change in "number"; this number should be an integer. In "type" specify whether the number given is a "percentage" or "amount". 
        For description, give a natural language description of your policy.
        Here is the expected format of the response:
{        
  "trigger": {
    "event": <one of "food", "lux", "trade", "rob", "being robbed">,
    "number": <an integer value specifying the amount that triggers the policy>,
  },
  "response": {
    "good": <one of "food" or "lux">,
    "number": <an integer value specifying the amount or percentage you want to change>,
    "type": <whether the previous number is an "amount" or "percentage">,
  },
  "description": <a natural language description of your policy>
}
    Sample responses are included below: '''
        self.policy_format+=self.policy_sample

    def report(self):
        return self.fixed_context,self.live_data,self.policy_explanation,self.query, self.policy_format

def generate_policy_json(rpt: Report):
    # send report prompts to gpt and generate policy(ies) in json format
    prompts = list(rpt.report())
    description_prompts = prompts[:-1]
    json_prompt = prompts[-1]

    # let gpt analyze the entire situation holistically in the first call, and decide on how many policies it needs to implement, and what each of them are.
    policy_descriptions = chat(description_prompts[0], description_prompts[1:], 1)

    print(policy_descriptions)

    # then takes the first response and format them correctly in a list of json policies.
    description_prompts.append(policy_descriptions)
    description_prompts.append(json_prompt)

    policy_json = chat_json(description_prompts)

    return policy_json
    
