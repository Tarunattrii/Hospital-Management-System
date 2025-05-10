from django.urls import path
from docappsystem import adminviews
urlpatterns = [
    path('bed-vacancy/', adminviews.BED_VACANCY, name='bed_vacancy'),
    path('wards/', adminviews.WARD_LIST, name='ward_list'),
    path('add-ward/', adminviews.ADD_WARD, name='add_ward'),
    path('edit-ward/<int:id>/', adminviews.EDIT_WARD, name='edit_ward'),
    path('delete-ward/<int:id>/', adminviews.DELETE_WARD, name='delete_ward'),
    path('bed-types/', adminviews.BED_TYPE_LIST, name='bed_type_list'),
    path('add-bed-type/', adminviews.ADD_BED_TYPE, name='add_bed_type'),
    path('edit-bed-type/<int:id>/', adminviews.EDIT_BED_TYPE, name='edit_bed_type'),
    path('delete-bed-type/<int:id>/', adminviews.DELETE_BED_TYPE, name='delete_bed_type'),
    path('beds/', adminviews.BED_LIST, name='bed_list'),
    path('add-bed/', adminviews.ADD_BED, name='add_bed'),
    path('edit-bed/<int:id>/', adminviews.EDIT_BED, name='edit_bed'),
    path('delete-bed/<int:id>/', adminviews.DELETE_BED, name='delete_bed'),
    path('toggle-bed-status/<int:id>/', adminviews.TOGGLE_BED_STATUS, name='toggle_bed_status'),
]