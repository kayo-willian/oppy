import json
import sqlite3
import sys
from contextlib import closing

import pytest

from oppy import initialize
from oppy.__main__ import main


def test_json_status(tmp_path, monkeypatch, capsys):
    path = tmp_path / "monitor.db"
    monkeypatch.setenv("BEACON_DB_PATH", str(path))
    monkeypatch.setattr(sys, "argv", ["oppy", "status", "--json"])
    monkeypatch.delenv("BEACON_TELEGRAM_TOKEN", raising=False)
    initialize(path)
    main()
    assert json.loads(capsys.readouterr().out) == {
        "last_success_utc": None, "last_failure_utc": None,
        "pending_notifications": 0, "telegram_configured": False,
    }
    with closing(sqlite3.connect(path)) as db, db:
        db.executemany("INSERT INTO collections(observed_at,outcome,reason) VALUES(?,?,?)", [
            ("2026-01-01T07:00:00+02:00", "OK", "private"),
            ("2026-01-01T06:00:00Z", "OK", "private"),
            ("2026-01-02T09:00:00+02:00", "FAILED", "private"),
        ])
        db.execute("INSERT INTO outbox(event_id) VALUES(1)")
    monkeypatch.setenv("BEACON_TELEGRAM_TOKEN", "fixture")
    monkeypatch.setenv("BEACON_TELEGRAM_CHAT_ID", "fixture")
    before = path.read_bytes()
    main()
    assert json.loads(capsys.readouterr().out) == {
        "last_success_utc": "2026-01-01T06:00:00.000Z",
        "last_failure_utc": "2026-01-02T07:00:00.000Z",
        "pending_notifications": 1, "telegram_configured": True,
    }
    assert path.read_bytes() == before


@pytest.mark.parametrize("contents", [None, b"invalid database"])
def test_unavailable_json_status(tmp_path, contents, monkeypatch, capsys):
    path = tmp_path / "private-name"
    if contents is not None:
        path.write_bytes(contents)
    monkeypatch.setenv("BEACON_DB_PATH", str(path))
    monkeypatch.setattr(sys, "argv", ["oppy", "status", "--json"])
    with pytest.raises(SystemExit) as exc:
        main()
    output = capsys.readouterr()
    assert exc.value.code == 1
    assert output.out == ""
    assert output.err == "Status unavailable: check the initialized database.\n"
    assert (path.read_bytes() if path.exists() else None) == contents
