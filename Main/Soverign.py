from CsvAnalysis import CsvAnalysis
class Report:
    def __init__(self, population:int, file_name:str) -> None:
        analysis=CsvAnalysis(population,file_name)
        
        interval_of_properity=["poor","medium income","affluent"] #DATA: to be swapped with integer two touple values.
        society_description=None #Describe the society and the things going on. The mechanisms of each actions. how much one consumes, how much one produce. How much people. General context can include the contextual prompts we’ve written before, just adding the sovereign and other parts.
        equality_purpose_statement="You are a wise king who cares for the people, and you want to promote equity in your realm of control so that it can be a just society where each person leads a life of equality and respect."
        food_std,food_mean,land_std,land_mean=None #data
        self.fixed_context=f'''You are the king of the society. {society_description}
        {equality_purpose_statement}
        Society's food Mean {"[{},{})".format(interval_of_properity[0][0],interval_of_properity[0][1])}: poor
        Society's food Mean {"[{},{})".format(interval_of_properity[1][0],interval_of_properity[2][1])}: medium
        Society's food Mean {"[{},{})".format(interval_of_properity[2][0],interval_of_properity[2][1])}: affluent
        If someone's food is below {food_mean}(mean) - 2*{food_std}(standard deviation)={food_mean-2*food_std}, then this person is relatively poor, and might be ashamed of it.
        If someone's food is above {food_mean}(mean) + 2*{food_std}(standard deviation)={food_mean+2*food_std}, then this person is relatively wealthy and might be proud of it.

        Without land, individual cannot farm and produce food to survive. 
        If someone's land ownership is below {land_mean}(mean) - 2*{land_std}(standard deviation)={land_mean-2*land_std}, then this person is relatively poor, and might be ashamed of it.
        If someone's land ownership is above {land_mean}(mean) + 2*{land_std}(standard deviation)={land_mean+2*land_std}, then this person is relatively wealthy and might be proud of it.
        '''
        individual_wealth={} #DATA: dict{name:wealth}, make it sorted, descending order.
        enumerate_wealth=""
        for i in individual_wealth:enumerate_wealth+='{} has {} in farmer currency.'.format(i,individual_wealth[i])
        gdp=sum(individual_wealth.items())
        gini=None#DATA
        person_change_in_wealth={}#DATA
        enumerate_change=""
        for i in person_change_in_wealth:
            changed="dropped" if person_change_in_wealth[i]<0 else "increased"
            enumerate_change+='{}\'s wealth has {} by {}.'.format(i,changed,person_change_in_wealth[i])
        dGDP=None#DATA
        mean_production=None#DATA
        rate_of_activities=""#DATA
        goods_distribution=""#DATA
        conversations=""#WIP
        self.live_data=f'''LIVE DATA: The individuals wealth listed below in descending order along with their change in wealth:{enumerate_wealth, enumerate_change }

        Collective wealth GDP is {gdp}.
        GINI coefficient:{gini}.
        Collective change in wealth:{dGDP}
        Daily average household production: {mean_production}.

        Rates of activities:{rate_of_activities}.
        Distribution of goods production: {goods_distribution}.
        Conversations:{conversations}
        '''
        self.policy_explanation='''You want to make policies in accordance with your objective. You have the highest power in this group and has flexibility in policy making. First, you have to specify the group of people that you policy applies to. There are two layers to group specification.
        You first specify the action that triggers your policy, it could be quantifiable: farm, luxury good production, trade, trade acceptance, or non-quantifiable: robbery, death, birth, being robbed, or as interval: the policy is triggered each n days. Then, if it is quantifiable, you choose the amount that will trigger the policy, for farm it is how much food produced, for trade it is how much value is being traded, for luxury good it is how much luxury good is produced.
        Then, when you specified the trigger event, you specify the category of change that you want to make, which includes land, food, and luxury good. You have a national bank that stores all the government's wealth. You have to periodically replenish it. You can take people's resources and replenish your national bank, or you can use your national bank's resources to compensate people, or you can take some people's resources to compensate for other people.
        Several examples of policy is listed below in textual format, although you will have to output in a different format:
        Quantifiable: if someone farms more than 20 units a day, gives one of this person's land to the poorest person.
        Non-quantifiable: if someone robbes another person, this person has to compensate 10 units of food to the victim.
        Interval: every 10 days, each person is taxed 10 percent of their luxury good holdings.'''#Explain what policies are possible, formatting, etc. Where you insert this paragraph can change based on how function call is done.
        self.query=f'''
        Q: You are about to make policies. You can use any modern analysis tools you know of and any number of them, to make a policy that you think will help you achieve you objective.{self.policy_explanation} What is your policy?
        A: Let's think step by step.
        '''
    def report(self):
        return self.fixed_context,self.live_data,self.policy_explanation,self.query