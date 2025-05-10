from multiprocessing import context
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from dasapp.models import DoctorReg,Specialization,CustomUser,Appointment,AddPatient,MedicalHistory
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime

def DOCSIGNUP(request):
    specialization = Specialization.objects.all()
    if request.method == "POST":
        pic = request.FILES.get('pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        mobno = request.POST.get('mobno')
        fees = request.POST.get('fees')
        specialization_id = request.POST.get('specialization_id')
        password = request.POST.get('password')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request,'Email already exist')
            return redirect('docsignup')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request,'Username already exist')
            return redirect('docsignup')
        else:
            user = CustomUser(
               first_name=first_name,
               last_name=last_name,
               username=username,
               email=email,
               user_type=2,
               profile_pic = pic,
               
            )
            user.set_password(password)
            user.save()
            spid =Specialization.objects.get(id=specialization_id)
            doctor = DoctorReg(
                admin = user,
                fee = fees,
                mobilenumber = mobno,
                specialization_id = spid,
                
            )
            doctor.save()            
            messages.success(request,'Signup Successfully')
            return redirect('docsignup')
    
    context = {
        'specialization':specialization
    }

    return render(request,'doc/docreg.html',context)

@login_required(login_url='/')
def DOCTORHOME(request):
    doctor_admin = request.user
    doctor_reg = DoctorReg.objects.get(admin=doctor_admin)
    allaptcount = Appointment.objects.filter(doctor_id=doctor_reg).count
    newaptcount = Appointment.objects.filter(status='0',doctor_id=doctor_reg).count
    appaptcount = Appointment.objects.filter(status='Approved',doctor_id=doctor_reg).count
    canaptcount = Appointment.objects.filter(status='Canceled',doctor_id=doctor_reg).count
    doctor_admin = request.user
    doct_id = DoctorReg.objects.get(admin=doctor_admin)
    patcount = AddPatient.objects.filter(doctor_id=doct_id).count
    context = {
        'newaptcount':newaptcount,
        'allaptcount':allaptcount,
        'appaptcount':appaptcount,
        'canaptcount':canaptcount,
        'patcount':patcount        


    }
    return render(request,'doc/dochome.html',context)

def Add_Patient(request):
    if request.method == "POST":
        name = request.POST.get('name')
        mobilenumber = request.POST.get('mobilenumber')
        email = request.POST.get('email')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        medhistory = request.POST.get('medhistory')
        
        doctor_admin = request.user
        try:
            doct_id = DoctorReg.objects.get(admin=doctor_admin)
        except DoctorReg.DoesNotExist:
            messages.error(request, "Doctor not found")
            return redirect('add_patient')

        if AddPatient.objects.filter(email=email).exists():
            messages.warning(request, 'Email already exists')
            return redirect('add_patient')
        if AddPatient.objects.filter(mobilenumber=mobilenumber).exists():
            messages.warning(request, 'Mobile number already exists')
            return redirect('add_patient')
        
        addpatient = AddPatient(
            name=name,
            mobilenumber=mobilenumber,
            email=email,
            age=age,
            gender=gender,
            address=address,
            medicalhistory=medhistory,
            doctor_id=doct_id
        )
        addpatient.save()            
        messages.success(request, 'Data added successfully')
        return redirect('add_patient')
    
    return render(request, 'doc/add_patient.html')

def Manage_Patient(request):
    doctor_admin = request.user
    doct_id = DoctorReg.objects.get(admin=doctor_admin)
    patde = AddPatient.objects.filter(doctor_id=doct_id)
    context={
        'patde':patde
    }
    return render(request, 'doc/manage_patient.html',context)

@login_required(login_url='/')
def View_Patient(request,id):    
    patient_data = AddPatient.objects.get(id =id)    
    context = {
        
        "pd":patient_data,
    }
    return render(request,'doc/update_patient.html',context)


@login_required(login_url='/')

def edit_patient(request):
    if request.method == "POST":
        pat_id = request.POST.get('pid')
        try:
            patient_edit = AddPatient.objects.get(id=pat_id)
        except AddPatient.DoesNotExist:
            messages.error(request, "Patient details do not exist")
            return redirect('manage_patient')

        # Create a dictionary with updated data
        updated_patient = {
            'name': request.POST.get('name'),
            'mobilenumber': request.POST.get('mobilenumber'),
            'email': request.POST.get('email'),
            'address': request.POST.get('address'),
            'gender': request.POST.get('gender'),
            'age': request.POST.get('age'),
            'medicalhistory': request.POST.get('medhistory')
        }

        # Update the patient_edit object with the updated data
        for field, value in updated_patient.items():
            if value:
                setattr(patient_edit, field, value)

        patient_edit.save()
        messages.success(request, "Patient details have been updated successfully")
        return redirect('manage_patient')

    return render(request, 'manage_patient.html')

