from nylas import Client

from .config import settings

nylas_client = Client(
    api_key=settings.nylas_api_key, api_uri=settings.nylas_api_region_uri
)
