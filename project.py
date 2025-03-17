# import pandas as pd
# import numpy as np
# from datetime import datetime, timedelta
# from reportlab.lib.pagesizes import letter
# from reportlab.lib import colors
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
# import sys
# # Constants
# DAYS_IN_WEEK = 7
# MEALS_PER_DAY = 3
# MEAL_TYPES = ['Breakfast', 'Lunch', 'Dinner']
# MACRONUTRIENT_RATIOS = {
#     'weight_loss': {'protein': 0.3, 'carbs': 0.4, 'fats': 0.3},
#     'maintenance': {'protein': 0.25, 'carbs': 0.45, 'fats': 0.3},
#     'muscle_gain': {'protein': 0.35, 'carbs': 0.4, 'fats': 0.25}
# }
# ACTIVITY_LEVELS = {
#     'sedentary': 1.2,
#     'lightly_active': 1.375,
#     'moderately_active': 1.55,
#     'very_active': 1.725,
#     'extra_active': 1.9
# }

# # Load the recipe database
# def load_recipes(filepath):
#     recipes = pd.read_csv(filepath)
#     # Rename columns to match the expected format
#     recipes.rename(columns={
#         'Dish': 'Dish Name',
#         'Proteins (g)': 'Protein',
#         'Fats (g)': 'Fats',
#         'Carbs (g)': 'Carbs'
#     }, inplace=True)
#     return recipes

# # Calculate BMR using Harris-Benedict equation
# def calculate_bmr(age, height, weight, gender):
#     if gender.lower() == 'male':
#         return 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
#     else:
#         return 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

# # Calculate daily calorie needs
# def calculate_daily_calories(bmr, activity_level, fitness_goal):
#     activity_factor = ACTIVITY_LEVELS.get(activity_level, 1.2)
#     maintenance_calories = bmr * activity_factor
    
#     if fitness_goal == 'weight_loss':
#         return maintenance_calories - 500
#     elif fitness_goal == 'muscle_gain':
#         return maintenance_calories + 500
#     else:
#         return maintenance_calories

# # Calculate macronutrient requirements
# def calculate_macronutrients(calories, fitness_goal):
#     ratios = MACRONUTRIENT_RATIOS.get(fitness_goal, MACRONUTRIENT_RATIOS['maintenance'])
#     protein = (calories * ratios['protein']) / 4  # 4 calories per gram of protein
#     carbs = (calories * ratios['carbs']) / 4      # 4 calories per gram of carbs
#     fats = (calories * ratios['fats']) / 9        # 9 calories per gram of fat
#     return {'protein': protein, 'carbs': carbs, 'fats': fats}

# # Define weights based on fitness goal
# def define_weights(fitness_goal):
#     if fitness_goal == 'weight_loss':
#         return {'calories': 0.5, 'protein': 0.3, 'fats': 0.1, 'carbs': 0.1}
#     elif fitness_goal == 'maintenance':
#         return {'calories': 0.4, 'protein': 0.25, 'fats': 0.2, 'carbs': 0.15}
#     elif fitness_goal == 'muscle_gain':
#         return {'calories': 0.3, 'protein': 0.4, 'fats': 0.2, 'carbs': 0.1}
#     else:
#         return {'calories': 0.4, 'protein': 0.25, 'fats': 0.2, 'carbs': 0.15}  # Default

# # Calculate weighted score for a dish
# def calculate_score(dish, target, weights):
#     calorie_diff = abs(dish['Calories'] - target['calories'])
#     protein_diff = abs(dish['Protein'] - target['protein'])
#     fats_diff = abs(dish['Fats'] - target['fats'])
#     carbs_diff = abs(dish['Carbs'] - target['carbs'])
    
#     score = (weights['calories'] * calorie_diff) + \
#             (weights['protein'] * protein_diff) + \
#             (weights['fats'] * fats_diff) + \
#             (weights['carbs'] * carbs_diff)
#     return score

# # Find the best-matching dish
# def find_best_dish(recipes, meal_type, target, weights, history):
#     # Filter recipes by meal type and exclude recently recommended dishes
#     filtered = recipes[(recipes['Meal Type'] == meal_type) & (~recipes['Dish Name'].isin(history))]
    
