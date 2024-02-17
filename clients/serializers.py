from rest_framework import serializers
from .models import Comment, Clients, Proposal


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'comment', 'rating', 'client', 'location', 'approved', 'response']


class ClientsSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Clients
        fields = [
            'id', 'client_id', 'firstname', 'lastname', 'registration_token', 'do_not_send_push_bonus', 'comment_set']


class CommentSerializerDepth1(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'comment', 'rating', 'approved', 'response', 'client', 'location']
        depth = 1


class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        fields = ['id', 'proposal']
