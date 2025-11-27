from os import getenv
from typing import Optional

from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader

API_KEY = getenv("API_KEY")
API_KEY_HEADER = APIKeyHeader(
    name="x-api-key",
    auto_error=False,
    description="API Key required for authentication",
)


async def verify_api_key(api_key: Optional[str] = Security(API_KEY_HEADER)) -> None:
    """
    Verify the API key provided in the request header for authentication.
    """
    print(f"verify_api_key started: {api_key}")
    if not API_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API key not configured on server",
        )

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required. Include 'x-api-key' header.",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    return api_key
