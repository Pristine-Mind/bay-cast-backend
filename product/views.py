from django.db.models import F
from collections import defaultdict
from django.utils import timezone
from rest_framework import viewsets, response, status
from rest_framework.decorators import action
from rest_framework.views import APIView

from .models import Product, Process, Station
from .serializers import (
    ProductSerializer,
    ProcessSerializer,
    StationSerialzier,
    StationProductProcessSerializer
)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(
        detail=True, methods=['post']
    )
    def update_product(self, request, pk=None):
        product = self.get_object()
        is_checked = request.data.get('is_checked')
        move_to = request.data.get('move_to')
        if is_checked:
            process = Process.objects.filter(product=product).first()
            process.exit_time = timezone.now()
            process.save()

            # create new process objects after the project is moved
            if not Process.objects.filter(product=product, station=move_to).exists():
                Process.objects.create(
                    product=product,
                    station_id=move_to,
                    entry_time=timezone.now()
                )
            return response.Response(
                {'is_checked': 'Updated'}
            )
        return response.response("Couldn't update", status=status.HTTP_400_BAD_REQUEST)


class ProcessViewSet(viewsets.ModelViewSet):
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer


class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerialzier


class StationProductProcessView(APIView):

    def get(self, request):
        data = Process.objects.select_related('product', 'station').values(
            'station__name',
            'product__product_id',
            'product__product_name',
            'entry_time',
            'exit_time'
        ).order_by('station_id')

        # Grouping the data by station
        grouped_data = defaultdict(list)
        for item in data:
            station_name = item['station__name']
            product_info = {
                'product_id': item['product__product_id'],
                'product_name': item['product__product_name'],
                'entry_time': item['entry_time'],
                'exit_time': item['exit_time']
            }
            grouped_data[station_name].append(product_info)

        # Prepare the data for serialization
        response_data = [
            {
                'station_name': station,
                'products': products
            }
            for station, products in grouped_data.items()
        ]

        serializer = StationProductProcessSerializer(response_data, many=True)
        return response.Response(serializer.data)
