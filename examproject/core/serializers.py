from rest_framework import serializers
from .models import Role, Gadget

class GedgetSer(serializers.ModelSerializer):
    class Meta:
        model = Gadget
        fields = ["id", "name", "description", "price"]