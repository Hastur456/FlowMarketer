from fastapi import Request


from contextlib import asynccontextmanager
from fastapi import FastAPI
from elasticsearch.exceptions import TransportError
from app.elasticsearch.client import ESClient


@asynccontextmanager
async def es_lifespan(app: FastAPI):
    try:
        client = await ESClient().get_client()
        app.state.es_client = client
        info = await app.state.es_client.info()
        es_version = info.get('version', {}).get('number', 'unknown')
        print(f"✅ [Elasticsearch] Connected (v{es_version})")
    except TransportError as e:
        print("Elastic search exception: {}".format(e))
        raise

    try: 
        yield
    except Exception as e:
        raise e
    
    finally:
        try:
            await app.state.es_client.close()
            print("Sessin is closed")
        except Exception as e:
            print("Elasticsearch error {}".format(e))



async def get_es_client(request: Request):
    return request.app.state.es_client
