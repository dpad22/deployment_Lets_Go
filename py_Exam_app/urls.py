from django.urls import path
from . import views


urlpatterns = [
    path('',views.landing_page),
    path('main',views.main),
    path('register_user',views.register_user),
    path('user_page',views.user_page),
    path('user_page/add',views.renderAdd),
    path('postTravel', views.postTravel),
    path('addDestination/<int:tripId>', views.addDestination),
    path('view/<int:tripId>', views.viewTrip),
    path('login', views.user_login),
    path('logout', views.logout)

]