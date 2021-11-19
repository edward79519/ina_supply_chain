from django.urls import path
from . import views

urlpatterns = [
    path('company/', views.comp_list, name="Comp_Index"),
    path('company/add/', views.comp_add, name="Comp_Add"),
    path('company/<int:comp_id>/', views.comp_detail, name="Comp_Detail"),
    path('company/<int:comp_id>/update/', views.comp_update, name="Comp_Update"),
    path('item/', views.item_list, name="Item_Lsit"),
]