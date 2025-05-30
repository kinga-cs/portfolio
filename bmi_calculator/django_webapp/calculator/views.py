from django.shortcuts import render

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

def calculator(request):
    result = None
    if request.method == "POST":
        try:
            age = int(request.POST["age"])
            weight = float(request.POST["weight"])
            height = float(request.POST["height"])

            if age <= 0 or weight <= 0 or height <= 0:
                result = "Please enter positive valid numbers."
            elif age < 20:
                result = "This calculator can only interpret measurements of adults aged 20 and over."
            else:
                bmi = calculate_bmi(weight, height)
                category = categorize(bmi)
                result = f"Your BMI is {bmi} which means you are {category}."

        except ValueError:
            result = "Please enter valid numbers."

    return render(request, 'calculator/calculator.html', {'result': result})


