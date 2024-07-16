from django.utils import timezone
from rest_framework import viewsets, response, status
from rest_framework.decorators import action

from .models import Product, Process, Station
from .serializers import ProductSerializer, ProcessSerializer, StationSerialzier


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