#     # Calculate scores for all dishes
#     filtered = filtered.copy()  # Ensure a new copy is created
#     filtered.loc[:, 'Score'] = filtered.apply(lambda row: calculate_score(row, target, weights), axis=1)

    
#     # Return the dish with the lowest score
#     return filtered.loc[filtered['Score'].idxmin()]

# # Recommend a combination of dishes
# def recommend_combination(recipes, meal_type, target, weights, history):
#     # Filter recipes by meal type and exclude recently recommended dishes
#     filtered = recipes[(recipes['Meal Type'] == meal_type) & (~recipes['Dish Name'].isin(history))]
    
#     # Use a greedy algorithm to find the best combination
#     best_combo = []
#     remaining_target = target.copy()
    
#     while True:
#         # Find the best-matching dish for the remaining target
#         dish = find_best_dish(filtered, meal_type, remaining_target, weights, history)
#         best_combo.append(dish)
        
#         # Update the remaining target
#         remaining_target['calories'] -= dish['Calories']
#         remaining_target['protein'] -= dish['Protein']
#         remaining_target['fats'] -= dish['Fats']
#         remaining_target['carbs'] -= dish['Carbs']
        
#         # Stop if the remaining target is met or no more dishes are available
#         if all(v <= 0 for v in remaining_target.values()) or len(best_combo) >= 3:
#             break
    
#     return best_combo

# # Combine duplicate dishes in a meal
# def combine_duplicate_dishes(meals):
#     combined_meals = {}
#     for meal in meals:
#         key = (meal['Day'], meal['Meal Type'], meal['Dish Name'])
#         if key in combined_meals:
#             # Update portion size and nutritional values
#             combined_meals[key]['Portion Size'] += 1.0
#             combined_meals[key]['Calories'] += meal['Calories']
#             combined_meals[key]['Protein'] += meal['Protein']
#             combined_meals[key]['Fats'] += meal['Fats']
#             combined_meals[key]['Carbs'] += meal['Carbs']
#         else:
#             # Add new meal to the dictionary
#             combined_meals[key] = meal.copy()
#     return list(combined_meals.values())

# # Recommend meals for a day
# def recommend_meals_for_day(recipes, daily_target, weights, history, threshold=20):
#     meals = []
#     for meal_type in MEAL_TYPES:
#         # Calculate target for the meal
#         meal_target = {
#             'calories': daily_target['calories'] * 0.30 if meal_type == 'Breakfast' else daily_target['calories'] * 0.40 if meal_type == 'Lunch' else daily_target['calories'] * 0.30,
#             'protein': daily_target['protein'] * 0.25 if meal_type == 'Breakfast' else daily_target['protein'] * 0.40 if meal_type == 'Lunch' else daily_target['protein'] * 0.35,
#             'fats': daily_target['fats'] * 0.25 if meal_type == 'Breakfast' else daily_target['fats'] * 0.40 if meal_type == 'Lunch' else daily_target['fats'] * 0.35,
#             'carbs': daily_target['carbs'] * 0.25 if meal_type == 'Breakfast' else daily_target['carbs'] * 0.40 if meal_type == 'Lunch' else daily_target['carbs'] * 0.35
#         }
        
#         # Find the best single dish
#         best_single_dish = find_best_dish(recipes, meal_type, meal_target, weights, history)
#         best_single_score = calculate_score(best_single_dish, meal_target, weights)
        
#         # Decide whether to recommend a single dish or a combination
#         if best_single_score <= threshold:
#             meals.append({
#                 'Day': 1,  # Placeholder, will be updated later
#                 'Meal Type': meal_type,
#                 'Dish Name': best_single_dish['Dish Name'],
#                 'Portion Size': 1.0,
#                 'Calories': best_single_dish['Calories'],
#                 'Protein': best_single_dish['Protein'],
#                 'Fats': best_single_dish['Fats'],
#                 'Carbs': best_single_dish['Carbs']
#             })
#             history.append(best_single_dish['Dish Name'])
#         else:
#             combo = recommend_combination(recipes, meal_type, meal_target, weights, history)
#             for dish in combo:
#                 meals.append({
#                     'Day': 1,  # Placeholder, will be updated later
#                     'Meal Type': meal_type,
#                     'Dish Name': dish['Dish Name'],
#                     'Portion Size': 1.0,
#                     'Calories': dish['Calories'],
#                     'Protein': dish['Protein'],
#                     'Fats': dish['Fats'],
#                     'Carbs': dish['Carbs']
#                 })
#                 history.append(dish['Dish Name'])
    
