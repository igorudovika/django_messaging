from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Messages
from .serializers import MessagesBoxSerializer, UsersSerializer


class HomeTemplateView(TemplateView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/login/')
        return super(HomeTemplateView, self).get(request, *args, **kwargs)


@login_required
@api_view(['GET'])
def inbox(request):
    messages = Messages.objects.filter(recipient=request.user)
    serializer = MessagesBoxSerializer(messages, many=True)
    return Response(serializer.data)


@login_required
@api_view(['GET', 'POST'])
def sent(request):
    if request.method == 'POST':
        # request.data._mutable = True
        request.data['sender'] = request.user.id
        serializer = MessagesBoxSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)
    else:
        messages = Messages.objects.filter(sender=request.user)
        serializer = MessagesBoxSerializer(messages, many=True)
        return Response(serializer.data)


@login_required
@api_view(['GET', 'PUT', 'DELETE'])
def message(request, pk):
    try:
        message_object = Messages.objects.get(id=pk)
    except Messages.DoesNotExist:
        return Response({'error': 'Message does not exists'}, status=404)
    if request.method == 'PUT':
        serializer = MessagesBoxSerializer(instance=message_object, data=request.data, partial=True, many=False)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if request.user.id == message_object.sender.id or request.user.id == message_object.recipient.id:
            message_object.delete()
            return Response('Deleted {} board'.format(message_object.title))
        else:
            return Response({'error': 'Only sender or recipient can delete board'}, status=401)
    else:
        serializer = MessagesBoxSerializer(instance=message_object)
        return Response(serializer.data)


@login_required
@api_view(['GET'])
def users(request):
    messages = User.objects.all()
    serializer = UsersSerializer(messages, many=True)
    return Response(serializer.data)
