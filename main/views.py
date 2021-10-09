from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Message
import json
# Create your views here.

def validate_new_message(mes):
    if 'sender_id' not in mes or 'reciver_id' not in mes or mes['sender_id'] == mes['reciver_id'] or type(mes['sender_id']) is not int or type(mes['reciver_id']) is not int:
        return {'False': "Sender and receiver can't be the same and must have an integer value"}
    if 'subject' not in mes or 'message_text' not in mes or type(mes['subject']) is not str or type(mes['message_text']) is not str or len(mes['subject'])<1 or len(mes['message_text'])<1:
        return {'False': "subject and reciver_id are required and must be strings"}
    return {'True': 'Input is valid'}

@csrf_exempt
def write(response):
    if response.method == 'POST':
        data = json.loads(response.body)
        validation = validate_new_message(data)
        if 'False' in validation:
            return JsonResponse({'Error': validation['False']})
        mes = Message(sender_id=data['sender_id'], reciver_id=data['reciver_id'], subject=data['subject'], message_text=data['message_text'])
        mes.save()
        obj = model_to_dict(Message.objects.latest('message_id'))
        return JsonResponse(obj)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all(response):
    id = response.user.id
    try:
        mes_set = Message.objects.all().filter(reciver_id=id)
        if not mes_set:
            raise Exception
        for mes in mes_set:
            mes.is_read = True
            mes.save()
        mes_json = serializers.serialize("json", mes_set)
        return JsonResponse(json.loads(mes_json), safe=False)
    except:
        return JsonResponse({'log': 'No messages found for receiver ' + str(id)})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_unread(response):
    id = response.user.id
    try:
        mes_set = Message.objects.all().filter(reciver_id=id, is_read=False)
        if not mes_set:
            raise Exception
        for mes in mes_set:
            mes.is_read = True
            mes.save()
        mes_json = serializers.serialize("json", mes_set)
        return JsonResponse(json.loads(mes_json), safe=False)
    except:
        return JsonResponse({'log': 'No unread messages found for receiver ' + str(id)})

@api_view(['GET'])
@permission_classes([IsAuthenticated])    
def get_message(response, mes_id):
    id = response.user.id
    try:
        mes = Message.objects.get(message_id=mes_id, reciver_id=id)
        mes.is_read = True
        mes.save()
        obj = model_to_dict(mes)
        return JsonResponse(obj)
    except:
        return JsonResponse({'log': 'Message ' + str(mes_id) + ' was not found'})

@csrf_exempt
def delete_message(response, id):
    try:
        mes = Message.objects.get(message_id=id)
        mes.delete()
        return JsonResponse({'log': 'Message ' + str(id) + ' deleted'})
    except:
        return JsonResponse({'log': 'Message ' + str(id) + ' was not found'})