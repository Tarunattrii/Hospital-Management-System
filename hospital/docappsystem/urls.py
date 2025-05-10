"""
URL configuration for docappsystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from dasapp import views
from .import views,adminviews,docviews,userviews
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from django.contrib import admin
from django.urls import path
from docappsystem import adminviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', views.BASE, name='base'),
    path('login', views.LOGIN, name='login'),
    
    path('doLogin', views.doLogin, name='doLogin'),
    path('doLogout', views.doLogout, name='logout'),

    # This is admin panel
    path('Admin/AdminHome', adminviews.ADMINHOME, name='admin_home'),
    path('Admin/Specialization', adminviews.SPECIALIZATION, name='add_specilizations'),
    path('Admin/ManageSpecialization', adminviews.MANAGESPECIALIZATION, name='manage_specilizations'),
    path('Admin/DeleteSpecialization/<str:id>', adminviews.DELETE_SPECIALIZATION, name='delete_specilizations'),
    path('UpdateSpecialization/<str:id>', adminviews.UPDATE_SPECIALIZATION, name='update_specilizations'),
    path('UPDATE_Specialization_DETAILS', adminviews.UPDATE_SPECIALIZATION_DETAILS, name='update_specilizations_details'),
    path('Admin/DoctorList', adminviews.DoctorList, name='viewdoctorlist'),
    path('Admin/ViewDoctorDetails/<str:id>', adminviews.ViewDoctorDetails, name='viewdoctordetails'),
    path('Admin/ViewDoctorAppointmentList/<str:id>', adminviews.ViewDoctorAppointmentList, name='viewdoctorappointmentlist'),
    path('Admin/ViewDOCPatient/<str:id>', adminviews.View_DOCPatient, name='viewdocpatient'),
    path('Admin/ViewCheckPatient/<str:id>', adminviews.ViewCheckAddPatient, name='viewcheckaddpatient'),
   
    path('Admin/ViewPatientDetails/<str:id>', adminviews.ViewPatientDetails, name='viewpatientdetails'),
    path('SearchDoctor', adminviews.Search_Doctor, name='search_doctor'),
    path('Admin/RegUsers', adminviews.RegUsersDetails, name='regusers'),
    path('Admin/DeleteRegusers/<str:id>', adminviews.DELETE_REGUSERS, name='delusersdetails'),
    path('Admin/RegUserAppointment/<str:id>', adminviews.Reg_User_Appoinments, name='regusersapp'),
    path('admin/', adminviews.BED_VACANCY, name='bed_vacancy'),
    path('admin/wards/', adminviews.WARD_LIST, name='ward_list'),
    path('admin/add-ward/', adminviews.ADD_WARD, name='add_ward'),
    path('admin/edit-ward/<int:id>/', adminviews.EDIT_WARD, name='edit_ward'),
    path('admin/delete-ward/<int:id>/', adminviews.DELETE_WARD, name='delete_ward'),
    path('admin/bed-types/', adminviews.BED_TYPE_LIST, name='bed_type_list'),
    path('admin/add-bed-type/', adminviews.ADD_BED_TYPE, name='add_bed_type'),
    path('admin/edit-bed-type/<int:id>/', adminviews.EDIT_BED_TYPE, name='edit_bed_type'),
    path('admin/delete-bed-type/<int:id>/', adminviews.DELETE_BED_TYPE, name='delete_bed_type'),
    path('admin/beds/', adminviews.BED_LIST, name='bed_list'),
    path('admin/add-bed/', adminviews.ADD_BED, name='add_bed'),
    path('admin/edit-bed/<int:id>/', adminviews.EDIT_BED, name='edit_bed'),
    path('admin/delete-bed/<int:id>/', adminviews.DELETE_BED, name='delete_bed'),
    path('admin/toggle-bed-status/<int:id>/', adminviews.TOGGLE_BED_STATUS, name='toggle_bed_status'),
    path('admin/', include('docappsystem.bed_management_urls')),
    path('admin/', adminviews.BED_VACANCY, name='bed_vacancy'),
    path('admin/wards/', adminviews.WARD_LIST, name='ward_list'),
    path('admin/add-ward/', adminviews.ADD_WARD, name='add_ward'),
    path('admin/bed-management/', include('docappsystem.bed_management_urls')),

    path('DoctorBetweenDateReport', adminviews.Doctor_Between_Date_Report, name='doctor_between_date_report'),

    #Website Page
     path('Website/update', adminviews.WEBSITE_UPDATE, name='website_update'),
     path('UPDATE_WEBSITE_DETAILS', adminviews.UPDATE_WEBSITE_DETAILS, name='update_website_details'),

    # This is Doctor Panel
    path('docsignup/', docviews.DOCSIGNUP, name='docsignup'),
    path('Doctor/DocHome', docviews.DOCTORHOME, name='doctor_home'),
    path('Doctor/AddPatient', docviews.Add_Patient, name='add_patient'),
    path('Doctor/ManagePatient', docviews.Manage_Patient, name='manage_patient'),
    path('Doctor/ViewPatient/<str:id>', docviews.View_Patient, name='viewpatient'),
    path('Doctor/EditPatient', docviews.edit_patient, name='editpatient'),
    path('Doctor/ViewCheckPatient/<str:id>', docviews.ViewCheckPatient, name='viewcheckpatient'),
    path('Doctor/UpdateMedRecPatient', docviews.update_med_rec_patient, name='updatemedrecpatient'),
    path('Doctor/ViewAppointment', docviews.View_Appointment, name='view_appointment'),
    path('DoctorPatientAppointmentDetails/<str:id>', docviews.Patient_Appointment_Details, name='patientappointmentdetails'),
    path('AppointmentDetailsRemark/Update', docviews.Patient_Appointment_Details_Remark, name='patient_appointment_details_remark'),
    path('DoctorPatientApprovedAppointment', docviews.Patient_Approved_Appointment, name='patientapprovedappointment'),
    path('DoctorPatientCancelledAppointment', docviews.Patient_Cancelled_Appointment, name='patientcancelledappointment'),
    path('DoctorPatientNewAppointment', docviews.Patient_New_Appointment, name='patientnewappointment'),
    path('DoctorPatientListApprovedAppointment', docviews.Patient_List_Approved_Appointment, name='patientlistappointment'),
    path('DoctorAppointmentList/<str:id>', docviews.DoctorAppointmentList, name='doctorappointmentlist'),
    path('PatientAppointmentPrescription', docviews.Patient_Appointment_Prescription, name='patientappointmentprescription'),
    path('PatientAppointmentCompleted', docviews.Patient_Appointment_Completed, name='patientappointmentcompleted'),
    path('SearchAppointment', docviews.Search_Appointments, name='search_appointment'),
    path('SearchPatient', docviews.Search_Patient, name='search_patient'),
    path('BetweenDateReport', docviews.Between_Date_Report, name='between_date_report'),
    path('BetweenDatePatientReport', docviews.Between_Date_Patient_Report, name='between_date_patient_report'),

    #This is User Panel
    path('PatientRegsitratios', userviews.PATIENTREGISTRATION, name='patreg'),
    path('Pat/PatHome', userviews.PATIENTHOME, name='userhome'),
    path('userbase/', userviews.USERBASE, name='userbase'),
    path('', userviews.Index, name='index'),
    path('patientappointment/', userviews.create_appointment, name='patientappointment'),
    
    path('get_doctor/', userviews.get_doctor, name='get_doctor'),
    path('User_SearchAppointment', userviews.User_Search_Appointments, name='user_search_appointment'),
    path('ViewAppointmentHistory', userviews.View_Appointment_History, name='view_appointment_history'),
    path('cancel_appointment/<str:id>', userviews.cancel_appointment, name='cancel_appointment'),
    path('ViewAppointmentDetails/<str:id>/', userviews.View_Appointment_Details, name='viewappointmentdetails'),
    path('Doctor', userviews.Doctor, name='doctor'),
    path('Aboutus', userviews.Aboutus, name='aboutus'),
    path('Contactus', userviews.Contactus, name='contactus'),



 
    
    



    #profile path
    path('Profile', views.PROFILE, name='profile'),
    path('Profile/update', views.PROFILE_UPDATE, name='profile_update'),
    path('Password', views.CHANGE_PASSWORD, name='change_password'),
    
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
