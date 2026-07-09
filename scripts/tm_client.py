"""
Thin client for a transfermarkt-api instance (https://github.com/felipeall/transfermarkt-api).

Wraps the two endpoints the market-value sync needs:
  - GET /players/search/{name}        -> candidates (name, club, age, marketValue, tm id)
  - GET /players/{id}/market_value    -> exact current market value for a known tm id

Retries with backoff on 429 / transient errors, and applies a fixed courtesy
delay between calls so we stay friendly to the (possibly self-hosted) scraper.
"""

from __future__ import annotations

import re
import time
from dataclasses import dataclass
from typing import Optional

import httpx
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)


class TransfermarktError(Exception):
    """Raised when the TM API is unreachable or returns an unusable response."""


class RateLimited(TransfermarktError):
    """Raised on HTTP 429 so tenacity can back off and retry."""


@dataclass
class TMCandidate:
    tm_id: str
    name: str
    club_name: Optional[str]
    club_id: Optional[str]
    age: Optional[str]
    market_value: Optional[int]  # in euros, already parsed


# ----------------------------------------------------------------------------
# Market-value string parsing
# TM search returns values like "€35.00m", "€900k", "-" (unknown), or "".
# The /market_value endpoint returns a clean integer, so this only handles the
# search-result strings.
# ----------------------------------------------------------------------------
_MV_RE = re.compile(r"€?\s*([\d.,]+)\s*([mk]?)", re.IGNORECASE)


def parse_market_value(raw) -> Optional[int]:
    """Convert a TM market value to an integer number of euros.

    The API returns this already coerced to an int (e.g. 35000000); older/other
    shapes return strings ("€35.00m", "€900k"). Handle both.

    35000000 -> 35_000_000 ; "€35.00m" -> 35_000_000 ; "-"/""/None -> None
    """
    if raw is None:
        return None
    if isinstance(raw, bool):
        return None
    if isinstance(raw, (int, float)):
        return int(raw)
    raw = str(raw).strip()
    if raw in {"-", "–", ""}:
        return None
    m = _MV_RE.search(raw)
    if not m:
        return None
    number, suffix = m.group(1), m.group(2).lower()
    # TM uses "." as the decimal separator in these strings (e.g. 35.00m).
    try:
        value = float(number.replace(",", ""))
    except ValueError:
        return None
    if suffix == "m":
        value *= 1_000_000
    elif suffix == "k":
        value *= 1_000
    return int(round(value))


class TransfermarktClient:
    def __init__(self, base_url: str, delay: float = 0.5, timeout: float = 30.0):
        self.base_url = base_url.rstrip("/")
        self.delay = delay
        self._client = httpx.Client(
            base_url=self.base_url,
            timeout=timeout,
            headers={"Accept": "application/json"},
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "TransfermarktClient":
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    @retry(
        retry=retry_if_exception_type(RateLimited),
        wait=wait_exponential(multiplier=2, min=2, max=60),
        stop=stop_after_attempt(5),
        reraise=True,
    )
    def _get(self, path: str) -> dict:
        time.sleep(self.delay)
        try:
            resp = self._client.get(path)
        except httpx.HTTPError as e:
            raise TransfermarktError(f"request to {path} failed: {e}") from e
        if resp.status_code == 429:
            raise RateLimited(f"429 from {path}")
        if resp.status_code == 404:
            return {}
        if resp.status_code >= 400:
            raise TransfermarktError(f"{resp.status_code} from {path}: {resp.text[:200]}")
        try:
            return resp.json()
        except ValueError as e:
            raise TransfermarktError(f"non-JSON from {path}: {e}") from e

    def search(self, name: str) -> list[TMCandidate]:
        """Search players by name; returns parsed candidates (may be empty)."""
        data = self._get(f"/players/search/{httpx.URL(name).path or name}")
        results = data.get("results") or []
        candidates: list[TMCandidate] = []
        for r in results:
            club = r.get("club") or {}
            candidates.append(
                TMCandidate(
                    tm_id=str(r.get("id")),
                    name=r.get("name") or "",
                    club_name=club.get("name"),
                    club_id=str(club.get("id")) if club.get("id") else None,
                    age=str(r.get("age")) if r.get("age") is not None else None,
                    market_value=parse_market_value(r.get("marketValue")),
                )
            )
        return candidates

    def market_value(self, tm_id: str) -> Optional[int]:
        """Exact current market value (euros) for a known TM id, or None."""
        data = self._get(f"/players/{tm_id}/market_value")
        if not data:
            return None
        mv = data.get("market_value")
        if isinstance(mv, (int, float)):
            return int(mv)
        # Fallback: some deployments return the string form.
        return parse_market_value(mv if isinstance(mv, str) else None)
