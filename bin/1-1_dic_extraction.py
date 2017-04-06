#%%
import re
import pandas as pd

f = open(r"D:\OneDrive\GitHub\content_analysis_final\reference\Webster's Unabridged 09\29765-8.txt")
text = f.read()

#%%
results_feel = re.findall('\n[^a-z]+\n.*?[f|F]eel', text, re.DOTALL)
results_emotion = re.findall('\n[^a-z]+\n.*?[e|E]motion', text, re.DOTALL)
results_experience = re.findall('\n[^a-z]+\n.*?[e|E]xperience', text, re.DOTALL)

result_feel = set([(re.findall('\n[^a-z]+\n', s)[-1]).strip() for s in results_feel])
result_emotion = set([(re.findall('\n[^a-z]+\n', s)[-1]).strip() for s in results_emotion])
result_experience = set([(re.findall('\n[^a-z]+\n', s)[-1]).strip() for s in results_experience])

#%%
results_encounter = re.findall('\n[^a-z]+\n.*?[e|E]ncounter', text, re.DOTALL)
result_encounter = set([(re.findall('\n[^a-z]+\n', s)[-1]).strip() for s in results_encounter])
# print(result_encounter)

#%%
results_sensation = re.findall('\n[^a-z]+\n.*?[s|S]ensation', text, re.DOTALL)
result_sensation = set([(re.findall('\n[^a-z]+\n', s)[-1]).strip() for s in results_sensation])
# print(result_sensation)

#%%
len(result_emotion | result_feel | result_experience | result_encounter | result_sensation)

keywords = pd.Series(list(result_emotion | result_feel | result_experience | result_encounter | result_sensation))

keywords.to_csv(r'..\data\process\keywords.csv', index=False)
