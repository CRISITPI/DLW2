from dlw.models import testc
from rest_framework import serializers

class testSerializer(serializers.ModelSerializer):
    class Meta:
        model=testc
        # fields=('id','subject','targetone','targettwo')
        fields = '__all__'

# class brnoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = M2Doc
#         fields = '__all__'