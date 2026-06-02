from __future__ import annotations

import json
import urllib.parse
import urllib.request
from typing import Any, Callable


REGISTRY_ALIASES = {
    "npm": "npmjs.org",
    "npmjs": "npmjs.org",
    "pypi": "pypi.org",
    "python": "pypi.org",
}


def discover_dependents(
    package: str,
    ecosystems: list[str],
    top: int = 40,
    seeds: list[dict[str, Any]] | None = None,
    mailto: str | None = None,
    fetcher: Callable[[str], Any] | None = None,
) -> dict[str, Any]:
    dependents = list(seeds or [])
    fetch = fetcher or _fetch_json
    for ecosystem in ecosystems:
        registry = REGISTRY_ALIASES.get(ecosystem, ecosystem)
        if registry in {"github", "gitlab", "manual", "seeds"}:
            continue
        url = _dependent_packages_url(registry, package, top, mailto)
        try:
            payload = fetch(url)
        except Exception as exc:  # Network discovery is best-effort; manual seeds remain canonical.
            dependents.append({"name": f"{registry}:{package}", "source": "ecosyste.ms", "status": "failed", "error": str(exc)})
            continue
        dependents.extend(_normalize_ecosystems_dependents(payload, registry))

    ranked = _rank_dependents(dependents)[:top]
    return {"schema_version": 1, "target": {"package": package, "ecosystems": ecosystems}, "dependents": ranked}


def parse_seed(seed: str) -> dict[str, Any]:
    if "=" in seed:
        name, path = seed.split("=", 1)
        return {"name": name, "path": path, "source": "manual"}
    return {"name": seed.rstrip("/").split("/")[-1], "path": seed, "source": "manual"}


def _dependent_packages_url(registry: str, package: str, top: int, mailto: str | None) -> str:
    encoded = urllib.parse.quote(package, safe="")
    query = {"per_page": str(top)}
    if mailto:
        query["mailto"] = mailto
    return f"https://packages.ecosyste.ms/api/v1/registries/{registry}/packages/{encoded}/dependent_packages?{urllib.parse.urlencode(query)}"


def _fetch_json(url: str) -> Any:
    request = urllib.request.Request(url, headers={"User-Agent": "hyrumguard/0.1"})
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def _normalize_ecosystems_dependents(payload: Any, registry: str) -> list[dict[str, Any]]:
    if isinstance(payload, dict):
        items = payload.get("dependent_packages") or payload.get("packages") or payload.get("data") or []
    else:
        items = payload
    normalized: list[dict[str, Any]] = []
    for item in items if isinstance(items, list) else []:
        if not isinstance(item, dict):
            continue
        name = item.get("name") or item.get("package_name") or item.get("full_name")
        repository_url = item.get("repository_url") or item.get("repository") or item.get("html_url")
        if not name:
            continue
        normalized.append(
            {
                "name": name,
                "repository_url": repository_url,
                "registry": registry,
                "source": "ecosyste.ms",
                "downloads": item.get("downloads") or item.get("downloads_count") or 0,
                "stars": item.get("stars") or item.get("stargazers_count") or 0,
            }
        )
    return normalized


def _rank_dependents(dependents: list[dict[str, Any]]) -> list[dict[str, Any]]:
    unique: dict[str, dict[str, Any]] = {}
    for item in dependents:
        name = item.get("name") or item.get("path") or item.get("repository_url")
        if not name:
            continue
        unique.setdefault(name, item)
    return sorted(
        unique.values(),
        key=lambda item: (-(int(item.get("stars") or 0) + int(item.get("downloads") or 0)), item.get("name", "")),
    )
