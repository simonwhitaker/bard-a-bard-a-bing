# Bard-a-Bing!

A search engine for Shakespeare sonnets, powered by [Meilisearch](https://www.meilisearch.com/).

## Getting started

1. Generate a local JSON document containing the Shakespeare sonnets as per-line data elements:

    ```command
    curl -s https://ocw.mit.edu/ans7870/6/6.006/s08/lecturenotes/files/t8.shakespeare.txt \
        | ./pre-process.py > sonnets.json
    ```

2. Run a Meilisearch instance locally using docker compose:

    ```command
    docker compose up -d
    ```

3. Load the documents into your search index:

    ```command
    curl \
        -X POST 'http://localhost:7700/indexes/sonnets/documents?primaryKey=id' \
        -H 'Content-Type: application/json' \
        --data-binary @sonnets.json
    ```

4. Open http://localhost:7700 and search! Or query using cURL or (my favourite) [HTTPie](https://httpie.io/), like this:

    ```command
    http --body localhost:7700/indexes/sonnets/search q=compare+thee limit:=1
    ```

    Which returns:

    ```json
    {
        "estimatedTotalHits": 1,
        "hits": [
            {
                "id": 239,
                "line_number": 1,
                "sonnet_number": 18,
                "text": "Shall I compare thee to a summer's day?"
            }
        ],
        "limit": 1,
        "offset": 0,
        "processingTimeMs": 0,
        "query": "compare+thee"
    }
    ```
