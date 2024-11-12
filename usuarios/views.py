from django.contrib.auth.hashers import make_password, check_password
from .models import Usuarios
from .serializers import UsuariosSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def usuario_manager(request, pk=None):
    """
    CRUD baseado na existencia de uma PK
    Retorna STATUS HTTP_404_NOT_FOUND: caso usuario não encontrado
    Retorna STATUS HTTP_400_BAD_REQUEST: caso houver erros na requisição
    """
    if pk != None and request.method in ['GET', 'PUT', 'DELETE']:
        try:
            usuario = Usuarios.objects.get(pk=pk)
        except Usuarios.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if request.method == 'GET':
            """Retorna os dados serializados do usuario correspondente a PK recebida e um status HTTP_200_OK"""
            serializer = UsuariosSerializer(usuario)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PUT':
            """
            Atualiza todos os dados do usuario correspondente a PK recebida
            Retorna os dados serializados e um status HTTP_202_ACCEPTED
            Retorna os erros e status HTTP_400_BAD_REQUEST caso houver erros de validação
            """
            data_original = usuario.__dict__
            senha_usuario = usuario.password
            data_original.update(request.data)
            print(request.data['password'], senha_usuario)
            if not check_password(request.data['password'], senha_usuario) and request.data['password'] != senha_usuario:
                data_original['password'] = make_password(request.data['password'])
            else:
                data_original['password'] = senha_usuario
            serializer = UsuariosSerializer(usuario, data=data_original)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            """
            Deleta o usuario correspondente a PK recebida
            Retorna um status HTTP_204_NO_CONTENT
            """
            usuario.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    elif not pk:
        if request.method == 'GET':
            """Retorna os dados de todos os usuarios cadastrados e um status HTTP_200_OK"""
            serializer = UsuariosSerializer(Usuarios.objects.all(), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'POST':
            """Retorna os dados serializados do usuario criado e um status HTTP_201_CREATED"""
            novo_usuario = request.data
            novo_usuario['password'] = make_password(novo_usuario['password'])
            serializer = UsuariosSerializer(data=novo_usuario)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)