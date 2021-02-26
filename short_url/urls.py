from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("new", views.new, name="new"),
    path("new_with_short_specified", views.new_with_short_specified, name="new_with_short_specified"),
    path("<slug:short_id>", views.show, name="show"),
]
