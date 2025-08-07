from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView

from .models import (
    Property, Region, City, District, HouseImage,
    LegalDocument, HouseReview, Review, Favorite, Rental
)
from .serializers import (
    PropertySerializer, RegionSerializer, CitySerializer, DistrictSerializer,
    HouseImageSerializer, LegalDocumentSerializer, HouseReviewSerializer,
    ReviewSerializer, FavoriteSerializer, RentalSerializer
)
from .filters import PropertyFilter


class PropertyListCreateView(generics.ListCreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PropertyFilter
    search_fields = ['title', 'description', 'address']
    ordering_fields = ['price', 'title']


class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer


class RegionListView(generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    search_fields = ['name']


class CityListView(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    search_fields = ['name']


class DistrictListView(generics.ListAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    search_fields = ['name']


class HouseImageListCreateView(generics.ListCreateAPIView):
    queryset = HouseImage.objects.all()
    serializer_class = HouseImageSerializer


class LegalDocumentListCreateView(generics.ListCreateAPIView):
    queryset = LegalDocument.objects.all()
    serializer_class = LegalDocumentSerializer


class HouseReviewListCreateView(generics.ListCreateAPIView):
    queryset = HouseReview.objects.all()
    serializer_class = HouseReviewSerializer


class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class FavoriteListView(generics.ListAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer


class RentalListCreateView(generics.ListCreateAPIView):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Rental.objects.all()

        if user.role == 'seller':
            return Rental.objects.filter(property__seller=user)

        return Rental.objects.filter(renter=user)

    def perform_create(self, serializer):
        property_id = self.request.data.get('property_id')
        try:
            property_obj = Property.objects.get(id=property_id)
        except Property.DoesNotExist:
            raise Response({'error': 'Объект недвижимости не найден'}, status=status.HTTP_404_NOT_FOUND)

        serializer.save(renter=self.request.user, property=property_obj)


class RentalStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, status_action):
        try:
            rental = Rental.objects.get(pk=pk)
        except Rental.DoesNotExist:
            return Response({'error': 'Аренда не найдена'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        if status_action in ['approved', 'rejected']:
            if rental.property.seller != user:
                return Response({'error': 'Вы не владелец объекта'}, status=status.HTTP_403_FORBIDDEN)

        if status_action == 'cancelled':
            if rental.renter != user:
                return Response({'error': 'Вы не арендатор'}, status=status.HTTP_403_FORBIDDEN)

        rental.status = status_action
        rental.save()
        return Response({'status': f'Аренда переведена в состояние: {status_action}'}, status=status.HTTP_200_OK)
