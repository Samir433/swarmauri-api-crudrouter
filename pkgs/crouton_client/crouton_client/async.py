import aiohttp
import logging
from urllib.parse import urlencode
from typing import Optional, Any, Dict
from .UUID import UUIDGenerator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AsyncCroutonClient:
    def __init__(self, API_ROOT: str, ACCESS_STRING: Optional[str] = None):
        self.API_ROOT = API_ROOT.rstrip('/')  # Ensure no trailing slash
        self.ACCESS_STRING = ACCESS_STRING

    async def _build_url(self, resource: str, item_id: Optional[str] = None, query_params: Optional[Dict[str, Any]] = None) -> str:
        """
        Helper method to construct the URL with resource, item_id, and query parameters.
        """
        url = f"{self.API_ROOT}/{resource.strip('/')}"
        
        # Add item ID if provided
        if item_id:
            url += f"/{item_id}"

        # Add query parameters
        if query_params:
            query_string = urlencode(query_params)
            url += f"?{query_string}"

        # Add access string as a query parameter
        if self.ACCESS_STRING:
            separator = '&' if '?' in url else '?'
            url += f"{separator}token={self.ACCESS_STRING.strip('?')}"

        return url

    async def get(
        self, 
        resource: str, 
        item_id: Optional[str] = None, 
        filter_key: Optional[str] = None, 
        filter_value: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Perform an asynchronous GET request with optional filters and an item ID.
        """
        query_params = {filter_key: filter_value} if filter_key and filter_value else None
        url = await self._build_url(resource, item_id, query_params)

        logger.info(f"Performing GET request to {url}")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as res:
                if res.status == 200:
                    return await res.json()
                else:
                    error_content = await res.text()
                    logger.error(f"GET request failed with status {res.status}: {error_content}")
                    raise ValueError(f"GET request failed with status {res.status}: {error_content}")

    async def post(self, resource: str, data_obj: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform an asynchronous POST request to create a resource.
        """
        if 'id' not in data_obj:
            data_obj['id'] = UUIDGenerator().create()

        url = await self._build_url(resource)

        logger.info(f"Performing POST request to {url} with data {data_obj}")
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data_obj) as res:
                if res.status == 200:
                    return await res.json()
                else:
                    error_content = await res.text()
                    logger.error(f"POST request failed with status {res.status}: {error_content}")
                    raise ValueError(f"POST request failed with status {res.status}: {error_content}")

    async def put(self, resource: str, data_obj: Dict[str, Any], item_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Perform an asynchronous PUT request to update a resource.
        """
        url = await self._build_url(resource, item_id)

        logger.info(f"Performing PUT request to {url} with data {data_obj}")
        async with aiohttp.ClientSession() as session:
            async with session.put(url, json=data_obj) as res:
                if res.status == 200:
                    return await res.json()
                else:
                    error_content = await res.text()
                    logger.error(f"PUT request failed with status {res.status}: {error_content}")
                    raise ValueError(f"PUT request failed with status {res.status}: {error_content}")

    async def delete(self, resource: str, item_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Perform an asynchronous DELETE request to delete a resource.
        """
        url = await self._build_url(resource, item_id)

        logger.info(f"Performing DELETE request to {url}")
        async with aiohttp.ClientSession() as session:
            async with session.delete(url) as res:
                if res.status == 200:
                    return await res.json()
                else:
                    error_content = await res.text()
                    logger.error(f"DELETE request failed with status {res.status}: {error_content}")
                    raise ValueError(f"DELETE request failed with status {res.status}: {error_content}")
