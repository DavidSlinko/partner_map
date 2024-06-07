from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (LegalFaceViewSet, BrandViewSet, GeoDataViewSet, BonusViewSet, GeoDataUploadView,
                    GeoDataDeleteAllView, BrandDataDeleteAllView, EntityDataDeleteAllView, AddBonusToGeoDataByEntity,
                    GetBonusesByEntity, RemoveBonusFromGeoDataByEntity, BonusListView, BonusDeleteAllView,
                    BonusValueUpdateByIdBonusView)

router = DefaultRouter()
router.register(r'legalfaces', LegalFaceViewSet)
router.register(r'brands', BrandViewSet)
router.register(r'geodata', GeoDataViewSet)
router.register(r'bonuses', BonusViewSet)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', include(router.urls)),
    path('upload-geodata/', GeoDataUploadView.as_view(), name='upload-geodata'),
    path('entity/<uuid:entity_id>/add-bonus/<uuid:bonus_id>/', AddBonusToGeoDataByEntity.as_view(),
         name='add-bonus-to-geodata'),
    path('entity/<uuid:entity_id>/bonuses/', GetBonusesByEntity.as_view(), name='get-bonuses-by-entity'),
    path('entity/<uuid:entity_id>/remove-bonus/<uuid:bonus_id>/', RemoveBonusFromGeoDataByEntity.as_view(),
         name='remove-bonus-from-geodata'),
    path('bonus-list/', BonusListView.as_view(), name='bonus-list'),

    path('update-bonus-value/<str:id_bonus>/', BonusValueUpdateByIdBonusView.as_view(), name='update_bonus_value'),

    # ------------------------- !!! запросы на удаление всех определенных объектов !!! ---------------------------------
    path('delete-all-geodata/', GeoDataDeleteAllView.as_view(), name='delete-all-geodata'),
    path('delete-all-brand/', BrandDataDeleteAllView.as_view(), name='delete-all-brand'),
    path('delete-all-entity/', EntityDataDeleteAllView.as_view(), name='delete-all-entity'),
    path('delete-all-bonus/', BonusDeleteAllView.as_view(), name='delete-all-bonus')
]
