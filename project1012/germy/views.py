from django.shortcuts import render

from  rest_framework import generics
from.models import germy
from.serializers import germyserializer

class germyListCreateView(generics.ListCreateAPIView):
    queryset = germy.objects.all()
    serializer_class = germyserializer

class germyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = germy.objects.all()
    serializer_class = germyserializer 