@login_required(login_url='/')
def ViewCheckPatient(request,id):    
    patient_data = AddPatient.objects.get(id =id) 
    medrec_data = MedicalHistory.objects.filter(pat_id =id)    
    context = {
        
        "pd":patient_data,
        "mrd":medrec_data,
    }
    return render(request,'doc/update_patientmdrec.html',context)

def update_med_rec_patient(request):
    if request.method == 'POST':
        patient_id = request.POST.get('p_id')
        bloodpressure = request.POST.get('bloodpressure')
        weight = request.POST.get('weight')
        bloodsugar = request.POST.get('bloodsugar')
        bodytemp = request.POST.get('bodytemp')
        prescription = request.POST.get('prescription')

        try:
            patient_instance = AddPatient.objects.get(id=patient_id)
        except AddPatient.DoesNotExist:
            messages.error(request, "Patient does not exist")
            return redirect('manage_patient')

        medical_history = MedicalHistory(
            pat_id=patient_instance,
            bloodpressure=bloodpressure,
            weight=weight,
            bloodsugar=bloodsugar,
            bodytemp=bodytemp,
            prescription=prescription
        )
        medical_history.save()
        messages.success(request, "Medical record added successfully")
        return redirect('manage_patient')
    
    return render(request, 'doc/update_patientmdrec.html')

def View_Appointment(request):
    try:
        doctor_admin = request.user
        doctor_reg = DoctorReg.objects.get(admin=doctor_admin)
        view_appointment = Appointment.objects.filter(doctor_id=doctor_reg)
        

        # Pagination
        paginator = Paginator(view_appointment, 5)  # Show 10 appointments per page
        page = request.GET.get('page')
        try:
            view_appointment = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            view_appointment = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            view_appointment = paginator.page(paginator.num_pages)

        context = {'view_appointment': view_appointment}
    except Exception as e:
        # Handle exceptions, such as database errors, gracefully
        context = {'error_message': str(e)}

    return render(request, 'doc/view_appointment.html', context)


def Patient_Appointment_Details(request,id):
    patientdetails=Appointment.objects.filter(id=id)
    context={'patientdetails':patientdetails

    }

    return render(request,'doc/patient_appointment_details.html',context)


def Patient_Appointment_Details_Remark(request):
    if request.method == 'POST':
        patient_id = request.POST.get('pat_id')
        remark = request.POST['remark']
        status = request.POST['status']
        patientaptdet = Appointment.objects.get(id=patient_id)
        patientaptdet.remark = remark
        patientaptdet.status = status
        patientaptdet.save()
        messages.success(request,"Status Update successfully")
        return redirect('view_appointment')
    return render(request,'doc/view_appointment.html',context)

def Patient_Approved_Appointment(request):
    doctor_admin = request.user
    doctor_reg = DoctorReg.objects.get(admin=doctor_admin)
    patientdetails1 = Appointment.objects.filter(status='Approved',doctor_id=doctor_reg)
    context = {'patientdetails1': patientdetails1}
    return render(request, 'doc/patient_app_appointment.html', context)

def Patient_Cancelled_Appointment(request):
    doctor_admin = request.user
    doctor_reg = DoctorReg.objects.get(admin=doctor_admin)
    patientdetails1 = Appointment.objects.filter(status='Canceled',doctor_id=doctor_reg)
    context = {'patientdetails1': patientdetails1}
    return render(request, 'doc/patient_app_appointment.html', context)

def Patient_New_Appointment(request):
    doctor_admin = request.user
    doctor_reg = DoctorReg.objects.get(admin=doctor_admin)
    patientdetails1 = Appointment.objects.filter(status='0',doctor_id=doctor_reg)
    context = {'patientdetails1': patientdetails1}
    return render(request, 'doc/patient_app_appointment.html', context)

def Patient_List_Approved_Appointment(request):
    doctor_admin = request.user
    doctor_reg = DoctorReg.objects.get(admin=doctor_admin)
    patientdetails1 = Appointment.objects.filter(status='Approved',doctor_id=doctor_reg)
    context = {'patientdetails1': patientdetails1}
    return render(request, 'doc/patient_list_app_appointment.html', context)

