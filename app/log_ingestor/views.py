from django.db import connection
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.db import close_old_connections, transaction
from .models import Log, LogResource, LogLevel
import django_rq
from .serializers import LogSerializer
from .helper import dictfetchall


q = django_rq.get_queue("logs")

def ingest_log(logs):
    close_old_connections()
    logs.save()


@api_view(['POST']) 
def process_log(request): 
    """ 
    Ingest the log, add it to the queue for processing
    """
    # Not sure if we will get only log dictionary or a list of logs
    # handling the senario just in case we get a list
    many_logs = isinstance(request.data, list)
    
    logs = LogSerializer(data=request.data, many=many_logs)

    if logs.is_valid():
        q.enqueue(ingest_log, logs)
        return Response({"message": "logs enqueued for ingestion"}, status=status.HTTP_200_OK)

    return Response(logs.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET']) 
def get_log_levels(request): 
    levels = list(LogLevel.objects.values())
    return Response(levels)


@api_view(['GET']) 
def get_resources(request): 
    resources = list(LogResource.objects.values())
    return Response(resources)

@api_view(['GET']) 
def get_init_filter_data(request):
    levels = list(LogLevel.objects.values())
    resources = list(LogResource.objects.values())

    return Response({
        "levels": levels,
        "resources": resources
    })


@api_view(['POST']) 
def fetch_logs(request):
    rules = request.data["rules"]
    page = request.data.get("page")

    if not page or not isinstance(page, int) or page <= 0:
        return Response({"message": "page value is not valid"}, status=status.HTTP_400_BAD_REQUEST)

    # Supporting only 1 rule for now
    if len(rules) < 1 or len(rules) > 1:
        return Response({"message": "Supporting 1 rule only"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        rule = rules[0]
        query = '''
            select lgs.message, lgs.\"spanId\", lgs.\"commit\",
                lgs.\"traceId\", lgs.\"timestamp\", lgs.metadata, 
                lls.level as level, lrs.resource as \"resourceId\" 
            from logs lgs
            inner join log_levels lls on lgs.level_id = lls.id
            inner join log_resources lrs on lgs."resourceId_id" = lrs.id where
        '''

        DATA_PER_PAGE = 50
        field = rule["field"]
        value = rule["value"]
        # depending on field generate the where clause for the query
        # TODO: make it better, some sort of configuration dict
        params = [value]
        # ordering by timestamp to get the latest logs at top
        order_by = " order by lgs.\"timestamp\" desc "

        pagination = """
        offset %s
        limit %s
        """
        if field == "message":
            where_condition = "lgs.search_vector @@ plainto_tsquery('english', %s) "
            # Removing order by in searching as it slows down query a lot
            order_by = ""
        elif field == "timestamp":
            start_time = value.split(",")[0]
            end_time = value.split(",")[1]
            where_condition = "lgs.\"timestamp\" between %s and %s "
            params = [start_time, end_time]
        elif field == "level":
            where_condition = f"lls.\"{field}\" = %s"
        elif field == "resource":
            where_condition = f"lrs.\"{field}\" = %s"
        else:
            where_condition = f"lgs.\"{field}\" = %s"


        params.append(DATA_PER_PAGE * (page - 1))
        params.append(DATA_PER_PAGE * page)
        with connection.cursor() as cursor:
            query = query + where_condition + order_by + pagination
            cursor.execute(query, params)
            data = dictfetchall(cursor)

        return Response(data)
    except Exception as e:
        return Response({"message": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)