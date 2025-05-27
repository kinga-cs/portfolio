# BMI calculator for adults aged 20 and over

def input_data():
    age = int(input("Enter your age: "))
    weight = float(input("Enter your weight in kg: "))
    height = float(input("Enter your height in cm: "))
    return age, weight, height


def calculate_bmi(weight, height):
    #bmi = weight / (height / 100) ** 2
    return round(weight / (height / 100) ** 2, 1)


def categorize(bmi):
    if bmi > 0:
        if bmi < 16.0:
            print(f"Your BMI is {bmi} which means you are severely underweight.")
        elif bmi <= 16.9:
            print(f"Your BMI is {bmi} which means you are moderately underweight.")
        elif bmi <= 18.4:
            print(f"Your BMI is {bmi} which means you are slightly underweight.")
        elif bmi <= 24.9:
            print(f"Your BMI is {bmi} which means you have a healthy weight.")
        elif bmi <= 29.9:
            print(f"Your BMI is {bmi} which means you are overweight.")
        elif bmi <= 34.9:
            print(f"Your BMI is {bmi} which means you are slightly obese.")
        elif bmi <= 39.9:
            print(f"Your BMI is {bmi} which means you are moderately obese.")
        else:
            print(f"Your BMI is {bmi} which means you are severely obese.")
    else:
        print("Please enter valid numbers.")


def main():
    user_age, user_weight, user_height = input_data()

    if user_age >= 20:
        bmi_value = calculate_bmi(user_weight, user_height)
        categorize(bmi_value)
    else:
        print("This calculator only works for adults aged 20 and over.")


if __name__ == "__main__":
    main()
