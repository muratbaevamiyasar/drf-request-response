from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.core.files.uploadedfile import InMemoryUploadedFile

from .models import Item
from .serializers import ItemsQueryParamsSerializer, ItemSerializer



class ItemListView(APIView):
    
    def get(self, request: Request) -> Response:
        # min_price, max_price, limit, category, is_actice
        # /api/books/?min_price=23&max_price=213&limit=20&category=tech&is_actice=true

        query_params = request.query_params

        query_serializer = ItemsQueryParamsSerializer(data=query_params)

        if query_serializer.is_valid(raise_exception=True):
            
            items = Item.objects.all()

            item_serializer = ItemSerializer(items, many=True)

            return Response(item_serializer.data, status=status.HTTP_200_OK)

        return Response(data="error", status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request: Request) -> Response:
        data = request.data

        item_serializer = ItemSerializer(data=data)
        if item_serializer.is_valid(raise_exception=True):
            validated_data = item_serializer.validated_data

            item = Item(
                name=validated_data['name'],
                desc=validated_data['desc'],
                price=validated_data['price'],
                category=validated_data['category'],
                is_active=validated_data['is_active'],
            )
            item.save()

            response_serializer = ItemSerializer(item)

            return Response(response_serializer.data)


class ItemDetailView(APIView):
    
    def get(self, request: Request, pk: int) -> Response:

        item = Item.objects.filter(pk=pk).first()
        if item:
            serializer = ItemSerializer(item)

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'error': 'no item'}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request: Request, pk: int) -> Response:
        return Response({'method': 'put'}, status=status.HTTP_200_OK)

    def delete(self, request: Request, pk: int) -> Response:
        return Response({'method': 'delete'}, status=status.HTTP_204_NO_CONTENT)


# client(chrome, js, postman) -> WSGI -> URL -> View (HttpRequest) -> APIView (Request)
# client(chrome, js, postman) <- WSGI -> URL <- View (HttpResponse) <- APIView (Response)

