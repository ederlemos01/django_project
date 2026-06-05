from rest_framework.response import Response
from rest_framework import status
from .models import Event
from .serializers import EventSerializer
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.permissions import IsAuthenticatedOrReadOnly

@api_view(['GET','POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def event_list(request):

    if request.method == 'GET':
        queryset = Event.objects.filter(is_active=True)
        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = EventSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        


@api_view(['GET', 'PUT','PATCH','DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def event_detail(request, pk):
    
    try:
        event = Event.objects.get(pk=pk, is_active = True)
    
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = EventSerializer(event)
        return Response(serializer.data)
    
#   -- metodos de gerenciamento dos eventos propios --
    if request.user != event.owner:
            return Response(status=status.HTTP_403_FORBIDDEN)
    
    if request.method in ['PUT','PATCH']:
        aceita_parcial = (request.method == 'PATCH')
        serializer = EventSerializer(event, data = request.data, partial = aceita_parcial)
        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
  
        
    elif request.method == "DELETE":
        event.is_active = False
        event.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

        


    









