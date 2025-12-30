# import pytest
# from app.elasticsearch.indexers.product_indexer import ProductIndexer
# from app.elasticsearch.searchers.product_searcher import ProductSearcher
# from tests.elasticsearch.utils.test_index_config import logger


# @pytest.mark.integration
# async def test_full_search_flow(es_client):
#     indexer = ProductIndexer(es_client, logger)
#     searcher = ProductSearcher(es_client, logger)

#     await indexer.create_index()
#     await indexer.index_one(product)
#     await indexer.refresh()

#     results = await searcher.search_by_text("iphone")
#     assert len(results) == 1
