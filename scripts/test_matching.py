"""Offline unit tests for the value parser and the disambiguation logic.

Run: python -m pytest scripts/test_matching.py   (or: python scripts/test_matching.py)
No network or DB required.
"""

from matching import club_similarity, match_player, normalize
from tm_client import TMCandidate, parse_market_value


def test_parse_market_value():
    assert parse_market_value("€35.00m") == 35_000_000
    assert parse_market_value("€900k") == 900_000
    assert parse_market_value("€1.50m") == 1_500_000
    assert parse_market_value("-") is None
    assert parse_market_value("") is None
    assert parse_market_value(None) is None


def test_normalize():
    assert normalize("Ousmane Diomandé") == "ousmane diomande"
    assert normalize("Gonçalo Inácio") == "goncalo inacio"
    assert normalize("  FC   Barcelona ") == "fc barcelona"


def test_club_similarity():
    assert club_similarity("Manchester City", "Manchester City FC") == 1.0
    # Abbreviated names overlap only partially ("sporting") -> deliberately low,
    # which routes such cases to review rather than a guessed match.
    assert 0.2 <= club_similarity("Sporting CP", "Sporting Clube de Portugal") < 0.5
    assert club_similarity("Ajax", "Chelsea") == 0.0


def _c(tm_id, name, club, mv=None):
    return TMCandidate(tm_id=tm_id, name=name, club_name=club, club_id=None,
                       age=None, market_value=mv)


def test_single_candidate_accepted():
    res = match_player("Leny Yoro", "Lille OSC",
                       [_c("1", "Leny Yoro", "Manchester United")])
    assert res.candidate is not None and res.reason == "single_candidate"


def test_no_candidates():
    assert match_player("Nobody", "X", []).candidate is None


def test_club_disambiguation():
    cands = [
        _c("1", "Danilo", "Juventus"),
        _c("2", "Danilo", "Nottingham Forest"),
    ]
    res = match_player("Danilo", "Nottingham Forest FC", cands)
    assert res.candidate is not None
    assert res.candidate.tm_id == "2"
    assert res.reason == "club_confirmed"


def test_ambiguous_when_club_unclear():
    cands = [
        _c("1", "Rodrigo", "Real Betis"),
        _c("2", "Rodrigo", "Al-Qadsiah"),
    ]
    res = match_player("Rodrigo", "Some Unrelated Club", cands)
    assert res.candidate is None
    assert res.reason == "ambiguous_club_unclear"


def test_ambiguous_when_no_db_club():
    cands = [_c("1", "Vitinha", "PSG"), _c("2", "Vitinha", "Marseille")]
    res = match_player("Vitinha", None, cands)
    assert res.candidate is None
    assert res.reason == "ambiguous_no_db_club"


def test_tm_shortens_full_legal_name():
    # DB holds the full legal name; TM uses a shorter common name.
    res = match_player(
        "Esnaider Eliecer Cabezas Castillo", "Guayaquil City",
        [_c("682082", "Esnáider Cabezas", "Guayaquil City FC", 225000)],
    )
    assert res.candidate is not None and res.candidate.tm_id == "682082"

    res2 = match_player(
        "Jonathan Vidal Ramos Benitez", "Sportivo Luqueño",
        [_c("1375809", "Jonathan Ramos", "Sportivo Luqueño", 350000)],
    )
    assert res2.candidate is not None


def test_lone_common_first_name_not_matched():
    # A single shared common token must NOT match (would match everyone).
    res = match_player(
        "Rodrigo Hernandez", "Manchester City",
        [_c("1", "Rodrigo", "Real Betis")],
    )
    # "rodrigo" alone (1 token) is not enough substance to auto-accept.
    assert res.candidate is None


if __name__ == "__main__":
    import sys
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for fn in fns:
        try:
            fn()
            print(f"PASS {fn.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL {fn.__name__}: {e}")
    print(f"\n{len(fns) - failed}/{len(fns)} passed")
    sys.exit(1 if failed else 0)
