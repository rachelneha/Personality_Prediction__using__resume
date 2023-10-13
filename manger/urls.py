from django.urls import path
from manger import views


urlpatterns = [
    path('signup/', views.signup, name="signup"),
    #path('$', views.index, name="index"),
    # path('', views.dashboard, name="dashboard"),
    path('resume/create/', views.CreateResume.as_view(), name="CreateResume"),
    path('', views.ListResume.as_view(), name="ListResume"),
    path('resume/<int:pk>/', views.DetailResume.as_view(), name="DetailResume"),
    path('resume/<int:pk>/predict/', views.predict, name="predict"),
    path('all-resumes/', views.ListAllResume.as_view(), name="ListAllResume"),
]
