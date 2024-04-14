from django.contrib import admin
import log_ingestor.models as models


admin.site.register(models.Log)
admin.site.register(models.LogLevel)
admin.site.register(models.LogResource)
