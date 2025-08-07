from django.urls import path
from .views import (
    PropertyListCreateView, PropertyDetailView,
    RegionListView, CityListView, DistrictListView,
    HouseImageListCreateView, LegalDocumentListCreateView,
    HouseReviewListCreateView, ReviewListCreateView,
    FavoriteListView,
    RentalListCreateView, RentalStatusUpdateView
)

urlpatterns = [
    path('properties/', PropertyListCreateView.as_view(), name='property-list-create'),
    path('properties/<int:pk>/', PropertyDetailView.as_view(), name='property-detail'),

    path('regions/', RegionListView.as_view(), name='region-list'),
    path('cities/', CityListView.as_view(), name='city-list'),
    path('districts/', DistrictListView.as_view(), name='district-list'),

    path('house-images/', HouseImageListCreateView.as_view(), name='house-image-list-create'),
    path('legal-documents/', LegalDocumentListCreateView.as_view(), name='legal-document-list-create'),

    path('house-reviews/', HouseReviewListCreateView.as_view(), name='house-review-list-create'),
    path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),

    path('favorites/', FavoriteListView.as_view(), name='favorite-list'),

    path('rentals/', RentalListCreateView.as_view(), name='rental-list-create'),
    path('rentals/<int:pk>/<str:status_action>/', RentalStatusUpdateView.as_view(), name='rental-status-update'),
]
