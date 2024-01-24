from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CommentSerializer, ClientsSerializer, ProposalSerializer, CommentSerializerDepth1
from .models import Comment, Clients
from django.conf import settings
from app_settings.poster import Poster


class CommentList(APIView):
    """
    List all approved comments, or create a new one.
    """

    def get(self, request, api_token):
        if api_token != settings.API_TOKEN:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        params = request.query_params.dict()
        comments_qs = Comment.objects.all().select_related('client')
        if 'approved' in params:
            comments_qs = comments_qs.filter(approved=params['approved'])

        client_qs = Clients.objects.all()

        if 'client_id' in params:
            client_qs = client_qs.filter(client_id=params['client_id'])
            try:
                client = client_qs.get()
                comments_qs = comments_qs.filter(client=client)
            except Clients.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = CommentSerializerDepth1(comments_qs, many=True)
        return Response(serializer.data)

    def post(self, request, api_token):
        if api_token != settings.API_TOKEN:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientDetail(APIView):
    """
    Get client by id and show his comments.
    """

    def get(self, request, api_token):
        if api_token != settings.API_TOKEN:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        params = request.query_params.dict()

        if 'client_id' in params:
            qs = Clients.objects.filter(client_id=params['client_id'])
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            client = qs.prefetch_related('comment_set').get()
        except Clients.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = ClientsSerializer(client)

        return Response(serializer.data)


class Proposals(APIView):
    """
    Create a new Proposal.
    """

    def post(self, request, api_token):
        if api_token != settings.API_TOKEN:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = ProposalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateRegistrationToken(APIView):
    """
    Update registration token for a user for push notifications
    """

    def post(self, request, api_token):
        if api_token != settings.API_TOKEN:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        params = request.POST.dict()
        if 'client_id' not in params or 'registration_token' not in params or not params['registration_token']:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            client = Clients.objects.get(client_id=params['client_id'])
            client.save(registration_token=params['registration_token'])
        except Clients.DoesNotExist:
            # If client does not exist request client in Poster and save it with registration token
            response = Poster().get(url='/api/clients.getClient', params={'client_id': params['client_id']})
            if 'error' in response:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            client_data = {
                'client_id': response['client_id'],
                'firstname': response['firstname'],
                'lastname': response['lastname'],
                'registration_token': params['registration_token'],
            }
            Clients.objects.create(**client_data)

        return Response(status=status.HTTP_200_OK)
