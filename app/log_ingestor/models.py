from django.db import models
from django.contrib.postgres.fields import DateTimeRangeField
from django.contrib.postgres.search import SearchVector, SearchVectorField
from django.contrib.postgres.indexes import SpGistIndex
from psycopg2.extras import DateTimeTZRange


class LogLevel(models.Model):
    level = models.CharField(unique=True)

    class Meta:
        db_table = "log_levels"
        indexes = [
            models.Index(fields=["level"]),
        ]

    def __str__(self):
        return self.level


class LogResource(models.Model):
    resource = models.CharField(unique=True)

    class Meta:
        db_table = "log_resources"
        indexes = [
            models.Index(fields=["resource"]),
        ]

    def __str__(self):
        return self.resource

class Log(models.Model):
    level = models.ForeignKey(LogLevel, on_delete=models.PROTECT)
    message = models.TextField()
    resourceId = models.ForeignKey(LogResource, on_delete=models.PROTECT)
    timestamp = models.DateTimeField()
    traceId = models.CharField()
    spanId = models.CharField()
    commit = models.CharField()
    metadata = models.JSONField()
    parentResourceId = models.CharField(blank=True, null=True)

    class Meta:
        db_table = "logs"
        indexes = [
            models.Index(fields=["timestamp"]),
            models.Index(fields=["level"]),
            models.Index(fields=["resourceId"]),
            models.Index(fields=["traceId"]),
            models.Index(fields=["spanId"]),
            models.Index(fields=["commit"]),
            models.Index(fields=["parentResourceId"]),
        ]

    def __str__(self):
        return f"{self.level}: {self.message}"
