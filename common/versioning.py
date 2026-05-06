SUPPORTED_API_VERSIONS = {1, 2}
DEFAULT_API_VERSION = 2


def get_api_version(request) -> int:
    """Return mobile API version from X-API-Version or build-version headers."""
    raw_version = (
        request.headers.get("X-API-Version")
        or request.headers.get("Build-Version")
        or request.headers.get("X-Build-Version")
    )
    if not raw_version:
        return DEFAULT_API_VERSION
    try:
        version = int(raw_version)
    except (TypeError, ValueError):
        return DEFAULT_API_VERSION
    return version if version in SUPPORTED_API_VERSIONS else DEFAULT_API_VERSION
