from django.urls import path
from . import views

urlpatterns = [
    path("write/", views.write, name="write"),
    path("get_all/", views.get_all, name="get_all"),
    path("get_all_unread/", views.get_all_unread, name="get_all_unread"),
    path("get_message/<int:mes_id>", views.get_message, name="get_message"),
    path("delete_message/<int:id>", views.delete_message, name="delete_message"),
]