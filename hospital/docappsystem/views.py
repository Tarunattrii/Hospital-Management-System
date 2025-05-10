from django.shortcuts import render, redirect, HttpResponse
from dasapp.EmailBackEnd import EmailBackEnd
from django.contrib.auth import logout, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from dasapp.models import CustomUser, DoctorReg, PatientReg, Specialization, Day  # Updated to include DoctorReg, Specialization, Day
from django.contrib.auth import get_user_model
User = get_user_model()

def BASE(request):
    return render(request, 'base.html')

def LOGIN(request):
    return render(request, 'login.html')

def doLogout(request):
    logout(request)
    return redirect('login')

def doLogin(request):
    if request.method == 'POST':
        user = EmailBackEnd.authenticate(request,
                                         username=request.POST.get('email'),
                                         password=request.POST.get('password')
                                         )
        if user != None:
            login(request, user)
            user_type = user.user_type
            if user_type == '1':
                 return redirect('admin_home')
            elif user_type == '2':
                 return redirect('doctor_home')
            elif user_type == '3':
                return redirect('userhome')
        else:
                messages.error(request, 'Email or Password is not valid')
                return redirect('login')
    else:
            messages.error(request, 'Email or Password is not valid')
            return redirect('login')

@login_required(login_url='/')
def PROFILE(request):
    user = CustomUser.objects.get(id=request.user.id)
    context = {
        "user": user,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='/')
def PROFILE_UPDATE(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email')
        username = request.POST.get('username')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name

            if profile_pic is not None and profile_pic != "":
               customuser.profile_pic = profile_pic
            customuser.save()
            messages.success(request, "Your profile has been updated successfully")
            return redirect('profile')
        except:
            messages.error(request, "Your profile updation has been failed")
    return render(request, 'profile.html')

def CHANGE_PASSWORD(request):
     context = {}
     ch = User.objects.filter(id=request.user.id)
     
     if len(ch) > 0:
            data = User.objects.get(id=request.user.id)
            context["data"]: data            
     if request.method == "POST":        
        current = request.POST["cpwd"]
        new_pas = request.POST['npwd']
        user = User.objects.get(id=request.user.id)
        un = user.username
        check = user.check_password(current)
        if check == True:
          user.set_password(new_pas)
          user.save()
          messages.success(request, 'Password Changed Successfully!!!')
          user = User.objects.get(username=un)
          login(request, user)
        else:
          messages.success(request, 'Current Password is wrong!!!')
          return redirect("change_password")
     return render(request, 'change-password.html')

def Doctor(request):
    doctors = DoctorReg.objects.all()
    
    for doctor in doctors:
        # Get available day names as a sorted list
        day_names = list(doctor.available_days.values_list('name', flat=True))

        # Check for common cases
        if set(day_names) == {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"}:
            doctor.day_display = "Monday - Sunday"
        elif set(day_names) == {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"}:
            doctor.day_display = "Monday - Saturday"
        elif set(day_names) == {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday"}:
            doctor.day_display = "Monday - Friday"
        elif set(day_names) == {"Saturday", "Sunday"}:
            doctor.day_display = "Saturday - Sunday"
        else:
            doctor.day_display = ", ".join(day_names)  # Default to individual days

    context = {'dv': doctors}
    return render(request, 'doctor.html', context)

def PATIENTREGISTRATION(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        username = request.POST.get('username')
        mobno = request.POST.get('mobno')
        address = request.POST.get('address')
        password = request.POST.get('password')
        pic = request.FILES.get('pic')

        # Check if mobile number already exists
        if PatientReg.objects.filter(mobno=mobno).exists():
            messages.error(request, "Mobile number already registered!")
            return redirect('patient_registration')

        # Save the patient record
        patient = PatientReg(
            first_name=first_name,
            last_name=last_name,
            email=email,
            gender=gender,
            username=username,
            mobno=mobno,
            address=address,
            password=password,  # Consider hashing the password
            pic=pic
        )
        patient.save()
        messages.success(request, "Registration successful! You can now log in.")
        return redirect('login')  # Redirect to login page

    return render(request, 'patient_registration.html')

# Doctor Registration View
def doctor_registration(request):
    days = Day.objects.all()
    specializations = Specialization.objects.all()

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email')
        mobilenumber = request.POST.get('mobno')
        specialization_id = request.POST.get('specialization_id')
        fee = request.POST.get('fees')
        timings = request.POST.get('timings')
        available_days = request.POST.getlist('available_days')  # Get list of days

        # Save doctor record
        doctor = DoctorReg(
            admin=request.user,
            fee=fee,
            mobilenumber=mobilenumber,
            specialization_id=specialization_id,
            timings=timings,
        )

        # Add available days to the doctor
        for day_id in available_days:
            day = Day.objects.get(id=day_id)
            doctor.available_days.add(day)

        doctor.save()
        messages.success(request, "Doctor registered successfully")
        return redirect('doctor_home')  # Redirect to doctor home or wherever needed

    context = {'days': days, 'specializations': specializations}
    return render(request, 'doctor_registration.html', context)

