'''creaated by Aryaman rawat '''
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import joblib
import numpy as np
# Create your views here.

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid user')
            return redirect('/login/')

        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, 'Invalid password')
            return redirect('/login/')

        else:
            login(request, user)
            return redirect('/')

    return render(request, 'login.html')
@login_required(login_url="/login/")
def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.info(request, "Username already exists")
            return redirect('/register/')

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password
        )
        user.save()
        messages.info(request, "Created successfully")
        return redirect('/register/')

    return render(request, 'register.html')




# Load the trained model
model = joblib.load('C:\\Users\\aryam\\OneDrive\\Desktop\\django prj\\diabetes_prj\\diabetes_model.pkl')  # Update the path as necessary
@login_required(login_url="/login/")
def pridict_page(request):
    if request.method == "POST":
        # Get user input from the form
        pregnancies = int(request.POST['Pregnancies'])
        glucose = int(request.POST['Glucose'])
        blood_pressure = int(request.POST['BloodPressure'])
        skin_thickness = int(request.POST['SkinThickness'])
        insulin = int(request.POST['Insulin'])
        bmi = float(request.POST['BMI'])
        dpf = float(request.POST['DiabetesPedigreeFunction'])
        age = int(request.POST['Age'])

        # Create feature array
        features = np.array([[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age]])

        # Make prediction
        prediction = model.predict(features)[0]
        result1=''
        if prediction==1:
            result1= "You are likely to have diabetes"
            
        else:
            result1="You are not likely to have diabetes"

        return redirect('display_result', result=result1)

    return render(request, 'predict.html')
@login_required(login_url="/login/")
def display_result(request, result):
    return render(request, 'result.html', {'result': result})


def logout_page(request):
    logout(request)
    return redirect('/login/')