from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate
from .models import Usuarios
from .serializers import UsuariosSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import TokenProxy
from rest_framework import status

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def usuarios_manager(request):
    if request.method == 'GET':
        """
        Retorna os dados serializados de todos os usuarios
        GET parametros
            cargo = "M" ou "A"
        Return
            Response: 200
                Json com dados serializados dos usuarios
        """
        usuarios = Usuarios.objects.all()
        if not usuarios.exists():
            return Response(status=status.HTTP_204_NO_CONTENT)
        try:
            serializer = UsuariosSerializer(usuarios.filter(cargo=request.GET['cargo'].upper()), many=True)
        except:
            serializer = UsuariosSerializer(usuarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        """
        Retorna os dados serializados do usuario criado
        Return
            Response: 201
            Response: 400
                {'erros': 'xxxxxxxx'}
        """
        try:
            novo_usuario = request.data
            if 'cargo' in novo_usuario.keys():
                novo_usuario['cargo'] = novo_usuario['cargo'].upper()
            novo_usuario['password'] = make_password(novo_usuario['password'])
            serializer = UsuariosSerializer(data=novo_usuario)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
        except:
            pass
    return Response(status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def usuario_manager(request, pk):
    """CRUD baseado na existencia de uma PK"""
    try:
        usuario = Usuarios.objects.get(pk=pk)
    except Usuarios.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        """
        Retorna os dados serializados do usuario correspondente a PK
        Return
            Response: 200
                Json com dados serializados do usuario
            Response: 204
        """
        serializer = UsuariosSerializer(usuario)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'PUT':
        """
        Atualiza todos os dados do usuario correspondente a PK recebida
        Return
            Response: 202
            Response: 400
                {'erro': 'erros de validação'}
        """
        data_original = usuario.__dict__
        senha_usuario = usuario.password
        data_original.update(request.data)
        if not check_password(request.data['password'], senha_usuario) and request.data['password'] != senha_usuario:
            data_original['password'] = make_password(request.data['password'])
        else:
            data_original['password'] = senha_usuario
        serializer = UsuariosSerializer(usuario, data=data_original)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response({'erros': 'Erros de validação'}, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        """
        Deleta o usuario correspondente a PK recebida
        Return
            Response: 204
        """
        usuario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def token(request):
    """
    Recebe o usuario e senha e, caso válidos, retorna o token do usuario
    Return
        Response: 200
            {"token": "xxxxxxxxxxxxxxxxxx"}
        Response: 400:
            {"message": "usuario ou senha incorretos"}
    """
    usuario = request.data['username']
    senha = request.data['password']

    usuario = authenticate(request, username=usuario, password=senha)
    if usuario:
        return Response({'token': TokenProxy.objects.filter(user_id=usuario.pk).first().key}, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def token_validation(request):
    """
    Validação de token recebido
    Return
        Response: 200
        Response: 400
            {"error": "token inválido"}
    """
    token = request.data['token']
    if TokenProxy.objects.filter(key=token).exists():
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)