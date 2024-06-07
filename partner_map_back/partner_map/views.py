import pandas as pd
from rest_framework.views import APIView
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from .models import LegalFace, Brand, GeoData, Bonus
from .parsers import ExcelParser
from rest_framework.permissions import IsAdminUser
from .serializers import LegalFaceSerializer, BrandSerializer, GeoDataSerializer, BonusSerializer, \
    BonusValueUpdateSerializer


# import pandas as pd


class LegalFaceViewSet(viewsets.ModelViewSet):
    queryset = LegalFace.objects.all()
    serializer_class = LegalFaceSerializer
    permission_classes = [IsAdminUser]


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAdminUser]


class BonusListView(generics.ListAPIView):
    queryset = Bonus.objects.all()
    serializer_class = BonusSerializer
    permission_classes = [IsAdminUser]


class GeoDataViewSet(viewsets.ModelViewSet):
    queryset = GeoData.objects.all()
    serializer_class = GeoDataSerializer
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['delete'], url_path='delete_by_legal_face')
    def delete_by_legal_face(self, request):
        legal_face_id = request.query_params.get('legal_face')
        if legal_face_id:
            deleted_count, _ = GeoData.objects.filter(legal_face_id=legal_face_id).delete()
            return Response({'deleted': deleted_count}, status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'legal_face parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'], url_path='delete_by_brand')
    def delete_by_brand(self, request):
        brand_id = request.query_params.get('brand')
        if brand_id:
            deleted_count, _ = GeoData.objects.filter(brand_id=brand_id).delete()
            return Response({'deleted': deleted_count}, status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'brand parameter is required'}, status=status.HTTP_400_BAD_REQUEST)


class GeoDataUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAdminUser]

    def post(self, request, format=None):
        file = request.FILES.get('file')
        if not file:
            return Response({"detail": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        if not file.name.endswith('.xlsx'):
            return Response({"detail": "Invalid file format"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            data = pd.read_excel(file, engine='openpyxl')
        except Exception as e:
            return Response({"detail": "Error reading the file"}, status=status.HTTP_400_BAD_REQUEST)

        geo_data_instances = []
        for index, row in data.iterrows():
            try:
                entity = LegalFace.objects.get(id=row['Entity'])
            except LegalFace.DoesNotExist:
                return Response({"detail": f"Entity with ID {row['Entity']} does not exist"},
                                status=status.HTTP_400_BAD_REQUEST)

            try:
                brand = Brand.objects.get(id=row['Brand'])
            except Brand.DoesNotExist:
                return Response({"detail": f"Brand with ID {row['Brand']} does not exist"},
                                status=status.HTTP_400_BAD_REQUEST)

            geo_data, created = GeoData.objects.update_or_create(
                coordinates=row['Coordinates'],
                defaults={
                    'type': row['Type'],
                    'entity': entity,
                    'brand': brand,
                    'region': row['Region'],
                    'address': row['Address'],
                    'nomenclature': row['Nomenclature'],
                    'discount': row['Discount'],
                    'nds': row['NDS'],
                    'logo': row['logo'],
                    'status': row['Status']
                }
            )

            if 'Bonuses' in row:
                bonus_ids = row['Bonuses'].split(',')
                for bonus_id in bonus_ids:
                    try:
                        bonus = Bonus.objects.get(id_bonus=bonus_id)
                        geo_data.bonuses.add(bonus)
                    except Bonus.DoesNotExist:
                        continue

            geo_data_instances.append(geo_data)

        serializer = GeoDataSerializer(geo_data_instances, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BonusViewSet(viewsets.ModelViewSet):
    queryset = Bonus.objects.all()
    serializer_class = BonusSerializer
    permission_classes = [IsAdminUser]


class GeoDataDeleteAllView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, format=None):
        GeoData.objects.all().delete()
        return Response({"detail": "All GeoData objects have been deleted."}, status=status.HTTP_204_NO_CONTENT)


class BrandDataDeleteAllView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, requests, format=None):
        Brand.objects.all().delete()
        return Response({"detail": "All GeoData objects have been deleted."}, status=status.HTTP_204_NO_CONTENT)


class EntityDataDeleteAllView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, requests, format=None):
        LegalFace.objects.all().delete()
        return Response({"detail": "All GeoData objects have been deleted."}, status=status.HTTP_204_NO_CONTENT)


class BonusDeleteAllView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, requests, format=None):
        Bonus.objects.all().delete()
        return Response({"detail": "All Bonus objects have been deleted."}, status=status.HTTP_204_NO_CONTENT)


class BonusValueUpdateByIdBonusView(generics.UpdateAPIView):
    queryset = Bonus.objects.all()
    serializer_class = BonusValueUpdateSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'id_bonus'

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddBonusToGeoDataByEntity(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, entity_id, bonus_id, format=None):
        try:
            entity = LegalFace.objects.get(id=entity_id)
            bonus = Bonus.objects.get(id_bonus=bonus_id)
        except (LegalFace.DoesNotExist, Bonus.DoesNotExist):
            return Response({"detail": "Entity or Bonus not found."}, status=status.HTTP_404_NOT_FOUND)

        geodata_list = GeoData.objects.filter(entity=entity)
        for geodata in geodata_list:
            geodata.bonuses.add(bonus)

        return Response({"detail": "Bonus added to all GeoData objects for the given entity."},
                        status=status.HTTP_200_OK)


class GetBonusesByEntity(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, entity_id, format=None):
        try:
            entity = LegalFace.objects.get(id=entity_id)
        except LegalFace.DoesNotExist:
            return Response({"detail": "Entity not found."}, status=status.HTTP_404_NOT_FOUND)

        geodata_list = GeoData.objects.filter(entity=entity).prefetch_related('bonuses')
        bonuses = set()
        for geodata in geodata_list:
            for bonus in geodata.bonuses.all():
                bonuses.add(bonus)

        bonus_data = [{"id": bonus.id, "name": bonus.name, "image": bonus.image} for bonus in bonuses]
        return Response(bonus_data, status=status.HTTP_200_OK)


class RemoveBonusFromGeoDataByEntity(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, entity_id, bonus_id, format=None):
        try:
            entity = LegalFace.objects.get(id=entity_id)
            bonus = Bonus.objects.get(id=bonus_id)
        except (LegalFace.DoesNotExist, Bonus.DoesNotExist):
            return Response({"detail": "Entity or Bonus not found."}, status=status.HTTP_404_NOT_FOUND)

        geodata_list = GeoData.objects.filter(entity=entity)
        for geodata in geodata_list:
            geodata.bonuses.remove(bonus)

        return Response({"detail": "Bonus removed from all GeoData objects for the given entity."},
                        status=status.HTTP_200_OK)
