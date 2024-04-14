#voting process explained:
voting_process='''First week (s):
Daily chores, with conversations. At first perhaps people wouldn't know who to talk to, so even if there were conversations the conversing partner chosen would be random, but as time go on, people accrue memories about other people, about interactive activities, and then choosing who to talk to wouldn't be random.

At certain points, people gather, roundtable discussions. People evince their opinions. People can raise policy recommendations, added to the list of potential policies. In the end, preferences are collected.

Another week (s):
After that, maybe another week passes, during the time each person can talk to any other person to persuade or just to discuss. We could make each person's live preferences available to everyone.

Then, we hold a voting. 
First, we vote on old policies. We can use approval voting on this one. So some policy with too little approval will be removed, but sometimes no policy will be removed.
Second, we hold policy voting for the newer policies. The top policy (s) will be implemented.
'''

#Phase 1, daily interactions. The prompt should be combined with the prompt for other actions.
direct_phase1=f"Each day you are allowed to talk with another person of your choice of topic of your choosing. You can choose to initiate it, or you can choose not to actively talk to anyone for today."
discuss_phase1=f"Now that everyone had time to experience the week, you have a chance to discuss it with other civilians of the village. Let people know your thoughts on the state of your life and this society, and suggest any policy you would want to implement."
#This prompt only provides the contexts. How policy is outputted will come from what's finalized from our soverign model.
summarize_phase1=f"Now you've had time to discuss, please summarize succinctly your preferred policy."
#This make people summarize their opinion into their top choice of policy.
direct_phase2=f"Now everyone has envinced their opinion on policy matters, you have a chance to talk to other people individually in private. You'd want to convince people who do not support the same policy as you do if you want your policy to win."
#This prompt people to persuade others during phase 2.