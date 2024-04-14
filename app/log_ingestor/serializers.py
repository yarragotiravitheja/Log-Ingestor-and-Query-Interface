from django.db import close_old_connections, transaction
from rest_framework import serializers
from log_ingestor.models import LogLevel, LogResource, Log


class LogLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogLevel
        fields = "__all__"


class LogResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogResource
        fields = "__all__"


class LogSerializer(serializers.ModelSerializer):
    level = serializers.CharField(source="level.level", allow_null=False)
    resourceId = serializers.CharField(source="resourceId.resource", allow_null=False)

    class Meta:
        model = Log
        fields = "__all__"

    def create(self, validated_data, **kwargs):
        with transaction.atomic():
            log_level = validated_data.pop("level")
            log_resource = validated_data.pop("resourceId")

            log_level, created = LogLevel.objects.get_or_create(level=log_level["level"])
            log_resource, created = LogResource.objects.get_or_create(resource=log_resource["resource"])

            parent_resource_id = validated_data.get("metadata", {}).get("parentResourceId")

            log = Log.objects.create(
                level=log_level,
                resourceId=log_resource,
                parentResourceId=parent_resource_id,
                **validated_data
            )

            return log