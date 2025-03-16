from django.shortcuts import render
from django.shortcuts import get_object_or_404,redirect
from .models import ChatRoom,Message
from store.models import product as Product
from account.models import registration
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
# Create your views here.

@login_required(login_url='login')
def chat_with_seller(request,product_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    product = get_object_or_404(Product,id=product_id)
    seller = product.seller

    chat_room,created = ChatRoom.objects.get_or_create(buyer=request.user,seller=seller,product=product)

    return redirect('chat_room',room_id=chat_room.id)

@login_required(login_url='login')
def chat_room(request,room_id):
    chat_room = get_object_or_404(ChatRoom,id=room_id)

    if request.method == "POST":
        content = request.POST['content']
        Message.objects.create(room=chat_room,sender=request.user,content=content)

    messages = chat_room.messages.all().order_by('timestamp')

    context = {
        'chat_room':chat_room,
        'messages':messages,
    }

    return render(request,'chats/chat_room.html',context)

@login_required(login_url='login')
def chat_list(request):
    registration_user = request.user

    chat_rooms = []

    if registration_user:
        chat_rooms = ChatRoom.objects.filter(Q(buyer=registration_user) | Q(seller=registration_user)).order_by('-created_at')
    return render(request,'chats/chat_list.html',{'chat_rooms':chat_rooms})

def get_messages(request,room_id):
    chat_room = get_object_or_404(ChatRoom,id=room_id)
    messages = chat_room.messages.all().order_by('timestamp')
    data = []
    for msg in messages:
        data.append({
            'sender':msg.sender.username,
            'content':msg.content,
            'timestamp':msg.timestamp.strftime("%b %d, %Y %H:%M")
        })
    return JsonResponse({'messages':data})