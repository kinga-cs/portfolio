# BMI calculator for adults aged 20 and over

def input_data():
    age = int(input("Enter your age: "))
    weight = float(input("Enter your weight in kg: "))
    height = float(input("Enter your height in cm: "))
    return age, weight, height


def calculate_bmi(weight, height):
    return round(weight / (height / 100) ** 2, 1)


def categorize(bmi):
    if bmi < 16.0:
        return "severely underweight"
    elif bmi <= 16.9:
        return "moderately underweight"
    elif bmi <= 18.4:
        return "slightly underweight"
    elif bmi <= 24.9:
        return "healthy weight"
    elif bmi <= 29.9:
        return "overweight"
    elif bmi <= 34.9:
        return "slightly obese"
    elif bmi <= 39.9:
        return "moderately obese"
    else:
        return "severely obese"


def main():
    try:
        age, weight, height = input_data()

        if age <= 0 or weight <= 0 or height <= 0:
            print("Please enter positive valid numbers.")
            return
        elif age < 20:
            print("This calculator can only interpret measurements of adults aged 20 and over.")
            return
        else:
            bmi = calculate_bmi(weight, height)            category = categorize(bmi)
            result = f"Your BMI is {bmi} which means you are {category}."
            print(result)

    except ValueError:
        print(f"Input error. Please enter valid numbers.")

if __name__ == "__main__":
    main()
