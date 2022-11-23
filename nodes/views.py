from django.shortcuts import render
from .models import Node
from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from authors.serializers import AuthorSerializer


class NodeAPIView(GenericAPIView):
    def get_serializer_class(self):
        return NodeSerializer

    def get(self, request):
        """
        Get all nodes
        """
        nodes = self.get_queryset()
        serializer = ReadNodeSerializer(nodes, many=True)
        return Response({"nodes":serializer.data})
    def get_queryset(self):
        return Node.objects.all()
    
    


class NodeSerializer(serializers.ModelSerializer):
    api_url = serializers.URLField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def create(self, validated_data):
        node = Node.objects.create(**validated_data)
        return node

    class Meta:
        model = Node
        fields = ("api_url", "username", "password")


class ReadNodeSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(required=True)
    api_url = serializers.URLField(required=True)
    username = serializers.CharField(required=True)
    proxy_users = serializers.SerializerMethodField("get_proxy_users")
    team_account = serializers.SerializerMethodField("get_team_account")

    def get_proxy_users(self, obj):
        return AuthorSerializer(obj.proxy_users.all(), many=True).data
    
    def get_team_account(self, obj):
        return AuthorSerializer(obj.team_account).data

    class Meta:
        model = Node
        fields = ("api_url", "username", "proxy_users","team_account","nickname")
