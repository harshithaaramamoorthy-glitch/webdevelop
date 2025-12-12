from django.urls import path
from.views import germyListCreateView, germyDetailView

urlpatterns = [
    path('germy/', germyListCreateView.as_view(),name = 'germy-list-create'),
    path('germy/<int:pk>/', germyDetailView.as_view(),name= 'germy-Detail'),
    
]