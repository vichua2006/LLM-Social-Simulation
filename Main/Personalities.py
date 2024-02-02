from random import randint

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

def generate_personality():
    all_traits = [openness, conscientiousness, extraversion, agreeableness, neuroticism]
    
    descriptions = []
    for trait in all_traits:
        descriptions.append(trait[randint(0, 4)])
    
    return descriptions