"""
Player matching: pick the right Transfermarkt candidate for a DB player.

The core problem is duplicate names — "Rodrigo", "Danilo", "Vitinha" all map
to several real players. We disambiguate using the club we already hold in the
DB. The rule set is deliberately conservative: when we cannot confidently pick
one candidate, we return no match and the caller flags the player for review
rather than writing a possibly-wrong value.
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass
from typing import Optional, Sequence

from tm_client import TMCandidate


def normalize(text: Optional[str]) -> str:
    """Lowercase, strip accents and punctuation, collapse whitespace."""
    if not text:
        return ""
    nfkd = unicodedata.normalize("NFKD", text)
    ascii_text = "".join(c for c in nfkd if not unicodedata.combining(c))
    ascii_text = ascii_text.lower()
    out = []
    for ch in ascii_text:
        if ch.isalnum() or ch.isspace():
            out.append(ch)
        else:
            out.append(" ")
    return " ".join("".join(out).split())


# Common club-name noise so "Manchester City FC" ~ "Man City" get closer.
_CLUB_STOPWORDS = {
    "fc", "cf", "afc", "sc", "ac", "as", "ss", "ssc", "us", "if", "bk", "fk",
    "club", "cd", "ca", "rc", "sv", "vfb", "vfl", "tsg", "bv", "de", "the",
}


def _club_tokens(club: Optional[str]) -> set[str]:
    return {t for t in normalize(club).split() if t and t not in _CLUB_STOPWORDS}


def club_similarity(a: Optional[str], b: Optional[str]) -> float:
    """Token overlap (Jaccard) between two club names, 0.0–1.0."""
    ta, tb = _club_tokens(a), _club_tokens(b)
    if not ta or not tb:
        return 0.0
    inter = ta & tb
    union = ta | tb
    return len(inter) / len(union)


# Confidence thresholds.
CLUB_MATCH_MIN = 0.5   # a candidate's club must overlap this much to "confirm"
NAME_MATCH_MIN = 0.6   # unlikely-typo guard when a name is only loosely equal


@dataclass
class MatchResult:
    candidate: Optional[TMCandidate]
    reason: str  # machine-readable outcome for logging/review


def match_player(
    db_name: str,
    db_club: Optional[str],
    candidates: Sequence[TMCandidate],
) -> MatchResult:
    """Choose the best TM candidate for a DB player, or none if ambiguous.

    Strategy (in order):
      1. No candidates                          -> no_candidates
      2. Exactly one candidate                  -> single_candidate (accept)
      3. Multiple, one clearly best by club     -> club_confirmed (accept)
      4. Multiple, club can't disambiguate      -> ambiguous (skip + flag)
    """
    if not candidates:
        return MatchResult(None, "no_candidates")

    n_db = normalize(db_name)
    # Keep only candidates whose name genuinely matches (search can be fuzzy).
    named = [c for c in candidates if _name_matches(n_db, normalize(c.name))]
    if not named:
        return MatchResult(None, "no_name_match")

    if len(named) == 1:
        return MatchResult(named[0], "single_candidate")

    # Multiple same-name players: rank by club similarity to what we hold.
    if not db_club:
        return MatchResult(None, "ambiguous_no_db_club")

    scored = sorted(
        ((club_similarity(db_club, c.club_name), c) for c in named),
        key=lambda p: p[0],
        reverse=True,
    )
    best_score, best = scored[0]
    second_score = scored[1][0] if len(scored) > 1 else 0.0

    if best_score >= CLUB_MATCH_MIN and best_score > second_score:
        return MatchResult(best, "club_confirmed")

    return MatchResult(None, "ambiguous_club_unclear")


def _name_matches(a: str, b: str) -> bool:
    if not a or not b:
        return False
    if a == b:
        return True
    ta, tb = set(a.split()), set(b.split())
    if not ta or not tb:
        return False
    # Transfermarkt frequently shortens full legal names — the DB may hold
    # "Esnaider Eliecer Cabezas Castillo" while TM lists "Esnáider Cabezas".
    # Accept when one name's tokens are fully contained in the other's, as long
    # as the shorter side has real substance (>= 2 tokens, to avoid a lone
    # common first name matching everyone). Club confirmation still guards the
    # multi-candidate case upstream.
    shorter, longer = (ta, tb) if len(ta) <= len(tb) else (tb, ta)
    if len(shorter) >= 2 and shorter <= longer:
        return True
    overlap = len(ta & tb) / len(ta | tb)
    return overlap >= NAME_MATCH_MIN
