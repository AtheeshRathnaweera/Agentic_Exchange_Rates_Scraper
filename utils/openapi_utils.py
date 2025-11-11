from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI


def build_openapi(
    app: FastAPI, allowed_prefixes: list[str] | str | None = None
) -> None:
    """
    Customize the OpenAPI schema to include only selected route prefixes.

    Args:
        app (FastAPI): The FastAPI application.
        allowed_prefixes (list[str]): List of allowed route prefixes (e.g. ['/exchange-rates']).
    """

    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema

        # Build the full OpenAPI schema (unfiltered)
        full_schema = get_openapi(
            title=app.title or "API",
            version=app.version or "0.0.0",
            description=app.description or "",
            routes=app.routes,
        )

        # If wildcard or None -> keep everything
        if allowed_prefixes in (None, "*"):
            app.openapi_schema = full_schema
            return app.openapi_schema

        # Normalize prefixes to a list of strings
        if isinstance(allowed_prefixes, str):
            prefixes = [allowed_prefixes]
        else:
            prefixes = list(allowed_prefixes)

        # Filter paths keys (they look like "/exchange-rates/..." etc.)
        filtered_paths = {
            path: value
            for path, value in full_schema.get("paths", {}).items()
            if any(path.startswith(prefix) for prefix in prefixes)
        }

        # Rebuild schema with filtered paths
        filtered_schema = dict(full_schema)  # shallow copy
        filtered_schema["paths"] = filtered_paths

        app.openapi_schema = filtered_schema
        return app.openapi_schema

    app.openapi = custom_openapi
