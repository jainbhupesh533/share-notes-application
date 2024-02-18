from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Note, SharedNote, NoteHistory
from .serializers import NoteSerializer, SharedNoteSerializer, NoteHistorySerializer, UserSerializer


class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateNoteView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetOrUpdateNoteView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        note = get_object_or_404(Note, id=id)
        if request.user == note.owner or SharedNote.objects.filter(note=note, shared_user=request.user).exists():
            serializer = NoteSerializer(note)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Access denied"}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, id):
        note = get_object_or_404(Note, id=id)
        # Check if the user has permission to edit the note
        if request.user == note.owner or SharedNote.objects.filter(note=note, shared_user=request.user, can_edit=True).exists():
            # Save the original note content
            original_content = note.content

            # Update the note content with the new data
            new_content = request.data.get('content', '')
            note.content += "\n" + new_content

            try:
                # Use transaction.atomic() to ensure atomicity of database operations
                with transaction.atomic():
                    # Save the updated note and create a note history entry within the same transaction
                    note.save()
                    NoteHistory.objects.create(note=note, user=request.user, original_content=original_content,
                                               updated_content=note.content)
                    serializer = NoteSerializer(note).data
                return Response(serializer, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({f"An error occurred while updating the note: {e}"},
                                status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response("You don't have permission to edit this note", status=status.HTTP_403_FORBIDDEN)


class ShareNoteView(APIView):
    def post(self, request):
        # Get the note ID from the request data
        note_id = request.data.get('note_id')

        # Ensure the note exists
        note = get_object_or_404(Note, id=note_id)

        # Get the list of user IDs to share the note with
        user_ids = request.data.get('user_ids', [])

        # Share the note with each user
        for user_id in user_ids:
            shared_note_data = {'note': note_id, 'shared_user': user_id, 'can_edit': True}
            shared_note_serializer = SharedNoteSerializer(data=shared_note_data)
            if shared_note_serializer.is_valid():
                shared_note_serializer.save()
            else:
                return Response(shared_note_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Return success response
        return Response({"message":"Note shared successfully"}, status=status.HTTP_201_CREATED)


class NoteVersionHistoryView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        note = get_object_or_404(Note, id=id)
        if request.user == note.owner or SharedNote.objects.filter(note=note, shared_user=request.user).exists():
            history = NoteHistory.objects.filter(note=note).order_by('-timestamp')
            serializer = NoteHistorySerializer(history, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"errors":"Access denied"}, status=status.HTTP_403_FORBIDDEN)