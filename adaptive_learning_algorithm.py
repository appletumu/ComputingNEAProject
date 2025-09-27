"""
QUESTION SCORES
Correct = 2
Partially Correct = 1
Incorrect = 0

FACTORS
- Percentage
- Percentage History (gets an average from this)
- How many times recalled
- The last time it was recalled

ADAPTIVE LEARNING ALGORITHM
>90% = Don't need to recall
>70% = Needs attention
"""
percentage_history = [14, 27, 63, 40, 74, 82, 93, 90, 100]

user_score = 5 # input
available_score = 20 # input

percentage = int(round(user_score / available_score * 100, 2) if available_score > 0 else 0)
bad_scores = 0
alright_scores = 0
great_scores = 0
for previous_percentage in percentage_history:
    if previous_percentage >= 90:
        great_scores
    elif previous_percentage >= 70:
        alright_scores += 1
    else:
        bad_scores += 1

algorithim_grade = percentage

print(f"Current Percentage: {percentage}%")
print()
print(algorithim_grade)