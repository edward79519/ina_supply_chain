from django.urls import path
from . import ajax
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
    path('inquiry/', views.inquiry_list, name="Inquiry_List"),
    path('inquiry/add/', views.inquiry_add, name="Inquiry_Add"),
    path('inquiry/<int:inqry_id>/', views.inquiry_detail, name="Inquiry_Detail"),
    path('inquiry/<int:inqry_id>/addnewquota/', views.quota_newadd, name="Quota_Add"),
    path('inquiry/<int:inqry_id>/close/', views.inquiry_close, name="Inquiry_Close"),
    path('inquiry/<int:inqry_id>/exportxls', views.inquiry_export, name="Inquiry_Eptxls"),
    path('quota/<int:quota_id>/', views.quota_inpageupdate, name="Quota_Inpgupdate"),
    path('ajax/itemdetail/', ajax.getdetail, name="Ajax_Getitem"),
]