#     return meals

# # Generate PDF directly from meal plan data
# def generate_pdf(meal_plan, pdf_file):
#     # Create a PDF document
#     doc = SimpleDocTemplate(pdf_file, pagesize=letter)
#     styles = getSampleStyleSheet()
#     story = []
    
#     # Add title
#     title = Paragraph("Diet Plan", styles['Title'])
#     story.append(title)
#     story.append(Spacer(1, 12))
    
#     # Iterate through each day
#     for day in range(1, DAYS_IN_WEEK + 1):
#         # Add day header
#         day_header = Paragraph(f"Day {day}", styles['Heading2'])
#         story.append(day_header)
#         story.append(Spacer(1, 12))
        
#         # Filter data for the current day
#         day_data = [meal for meal in meal_plan if meal['Day'] == day]
        
#         # Group by meal type
#         for meal_type in MEAL_TYPES:
#             meal_data = [meal for meal in day_data if meal['Meal Type'] == meal_type]
#             if meal_data:
#                 # Add meal type header
#                 meal_header = Paragraph(meal_type, styles['Heading3'])
#                 story.append(meal_header)
#                 story.append(Spacer(1, 6))
                
#                 # Create a table for dishes and portion sizes
#                 table_data = [['Dish Name', 'Portion Size']]
#                 for meal in meal_data:
#                     table_data.append([meal['Dish Name'], f"{meal['Portion Size']}"])
                
#                 # Define table style
#                 table = Table(table_data, colWidths=[400, 100])
#                 table.setStyle(TableStyle([
#                     ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#                     ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#                     ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
#                     ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#                     ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#                     ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#                     ('GRID', (0, 0), (-1, -1), 1, colors.black),
#                 ]))
                
#                 # Add table to the story
#                 story.append(table)
#                 story.append(Spacer(1, 12))
    
#     # Build the PDF
#     doc.build(story)
#     print(f"PDF saved to {pdf_file}")

# # Main function
# import sys

# def main():
#     # Load recipes
#     recipes = load_recipes(r"D:\Ai Diet Planner\filtered_dataset.csv")
    
#     # Check if the script is being run with command-line arguments
#     if len(sys.argv) < 7:
#         print("Usage: python project.py <height> <weight> <age> <gender> <activity_level> <fitness_goal>")
#         return

#     # Get user inputs from command-line arguments
#     height = float(sys.argv[1])
#     weight = float(sys.argv[2])
#     age = int(sys.argv[3])
#     gender = sys.argv[4]
#     activity_level = sys.argv[5]
#     fitness_goal = sys.argv[6]

#     print(f"Inputs Received: Height={height}, Weight={weight}, Age={age}, Gender={gender}, Activity={activity_level}, Goal={fitness_goal}")

#     # Calculate daily requirements
#     bmr = calculate_bmr(age, height, weight, gender)
#     daily_calories = calculate_daily_calories(bmr, activity_level, fitness_goal)
#     macronutrients = calculate_macronutrients(daily_calories, fitness_goal)

#     # Define weights for scoring
#     weights = define_weights(fitness_goal)

#     # Initialize meal history
#     meal_history = []

#     # Generate meal plan for the week
#     meal_plan = []
#     for day in range(DAYS_IN_WEEK):
#         meals = recommend_meals_for_day(recipes, {
#             'calories': daily_calories,
#             'protein': macronutrients['protein'],
#             'fats': macronutrients['fats'],
#             'carbs': macronutrients['carbs']
#         }, weights, meal_history)

#         # Update the day for each meal
#         for meal in meals:
#             meal['Day'] = day + 1

