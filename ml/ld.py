import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('training_dataset.csv')

# Compute the highest trait score for each row
highest_trait = df[['openness', 'neuroticism', 'conscientiousness', 'agreeableness', 'extraversion']].idxmax(axis=1)

# Update the "Personality (Class label)" column based on the highest trait score
df['Personality (Class label)'] = ''
df.loc[highest_trait == 'openness', 'Personality (Class label)'] = 'responsible'
df.loc[highest_trait == 'neuroticism', 'Personality (Class label)'] = 'lively'
df.loc[highest_trait == 'conscientiousness', 'Personality (Class label)'] = 'serious'
df.loc[highest_trait == 'agreeableness', 'Personality (Class label)'] = 'dependable'
df.loc[highest_trait == 'extraversion', 'Personality (Class label)'] = 'extraverted'

# Write the updated DataFrame to a new CSV file
df.to_csv('training_dataset.md.csv', index=False)
