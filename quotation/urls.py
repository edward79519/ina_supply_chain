from django.urls import path
from . import views

urlpatterns = [
    path('company/', views.comp_list, name="Comp_Index"),
    path('company/add/', views.comp_add, name="Comp_Add"),
    path('company/<int:comp_id>/', views.comp_detail, name="Comp_Detail"),
    path('company/<int:comp_id>/update/', views.comp_update, name="Comp_Update"),
    path('item/', views.item_list, name="Item_Lsit"),
    path('item/add/', views.item_add, name="Item_add"),
    path('item/<int:item_id>/', views.item_detail, name="Item_Detail"),
    path('item/<int:item_id>/update/', views.item_update, name="Item_Update"),
]