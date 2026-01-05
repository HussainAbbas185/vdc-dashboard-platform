import csv
import random
import uuid
from faker import Faker
import os

fake = Faker('en_US')
Faker.seed(42)
random.seed(42)

OUTPUT_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'raw', 'input_data.csv')

def generate_record(original=None):
    """
    Generates a record. If 'original' is provided, it creates a duplicate 
    with potential errors (typos, variations).
    """
    if original and random.random() < 0.8: # 80% chance to corrupt the duplicate
        rec = original.copy()
        rec['id'] = str(uuid.uuid4()) # New ID for the duplicate record
        
        # Introduce noise
        change_type = random.choice(['typo_name', 'swap_email', 'missing_ssn', 'typo_dob', 'nick_name'])
        
        if change_type == 'typo_name':
            if random.choice([True, False]):
                rec['first_name'] = rec['first_name'][:-1] # Remove last char
            else:
                rec['last_name'] = rec['last_name'].replace('e', '3').replace('a', '@')
        elif change_type == 'nick_name':
            # rudimentary nickname logic
            if rec['first_name'] == 'Robert': rec['first_name'] = 'Bob'
            elif rec['first_name'] == 'William': rec['first_name'] = 'Bill'
            elif rec['first_name'] == 'Jennifer': rec['first_name'] = 'Jen'
        elif change_type == 'swap_email':
            # Change domain
            rec['email'] = rec['email'].replace('@example.com', '@test.com')
        elif change_type == 'missing_ssn':
            rec['ssn'] = None
        elif change_type == 'typo_dob':
            # Flip month/day potentially (simple string manip)
            parts = rec['dob'].split('-')
            if len(parts) == 3:
                rec['dob'] = f"{parts[0]}-{parts[2]}-{parts[1]}" # Swap month/day logic error
                
        return rec
    else:
        # completely new person
        gender = random.choice(['M', 'F'])
        fname = fake.first_name_male() if gender == 'M' else fake.first_name_female()
        lname = fake.last_name()
        
        return {
            'id': str(uuid.uuid4()),
            'first_name': fname,
            'last_name': lname,
            'email': f"{fname.lower()}.{lname.lower()}@{fake.free_email_domain()}",
            'dob': fake.date_of_birth(minimum_age=18, maximum_age=90).isoformat(),
            'ssn': fake.ssn(),
            'phone_number': fake.phone_number(),
            'address': fake.address().replace('\n', ', ')
        }

def generate_dataset(count=500, duplicate_rate=0.3):
    records = []
    
    # Determine how many unique people vs duplicates
    uniques_count = int(count * (1 - duplicate_rate))
    
    unique_people = []
    for _ in range(uniques_count):
        p = generate_record()
        unique_people.append(p)
        records.append(p)
        
    # Generate duplicates
    duplicates_needed = count - uniques_count
    for _ in range(duplicates_needed):
        original = random.choice(unique_people)
        duplicate = generate_record(original)
        records.append(duplicate)
        
    # Shuffle
    random.shuffle(records)
    
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    keys = records[0].keys()
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(records)
        
    print(f"Generated {len(records)} records (approx {duplicates_needed} duplicates) to {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_dataset(count=1000, duplicate_rate=0.4)
