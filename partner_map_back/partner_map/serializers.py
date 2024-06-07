from rest_framework import serializers
from .models import LegalFace, Brand, GeoData, Bonus


class LegalFaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalFace
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class BonusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bonus
        fields = ['id', 'id_bonus', 'name', 'image', 'value']


class BonusValueUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bonus
        fields = ['value']


class GeoDataSerializer(serializers.ModelSerializer):
    bonuses = BonusSerializer(many=True, read_only=True)

    class Meta:
        model = GeoData
        fields = ['id', 'coordinates', 'type', 'region', 'address', 'nomenclature', 'discount', 'nds', 'logo',
                  'status', 'entity', 'brand', 'bonuses']
