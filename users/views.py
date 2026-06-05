from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserProfileSerializer, UserRegistrationSerializer
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.permissions import IsAuthenticated, AllowAny


@api_view(['GET', 'PUT','DELETE', 'PATCH'])
def user_detail(request, username):

    try:
        user = User.objects.get(username=username) #procuro o usuario que tem esse username no db

    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND) #caso nao exista eu aviso para o front
    
    if request.method == 'GET':
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
    
    if request.user != user: # testo se o usuario que fez a requisicao eh o mesmo que buscamo no db
        return Response(status=status.HTTP_403_FORBIDDEN) 
    
   
  
    if request.method in ['PUT','PATCH']:

        aceita_parcial = (request.method == 'PATCH') #caso seja PATCH  defino nossa variavel que controla-ra se pode fazer alteracoes parciais

        serializer = UserProfileSerializer(user, data=request.data, partial = aceita_parcial) #jogo o dado do front para serializar
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
        
    elif request.method == 'DELETE':
        user.is_active = False
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([AllowAny])
def user_register(request):
    serializer = UserRegistrationSerializer(data=request.data) ##recebo os dados do front 
    serializer.is_valid(raise_exception=True)#checo se esta tudo nos conformes
    serializer.save()# salvo no banco de dados
    return Response(serializer.data, status=status.HTTP_201_CREATED)

    







        