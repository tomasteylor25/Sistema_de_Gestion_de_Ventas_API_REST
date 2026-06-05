"""Vistas de autenticación JWT"""

import logging
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from drf_spectacular.utils import extend_schema, OpenApiExample
from config.responses import respuesta_exitosa, respuesta_creada, respuesta_error
from .serializers import RegistroSerializer, LoginSerializer, PerfilSerializer

logger = logging.getLogger('api')


class RegistroView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=['Autenticación'],
        summary='Registrar nuevo usuario',
        request=RegistroSerializer,
    )
    def post(self, request):
        serializer = RegistroSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            logger.info(f'REGISTRO | usuario={user.username}')
            return respuesta_creada({
                'usuario': {
                    'id':       user.id,
                    'username': user.username,
                    'email':    user.email,
                },
                'tokens': {
                    'refresh': str(refresh),
                    'access':  str(refresh.access_token),
                }
            }, 'Usuario registrado exitosamente')
        return respuesta_error(errores=serializer.errors)


class LoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=['Autenticación'],
        summary='Iniciar sesión',
        request=LoginSerializer,
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            logger.info(f'LOGIN | usuario={user.username}')
            return respuesta_exitosa({
                'usuario': {
                    'id':       user.id,
                    'username': user.username,
                    'email':    user.email,
                    'es_admin': user.is_staff,
                },
                'tokens': {
                    'refresh': str(refresh),
                    'access':  str(refresh.access_token),
                }
            }, 'Login exitoso')
        return respuesta_error(errores=serializer.errors)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=['Autenticación'], summary='Cerrar sesión')
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info(f'LOGOUT | usuario={request.user.username}')
            return respuesta_exitosa(mensaje='Sesión cerrada correctamente')
        except TokenError:
            return respuesta_error('Token inválido o ya expirado')


class PerfilView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=['Autenticación'], summary='Ver perfil del usuario autenticado')
    def get(self, request):
        serializer = PerfilSerializer(request.user)
        return respuesta_exitosa(serializer.data)
