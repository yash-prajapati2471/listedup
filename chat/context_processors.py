from .models import ChatRoom
from django.db.models import Q

def chat_count(request):
    if request.user.is_authenticated:
        count = ChatRoom.objects.filter(Q(buyer=request.user) | Q(seller=request.user)).count()
    else:
        count = 0
    return {'chat_count':count}