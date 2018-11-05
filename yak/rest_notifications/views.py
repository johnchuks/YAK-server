from rest_framework import mixins, generics, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from pypushwoosh import client, constants
from pypushwoosh.command import RegisterDeviceCommand
from yak.rest_core.permissions import IsOwner
from yak.rest_notifications.models import NotificationSetting, Notification, create_notification, \
    PushwooshToken, NotificationType
from yak.rest_notifications.serializers import NotificationSettingSerializer, NotificationSerializer, \
    PushwooshTokenSerializer
from yak.rest_notifications.utils import register_device
from yak.rest_notifications.exceptions import DeviceRegistrationException
from yak.rest_social_network.views import CommentViewSet, FollowViewSet, ShareViewSet, LikeViewSet
from yak.settings import yak_settings


class PushwooshTokenView(generics.CreateAPIView):
    queryset = PushwooshToken.objects.all()
    serializer_class = PushwooshTokenSerializer
    permission_classes = (IsOwner,)

    def perform_create(self, serializer):
        token = serializer.validated_data['token']
        hwid = serializer.validated_data.pop("hwid")
        language = serializer.validated_data.pop("language")
        platform = serializer.validated_data.pop("platform")

        try:
            register_device(token, hwid, language, platform)
        except DeviceRegistrationException:
            raise AuthenticationFailed("Authentication with notification service failed")

        serializer.save(user=self.request.user)


class NotificationSettingViewSet(mixins.UpdateModelMixin,
                                 mixins.ListModelMixin,
                                 GenericViewSet):
    queryset = NotificationSetting.objects.all()
    serializer_class = NotificationSettingSerializer
    permission_classes = (IsOwner,)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def put(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, data=request.data, many=True, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class NotificationView(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = (IsOwner,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class NotificationCommentViewSet(CommentViewSet):
    def perform_create(self, serializer):
        obj = serializer.save(user=self.request.user)
        notification_type = NotificationType.objects.get(slug="comment")
        create_notification(obj.content_object.user, obj.user, obj.content_object, notification_type)


class NotificationFollowViewSet(FollowViewSet):
    def perform_create(self, serializer):
        obj = serializer.save(user=self.request.user)
        notification_type = NotificationType.objects.get(slug="follow")
        create_notification(obj.content_object, obj.user, obj.content_object, notification_type)


class NotificationShareViewSet(ShareViewSet):
    def perform_create(self, serializer):
        obj = serializer.save(user=self.request.user)
        notification_type = NotificationType.objects.get(slug="share")
        for receiver in obj.shared_with.all():
            create_notification(receiver, obj.user, obj.content_object, notification_type)


class NotificationLikeViewSet(LikeViewSet):
    def perform_create(self, serializer):
        obj = serializer.save(user=self.request.user)
        notification_type = NotificationType.objects.get(slug="like")
        create_notification(obj.content_object.user, obj.user, obj.content_object, notification_type)
