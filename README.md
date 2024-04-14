# Log Ingestor and Query Interface


# Table of Contents

1. [Challenge](./README.md)
2. [Requirements and Getting Started](./doc/README.md#requirements-and-getting-started)
3. [Usage](./doc/README.md#usage)
4. [Architecture](./doc/README.md#architecture)
5. [Stress tests](./doc/README.md#stress-tests)



## Introduction

This project aims to create a robust log ingestor system and a query interface capable of handling vast volumes of log data efficiently. It allows querying through a simple interface using full-text search or specific field filters.

### Objective

Develop a log ingestor system and query interface utilizing any programming language to meet the specified requirements.

### Sample Log Data Format

The logs to be ingested will follow this JSON format:

```json
{
	"level": "error",
	"message": "Failed to connect to DB",
    "resourceId": "server-1234",
	"timestamp": "2023-09-15T08:00:00Z",
	"traceId": "abc-xyz-123",
    "spanId": "span-456",
    "commit": "5e5342f",
    "metadata": {
        "parentResourceId": "server-0987"
    }
}
```

## Requirements

### Log Ingestor:

- **Ingestion Mechanism:** Develop a mechanism to ingest logs in the provided format.
- **Scalability:** Ensure scalability to handle high volumes of logs efficiently.
- **Bottleneck Mitigation:** Mitigate potential bottlenecks such as I/O operations, database write speeds, etc.
- **HTTP Server:** Logs should be ingested via an HTTP server, default port `3000`.

### Query Interface:

- **User Interface:** Offer a user interface (Web UI or CLI) for full-text search across logs.
- **Filters:** Include filters based on various log attributes (level, message, resourceId, timestamp, etc.).
- **Efficiency:** Aim for efficient and quick search results.

### Advanced Features (Bonus):

- Implement search within specific date ranges.
- Utilize regular expressions for search.
- Allow combining multiple filters.
- Provide real-time log ingestion and searching capabilities.
- Implement role-based access to the query interface.

## Sample Queries

Sample queries that will be executed for validation:

- Find all logs with the level set to "error".
- Search for logs with the message containing the term "Failed to connect".
- Retrieve all logs related to resourceId "server-1234".
- Filter logs between the timestamp "2023-09-10T00:00:00Z" and "2023-09-15T23:59:59Z". (Bonus)

## Evaluation Criteria

Your submission will be evaluated based on:

- Volume handling
- Speed in returning search results
- Scalability to increasing volumes of logs/queries
- Usability and user-friendliness
- Implementation of advanced features
- Cleanliness and structure of the codebase
