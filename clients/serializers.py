from rest_framework import serializers
from .models import Comment, Clients, Proposal


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'comment', 'rating', 'client', 'approved', 'response']


class ClientsSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Clients
        fields = ['id', 'client_id', 'firstname', 'lastname', 'comment_set']


class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        fields = ['id', 'proposal']
