from rest_framework import serializers
from.models import germy


class germyserializer(serializers.ModelSerializer):
    class Meta:
        model = germy
        fields  = '__all__'