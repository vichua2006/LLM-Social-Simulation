import csv
from typing import Tuple, Dict, overload
import random
TraitLevel = int
TraitDescription = Dict[TraitLevel, str]
TraitDescriptions = Dict[str, TraitDescription]

prompt_csv_file_path = '../data/prompt_sheet.csv'

def read_full_local_csv():
    # Read the local CSV file
    with open(prompt_csv_file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)
    
def read_trait_descriptions() -> TraitDescriptions:
    trait_descriptions = {}
    with open(prompt_csv_file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for i, row in enumerate(reader):
            if i >= 5:  # Read only the first 5 rows
                break
            trait_name = row[0]  # The trait name is in the first column
            descriptions = {level: description for level, description in enumerate(row[1:], start=1)}
            trait_descriptions[trait_name] = descriptions
    return trait_descriptions

# Function to generate the Big 5 Prompt
def generate_big_5_prompt(levels: Tuple[TraitLevel, ...], trait_descriptions: TraitDescriptions = read_trait_descriptions()) -> str:
    descriptions = [trait_descriptions[trait][level] for trait, level in zip(trait_descriptions.keys(), levels)]
    return ' '.join(f"You are {desc}" for desc in descriptions)

# Function to generate the Big 5 Final Prompt
def generate_big_5_final_prompt(levels: Tuple[TraitLevel, ...], trait_descriptions: TraitDescriptions = read_trait_descriptions()) -> str:
    big_5_prompt = generate_big_5_prompt(levels, trait_descriptions)
    hint_prompt = "You should consider how those characteristic traits influence your response and decision."
    return big_5_prompt + " " + hint_prompt


def generate_random_big_5_final_prompt()->str:
    levels=random.choices(range(1,5),k=5)
    print("select random levels:", levels)
    return generate_big_5_final_prompt(levels=levels)
    
def read_general_prompt():
    sheet_data = read_full_local_csv()
    # Read the first the header and the first 5 rows
    sheet_data = sheet_data[6:7]
    return sheet_data

if __name__ == "__main__":
    print(generate_random_big_5_final_prompt())