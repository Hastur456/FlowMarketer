from fastapi import Request

from contextlib import asynccontextmanager
from fastapi import FastAPI
from elasticsearch.exceptions import TransportError
from app.elasticsearch.client import ElasticsearchClient, es_config


@asynccontextmanager
async def es_lifespan(app: FastAPI):
    es_client = ElasticsearchClient(config=es_config)

    try:
        await es_client.connect()
        app.state.es_client = es_client
    except TransportError as e:
        print("Elastic search exception: {}".format(e))
        raise

    try: 
        yield
    except Exception as e:
        raise e
    
    finally:
        try:
            await app.state.es_client.disconnect()
            print("Sessin is closed")
        except Exception as e:
            print("Elasticsearch error {}".format(e))



async def get_es_client(request: Request):
    return request.app.state.es_client