def DoctorAppointmentList(request,id):
    patientdetails=Appointment.objects.filter(id=id)
    context={'patientdetails':patientdetails

    }

    return render(request,'doc/doctor_appointment_list_details.html',context)

def Patient_Appointment_Prescription(request):
    if request.method == 'POST':
        patient_id = request.POST.get('pat_id')
        prescription = request.POST['prescription']
        recommendedtest = request.POST['recommendedtest']
        status = request.POST['status']
        patientaptdet = Appointment.objects.get(id=patient_id)
        patientaptdet.prescription = prescription
        patientaptdet.recommendedtest = recommendedtest
        patientaptdet.status = status
        patientaptdet.save()
        messages.success(request,"Status Update successfully")
        return redirect('view_appointment')
    return render(request,'doc/patient_list_app_appointment.html',context)


def Patient_Appointment_Completed(request):
    doctor_admin = request.user
    doctor_reg = DoctorReg.objects.get(admin=doctor_admin)
    patientdetails1 = Appointment.objects.filter(status='Completed',doctor_id=doctor_reg)
    context = {'patientdetails1': patientdetails1}
    return render(request, 'doc/patient_list_app_appointment.html', context)

def Search_Appointments(request):
    doctor_admin = request.user
    try:
        doctor_reg = DoctorReg.objects.get(admin=doctor_admin)
    except DoctorReg.DoesNotExist:
        messages.error(request, "Doctor not found")
        return redirect('some_fallback_url')  # Use a fallback URL if needed

    if request.method == "GET":
        query = request.GET.get('query', '')
        if query:
            # Filter records where fullname or Appointment Number contains the query
            patient = Appointment.objects.filter(
                doctor_id=doctor_reg
            ).filter(
                pat_id__admin__first_name__icontains=query
            ) | Appointment.objects.filter(
                appointmentnumber__icontains=query
            ).filter(
                doctor_id=doctor_reg
            )
            messages.success(request, f"Search results for '{query}'")
            return render(request, 'doc/search-appointment.html', {'patient': patient, 'query': query})
        else:
            messages.info(request, "Please enter a search term")
            return render(request, 'doc/search-appointment.html', {})


@login_required(login_url='/')
def Search_Patient(request):
    doctor_admin = request.user
    try:
        doctor_reg = DoctorReg.objects.get(admin=doctor_admin)
    except DoctorReg.DoesNotExist:
        messages.error(request, "Doctor not found")
        return redirect('some_fallback_url')  # Replace with your actual fallback URL

    if request.method == "GET":
        query = request.GET.get('query', '')
        if query:
            searchpat = AddPatient.objects.filter(
                doctor_id=doctor_reg
            ).filter(
                name__icontains=query) | AddPatient.objects.filter(mobilenumber__icontains=query).filter(doctor_id=doctor_reg)
            
            messages.info(request, f"Search results for '{query}'")
            return render(request, 'doc/search-patient.html', {'searchpat': searchpat, 'query': query})
        else:
            
            return render(request, 'doc/search-patient.html', {})

def Between_Date_Report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    patient = []
    doctor_admin = request.user
    doctor_reg = DoctorReg.objects.get(admin=doctor_admin)

    if start_date and end_date:
        # Validate the date inputs
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return render(request, 'doc/between-dates-report.html', {'patient': patient, 'error_message': 'Invalid date format'})

        # Filter Appointment between the given date range
        patient = Appointment.objects.filter(created_at__range=(start_date, end_date)) & Appointment.objects.filter(doctor_id=doctor_reg)

    return render(request, 'doc/between-dates-report.html', {'patient': patient,'start_date':start_date,'end_date':end_date})

def Between_Date_Patient_Report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    patient = []
    doctor_admin = request.user
    doctor_reg = DoctorReg.objects.get(admin=doctor_admin)

    if start_date and end_date:
        # Validate the date inputs
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return render(request, 'doc/between-dates-patient-report.html', {'patient': patient, 'error_message': 'Invalid date format'})

        # Filter Patient between the given date range
        patient = AddPatient.objects.filter(regdate_at__range=(start_date, end_date)) & AddPatient.objects.filter(doctor_id=doctor_reg)

    return render(request, 'doc/between-dates-patient-report.html', {'patient': patient,'start_date':start_date,'end_date':end_date})