#         # Combine duplicate dishes
#         combined_meals = combine_duplicate_dishes(meals)
#         meal_plan.extend(combined_meals)

#     print(f"Generated Meal Plan: {meal_plan}")

#     # Generate PDF directly from meal plan data
#     generate_pdf(meal_plan, 'weekly_meal_plan.pdf')
#     print("Weekly meal plan PDF saved to 'weekly_meal_plan.pdf'.")

# # Run the program
# if __name__ == "__main__":
#     main()

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
import sys
import random

# Constants
DAYS_IN_WEEK = 7
MEALS_PER_DAY = 3
MEAL_TYPES = ['Breakfast', 'Lunch', 'Dinner']
MACRONUTRIENT_RATIOS = {
    'weight_loss': {'protein': 0.3, 'carbs': 0.4, 'fats': 0.3},
    'maintenance': {'protein': 0.25, 'carbs': 0.45, 'fats': 0.3},
    'muscle_gain': {'protein': 0.35, 'carbs': 0.4, 'fats': 0.25}
}
ACTIVITY_LEVELS = {
    'sedentary': 1.2,
    'lightly_active': 1.375,
    'moderately_active': 1.55,
    'very_active': 1.725,
    'extra_active': 1.9
}

# Load the recipe database
def load_recipes(filepath):
    recipes = pd.read_csv(filepath)
    # Rename columns to match the expected format
    recipes.rename(columns={
        'Dish': 'Dish Name',
        'Proteins (g)': 'Protein',
        'Fats (g)': 'Fats',
        'Carbs (g)': 'Carbs'
    }, inplace=True)
    return recipes

# Calculate BMR using Harris-Benedict equation
def calculate_bmr(age, height, weight, gender):
    if gender.lower() == 'male':
        return 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        return 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

# Calculate daily calorie needs
def calculate_daily_calories(bmr, activity_level, fitness_goal):
    activity_factor = ACTIVITY_LEVELS.get(activity_level, 1.2)
    maintenance_calories = bmr * activity_factor
    
    if fitness_goal == 'weight_loss':
        return maintenance_calories - 500
    elif fitness_goal == 'muscle_gain':
        return maintenance_calories + 500
    else:
        return maintenance_calories

# Calculate macronutrient requirements
def calculate_macronutrients(calories, fitness_goal):
    ratios = MACRONUTRIENT_RATIOS.get(fitness_goal, MACRONUTRIENT_RATIOS['maintenance'])
    protein = (calories * ratios['protein']) / 4  # 4 calories per gram of protein
    carbs = (calories * ratios['carbs']) / 4      # 4 calories per gram of carbs
    fats = (calories * ratios['fats']) / 9        # 9 calories per gram of fat
    return {'protein': protein, 'carbs': carbs, 'fats': fats}

# Define weights based on fitness goal
def define_weights(fitness_goal):
    if fitness_goal == 'weight_loss':
        return {'calories': 0.5, 'protein': 0.3, 'fats': 0.1, 'carbs': 0.1}
    elif fitness_goal == 'maintenance':
        return {'calories': 0.4, 'protein': 0.25, 'fats': 0.2, 'carbs': 0.15}
    elif fitness_goal == 'muscle_gain':
        return {'calories': 0.3, 'protein': 0.4, 'fats': 0.2, 'carbs': 0.1}
    else:
        return {'calories': 0.4, 'protein': 0.25, 'fats': 0.2, 'carbs': 0.15}  # Default

# Calculate weighted score for a dish
def calculate_score(dish, target, weights):
    calorie_diff = abs(dish['Calories'] - target['calories'])
    protein_diff = abs(dish['Protein'] - target['protein'])
    fats_diff = abs(dish['Fats'] - target['fats'])
    carbs_diff = abs(dish['Carbs'] - target['carbs'])
    
    score = (weights['calories'] * calorie_diff) + \
            (weights['protein'] * protein_diff) + \
            (weights['fats'] * fats_diff) + \
            (weights['carbs'] * carbs_diff)
    return score

