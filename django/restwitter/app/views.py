from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import TweetSerializer
from .models import Tweet

class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer


    # override 'author' with the current user
    def create(self, request, *args, **kwargs):
        print(timezone.now())
        request.data.update({'author': request.user.id})
        return super(TweetViewSet, self).create(request, *args, **kwargs)
    

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if (instance.author == request.user):
            request.data.update({'author': request.user.id})
            return super(TweetViewSet, self).update(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if (instance.author == request.user):
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

