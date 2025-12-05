import pandas as pd
import random
import datetime

# 1. Setup Lists of Options
insurance_providers = ['BlueCross', 'Aetna', 'UnitedHealth', 'Medicare', 'Cigna']
procedure_codes = ['99213', '99214', '99203', '99204', '36415']
denial_reasons = ['Prior Auth Missing', 'Duplicate Claim', 'Coverage Terminated', 'Coding Error']

# 2. Function to generate a random date within the last year
def generate_date():
    start_date = datetime.date(2023, 1, 1)
    end_date = datetime.date(2023, 12, 31)
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    return start_date + datetime.timedelta(days=random_number_of_days)

# 3. Create the Dataset
data = []

for i in range(1, 501):  # Generate 500 rows
    claim_id = 1000 + i
    date_of_service = generate_date()
    
    # Select Insurance (Weighted so Medicare appears often)
    insurance = random.choices(insurance_providers, weights=[25, 20, 20, 25, 10], k=1)[0]
    
    procedure = random.choice(procedure_codes)
    billed_amount = random.randint(100, 450)
    
    # 4. "Rigging" the Logic (The Secret Sauce)
    # If Medicare, higher chance of Denial due to 'Prior Auth Missing'
    if insurance == 'Medicare':
        status = random.choices(['Paid', 'Denied', 'Pending'], weights=[50, 40, 10], k=1)[0]
    else:
        status = random.choices(['Paid', 'Denied', 'Pending'], weights=[80, 15, 5], k=1)[0]
    
    # Assign Denial Reason only if status is 'Denied'
    if status == 'Denied':
        if insurance == 'Medicare':
            reason = 'Prior Auth Missing' # The pattern you want to find!
        else:
            reason = random.choice(denial_reasons)
    else:
        reason = None # Empty if Paid or Pending

    # Append row to data list
    data.append([claim_id, date_of_service, insurance, procedure, billed_amount, status, reason])

# 5. Convert to DataFrame and Save
df = pd.DataFrame(data, columns=['Claim_ID', 'Date_of_Service', 'Insurance_Provider', 
                                 'Procedure_Code', 'Billed_Amount', 'Claim_Status', 'Denial_Reason'])

# Save to CSV
df.to_csv('medical_claims_data.csv', index=False)

print("Success! 'medical_claims_data.csv' has been created.")
print(df.head()) # Show the first 5 rows