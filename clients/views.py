from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CommentSerializer, ClientsSerializer, ProposalSerializer
from .models import Comment, Clients
from django.conf import settings


class CommentList(APIView):
    """
    List all comments, or create a new snippet.
    """
    def get(self, request, api_token):
        if api_token != settings.API_TOKEN:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        comments_qs = Comment.objects.all()
        params = request.query_params.dict()
        client_qs = Clients.objects.all()

        if 'client_id' in params:
            client_qs = client_qs.filter(client_id=params['client_id'])
            try:
                client = client_qs.get()
                comments_qs = comments_qs.filter(client=client)
            except Clients.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = CommentSerializer(comments_qs, many=True)
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
