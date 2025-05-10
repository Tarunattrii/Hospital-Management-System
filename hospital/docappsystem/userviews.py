from multiprocessing import context
from django.shortcuts import render,redirect,HttpResponse
from dasapp.models import DoctorReg,Specialization,CustomUser,Appointment,Page,PatientReg
from django.http import JsonResponse
import random
from datetime import datetime
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

def USERBASE(request):
    
    return render(request, 'userbase.html',context)



def PATIENTREGISTRATION(request):
    if request.method == "POST":
        pic = request.FILES.get('pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email')
        mobno = request.POST.get('mobno')
        gender = request.POST.get('gender')
        username = request.POST.get('username')
        address = request.POST.get('address')
        password = request.POST.get('password')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request,'Email already exist')
            return redirect('patreg')
        
        else:
            user = CustomUser(
               first_name=first_name,
               last_name=last_name,
               username=username,
               email=email,
               user_type=3,
               profile_pic = pic,
            )
            user.set_password(password)
            user.save()
            
            patient = PatientReg(
                admin = user,
                mobilenumber = mobno,
                gender = gender,
                address = address,
            )
            patient.save()            
            messages.success(request,'Signup Successfully')
            return redirect('patreg')
    

    return render(request, 'user/patient-reg.html')

def PATIENTHOME(request):
    doctor_count = DoctorReg.objects.all().count
    specialization_count = Specialization.objects.all().count
    context = {
        'doctor_count':doctor_count,
        'specialization_count':specialization_count,

    } 
    return render(request,'user/userhome.html',context)

def Index(request):
    doctorview = DoctorReg.objects.all()
    first_page = Page.objects.first()

    context = {'doctorview': doctorview,
    'page':first_page,
    }
    return render(request, 'index.html',context)

def Doctor(request):
    doctorview = DoctorReg.objects.all()
    first_page = Page.objects.first()

    context = {'dv': doctorview,
    'page':first_page,
    }
    return render(request, 'doctor.html',context)

def Aboutus(request):
   
    first_page = Page.objects.first()

    context = {
    'page':first_page,
    }
    return render(request, 'aboutus.html',context)

def Contactus(request):
   
    first_page = Page.objects.first()

    context = {
    'page':first_page,
    }
    return render(request, 'contactus.html',context)

def get_doctor(request):
    if request.method == 'GET':
        s_id = request.GET.get('s_id')
        doctors = DoctorReg.objects.filter(specialization_id=s_id)
        
        doctor_options = ''
        for doc in doctors:
            doctor_options += f'<option value="{doc.id}">{doc.admin.first_name}</option>'
        
        return JsonResponse({'doctor_options': doctor_options})

def create_appointment(request):
    specialization = Specialization.objects.all()

    if request.method == "POST":
        try:
            appointmentnumber = random.randint(100000000, 999999999)
            spec_id = request.POST.get('spec_id')
            doctor_id = request.POST.get('doctor_id')
            date_of_appointment = request.POST.get('date_of_appointment')
            time_of_appointment = request.POST.get('time_of_appointment')
            additional_msg = request.POST.get('additional_msg')

            # Retrieve the DoctorReg and Specialization instances
            doc_instance = DoctorReg.objects.get(id=doctor_id)
            spec_instance = Specialization.objects.get(id=spec_id)

            # Accessing the PatientReg instance associated with the logged-in user
            patientreg = request.user.id
            patient_instance = PatientReg.objects.get(admin=patientreg)

            # Validate that date_of_appointment is greater than today's date
            try:
                appointment_date = datetime.strptime(date_of_appointment, '%Y-%m-%d').date()
                today_date = timezone.now().date()

                if appointment_date <= today_date:
                    # If the appointment date is not in the future, display an error message
                    messages.error(request, "Please select a date in the future for your appointment")
                    return redirect('patientappointment')  # Redirect back to the appointment page
            except ValueError:
                # Handle invalid date format error
                messages.error(request, "Invalid date format")
                return redirect('patientappointment')  # Redirect back to the appointment page

            # Create a new Appointment instance with the provided data
            Appointment.objects.create(
                appointmentnumber=appointmentnumber,
                pat_id=patient_instance,
                spec_id=spec_instance,
                doctor_id=doc_instance,
                date_of_appointment=date_of_appointment,
                time_of_appointment=time_of_appointment,
                additional_msg=additional_msg
            )

            # Display a success message
            messages.success(request, "Your Appointment Request Has Been Sent. We Will Contact You Soon")
            return redirect('patientappointment')

        except DoctorReg.DoesNotExist:
            messages.error(request, "Selected doctor does not exist.")
        except Specialization.DoesNotExist:
            messages.error(request, "Selected specialization does not exist.")
        except PatientReg.DoesNotExist:
            messages.error(request, "Patient information could not be retrieved.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

        return redirect('patientappointment')  # Redirect back to the appointment page in case of an error

    context = {
        'specialization': specialization
    }
    return render(request, 'user/appointment.html', context)





def View_Appointment_History(request):
    pat_reg = request.user
    pat_admin = PatientReg.objects.get(admin=pat_reg)
    userapptdetails = Appointment.objects.filter(pat_id=pat_admin)
    context = {
        'vah':userapptdetails
    }
    return render(request, 'user/appointment-history.html', context)

def cancel_appointment(request, id):
    try:
        appointment = Appointment.objects.get(id=id, pat_id=request.user.patientreg)
        if appointment.status != 'Approved':
            appointment.status = 'Canceled'
            appointment.save()
            messages.success(request, "Your appointment has been canceled successfully.")
        else:
            messages.error(request, "You cannot cancel this appointment.")
    except Appointment.DoesNotExist:
        messages.error(request, "Appointment not found.")
    return redirect('view_appointment_history')

def User_Search_Appointments(request):
    page = Page.objects.all()
    
    if request.method == "GET":
        query = request.GET.get('query', '')
        if query:
            # Filter records where fullname or Appointment Number contains the query
            patient = Appointment.objects.filter(fullname__icontains=query) | Appointment.objects.filter(appointmentnumber__icontains=query)
            messages.info(request, "Search against " + query)
            context = {'patient': patient, 'query': query, 'page': page}
            return render(request, 'search-appointment.html', context)
        else:
            print("No Record Found")
            context = {'page': page}
            return render(request, 'search-appointment.html', context)
    
    # If the request method is not GET
    context = {'page': page}
    return render(request, 'search-appointment.html', context)
def View_Appointment_Details(request,id):
    page = Page.objects.all()
    patientdetails=Appointment.objects.filter(id=id)
    context={'patientdetails':patientdetails,
    'page': page

    }

    return render(request,'user_appointment-details.html',context)




