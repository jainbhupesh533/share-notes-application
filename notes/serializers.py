from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Note, SharedNote, NoteHistory


class NoteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Note
        fields = ['id', 'owner', 'content', 'created_at', 'last_updated_at']


class SharedNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedNote
        fields = '__all__'


class NoteHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteHistory
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user