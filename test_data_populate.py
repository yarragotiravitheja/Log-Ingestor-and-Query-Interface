from faker import Faker
from locust import HttpUser, task
import random
import json
import uuid
from datetime import datetime, timezone

fake = Faker()

def generate_fake_log():
    log_level = random.choice(["info", "error", "warn", "debug", "trace", "critical"])
    message = fake.sentence()
    resource_id = "server-" + str(fake.random_int(min=1000, max=9999))
    timestamp = fake.date_time_this_decade().strftime("%Y-%m-%dT%H:%M:%SZ")
    trace_id = str(uuid.uuid4())
    span_id = "span-" + str(uuid.uuid4().hex)[:10]
    commit = str(uuid.uuid4().hex)[:7]
    parent_resource_id = "server-" + str(fake.random_int(min=1000, max=9999))

    log_data = {
        "level": log_level,
        "message": message,
        "resourceId": resource_id,
        "timestamp": timestamp,
        "traceId": trace_id,
        "spanId": span_id,
        "commit": commit,
        "metadata": {"parentResourceId": parent_resource_id},
    }

    return log_data


class LogStressTest(HttpUser):
    @task
    def ingest_logs(self):
        if random.randint(0, 1):
            fake_logs = [generate_fake_log() for _ in range(random.randint(2, 20))]
        else:
            fake_logs = generate_fake_log()

        self.client.post("/", json=fake_logs)