# Find the best-matching dish with randomization
def find_best_dish(recipes, meal_type, target, weights, history, top_n=5):
    # Filter recipes by meal type and exclude recently recommended dishes
    filtered = recipes[(recipes['Meal Type'] == meal_type) & (~recipes['Dish Name'].isin(history))]
    
    # Calculate scores for all dishes
    filtered = filtered.copy()  # Ensure a new copy is created
    filtered.loc[:, 'Score'] = filtered.apply(lambda row: calculate_score(row, target, weights), axis=1)

    # Sort by score and select the top N dishes
    top_dishes = filtered.nsmallest(top_n, 'Score')
    
    # Randomly select one dish from the top N
    if not top_dishes.empty:
        return top_dishes.sample(n=1).iloc[0]
    else:
        return None

# Recommend a combination of dishes
def recommend_combination(recipes, meal_type, target, weights, history):
    # Filter recipes by meal type and exclude recently recommended dishes
    filtered = recipes[(recipes['Meal Type'] == meal_type) & (~recipes['Dish Name'].isin(history))]
    
    # Use a greedy algorithm to find the best combination
    best_combo = []
    remaining_target = target.copy()
    
    while True:
        # Find the best-matching dish for the remaining target
        dish = find_best_dish(filtered, meal_type, remaining_target, weights, history)
        if dish is None:
            break
        best_combo.append(dish)
        
        # Update the remaining target
        remaining_target['calories'] -= dish['Calories']
        remaining_target['protein'] -= dish['Protein']
        remaining_target['fats'] -= dish['Fats']
        remaining_target['carbs'] -= dish['Carbs']
        
        # Stop if the remaining target is met or no more dishes are available
        if all(v <= 0 for v in remaining_target.values()) or len(best_combo) >= 3:
            break
    
    return best_combo

# Combine duplicate dishes in a meal
def combine_duplicate_dishes(meals):
    combined_meals = {}
    for meal in meals:
        key = (meal['Day'], meal['Meal Type'], meal['Dish Name'])
        if key in combined_meals:
            # Update portion size and nutritional values
            combined_meals[key]['Portion Size'] += 1.0
            combined_meals[key]['Calories'] += meal['Calories']
            combined_meals[key]['Protein'] += meal['Protein']
            combined_meals[key]['Fats'] += meal['Fats']
            combined_meals[key]['Carbs'] += meal['Carbs']
        else:
            # Add new meal to the dictionary
            combined_meals[key] = meal.copy()
    return list(combined_meals.values())

# Recommend meals for a day
def recommend_meals_for_day(recipes, daily_target, weights, history, threshold=20):
    meals = []
    for meal_type in MEAL_TYPES:
        # Calculate target for the meal
        meal_target = {
            'calories': daily_target['calories'] * 0.30 if meal_type == 'Breakfast' else daily_target['calories'] * 0.40 if meal_type == 'Lunch' else daily_target['calories'] * 0.30,
            'protein': daily_target['protein'] * 0.25 if meal_type == 'Breakfast' else daily_target['protein'] * 0.40 if meal_type == 'Lunch' else daily_target['protein'] * 0.35,
            'fats': daily_target['fats'] * 0.25 if meal_type == 'Breakfast' else daily_target['fats'] * 0.40 if meal_type == 'Lunch' else daily_target['fats'] * 0.35,
            'carbs': daily_target['carbs'] * 0.25 if meal_type == 'Breakfast' else daily_target['carbs'] * 0.40 if meal_type == 'Lunch' else daily_target['carbs'] * 0.35
        }
        
        # Find the best single dish
        best_single_dish = find_best_dish(recipes, meal_type, meal_target, weights, history)
        if best_single_dish is not None:
            best_single_score = calculate_score(best_single_dish, meal_target, weights)
        else:
            best_single_score = float('inf')
        
        # Decide whether to recommend a single dish or a combination
        if best_single_score <= threshold:
            meals.append({
                'Day': 1,  # Placeholder, will be updated later
                'Meal Type': meal_type,
                'Dish Name': best_single_dish['Dish Name'],
                'Portion Size': 1.0,
                'Calories': best_single_dish['Calories'],
                'Protein': best_single_dish['Protein'],
                'Fats': best_single_dish['Fats'],
                'Carbs': best_single_dish['Carbs']
            })
            history.append(best_single_dish['Dish Name'])
        else:
            combo = recommend_combination(recipes, meal_type, meal_target, weights, history)
            for dish in combo:
                meals.append({
                    'Day': 1,  # Placeholder, will be updated later
                    'Meal Type': meal_type,
                    'Dish Name': dish['Dish Name'],
                    'Portion Size': 1.0,
                    'Calories': dish['Calories'],
                    'Protein': dish['Protein'],
                    'Fats': dish['Fats'],
                    'Carbs': dish['Carbs']
                })
                history.append(dish['Dish Name'])
    
    return meals

# Generate PDF directly from meal plan data
def generate_pdf(meal_plan, pdf_file):
    # Create a PDF document
    doc = SimpleDocTemplate(pdf_file, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Add title
    title = Paragraph("Diet Plan", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))
    
    # Iterate through each day
    for day in range(1, DAYS_IN_WEEK + 1):
        # Add day header
        day_header = Paragraph(f"Day {day}", styles['Heading2'])
        story.append(day_header)
        story.append(Spacer(1, 12))
        
        # Filter data for the current day
        day_data = [meal for meal in meal_plan if meal['Day'] == day]
        
        # Group by meal type
        for meal_type in MEAL_TYPES:
            meal_data = [meal for meal in day_data if meal['Meal Type'] == meal_type]
            if meal_data:
                # Add meal type header
                meal_header = Paragraph(meal_type, styles['Heading3'])
                story.append(meal_header)
                story.append(Spacer(1, 6))
                
                # Create a table for dishes and portion sizes
                table_data = [['Dish Name', 'Portion Size']]
                for meal in meal_data:
                    table_data.append([meal['Dish Name'], f"{meal['Portion Size']}"])
                
                # Define table style
                table = Table(table_data, colWidths=[400, 100])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))
                
                # Add table to the story
                story.append(table)
                story.append(Spacer(1, 12))
    
    # Build the PDF
    doc.build(story)
    print(f"PDF saved to {pdf_file}")

# Main function
def main():
    # Load recipes
    recipes = load_recipes(r"D:\Ai Diet Planner\filtered_dataset.csv")
    
    # Check if the script is being run with command-line arguments
    if len(sys.argv) < 7:
        print("Usage: python project.py <height> <weight> <age> <gender> <activity_level> <fitness_goal>")
        return

    # Get user inputs from command-line arguments
    height = float(sys.argv[1])
    weight = float(sys.argv[2])
    age = int(sys.argv[3])
    gender = sys.argv[4]
    activity_level = sys.argv[5]
    fitness_goal = sys.argv[6]

    print(f"Inputs Received: Height={height}, Weight={weight}, Age={age}, Gender={gender}, Activity={activity_level}, Goal={fitness_goal}")

    # Calculate daily requirements
    bmr = calculate_bmr(age, height, weight, gender)
    daily_calories = calculate_daily_calories(bmr, activity_level, fitness_goal)
    macronutrients = calculate_macronutrients(daily_calories, fitness_goal)

    # Define weights for scoring
    weights = define_weights(fitness_goal)

    # Initialize meal history
    meal_history = []

    # Generate meal plan for the week
    meal_plan = []
    for day in range(DAYS_IN_WEEK):
        meals = recommend_meals_for_day(recipes, {
            'calories': daily_calories,
            'protein': macronutrients['protein'],
            'fats': macronutrients['fats'],
            'carbs': macronutrients['carbs']
        }, weights, meal_history)

        # Update the day for each meal
        for meal in meals:
            meal['Day'] = day + 1

        # Combine duplicate dishes
        combined_meals = combine_duplicate_dishes(meals)
        meal_plan.extend(combined_meals)

    print(f"Generated Meal Plan: {meal_plan}")

    # Generate PDF directly from meal plan data
    generate_pdf(meal_plan, 'weekly_meal_plan.pdf')
    print("Weekly meal plan PDF saved to 'weekly_meal_plan.pdf'.")

# Run the program
if __name__ == "__main__":
    main()