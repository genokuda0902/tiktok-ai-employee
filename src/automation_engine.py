"""Isolated orchestration core. No TikTok publishing or unapproved media delivery."""
import json
import os
import re
import sqlite3
import subprocess
import time
from pathlib import Path

ID = re.compile(r"^[A-Za-z0-9_-]{1,80}$")
REQUIRED = ("run_id", "account_id", "plan_id", "topic", "script", "generation_settings")


def validate(request):
    if not isinstance(request, dict) or any(k not in request for k in REQUIRED):
        raise ValueError("missing required fields")
    for key in ("run_id", "account_id", "plan_id"):
        if not isinstance(request[key], str) or not ID.fullmatch(request[key]):
            raise ValueError("invalid " + key)
    if not isinstance(request["topic"], str) or not request["topic"].strip() or len(request["topic"]) > 300:
        raise ValueError("invalid topic")
    if not isinstance(request["script"], (str, list)) or not request["script"]:
        raise ValueError("invalid script")
    if not isinstance(request["generation_settings"], dict):
        raise ValueError("invalid settings")
    return request


def inspect_mp4(path):
    path = Path(path)
    if not path.is_file() or path.suffix.lower() != ".mp4":
        return {"passed": False, "reason": "missing_mp4"}
    try:
        p = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)], capture_output=True, text=True, timeout=30, check=True)
        info = json.loads(p.stdout)
        streams = info.get("streams", [])
        video = next((s for s in streams if s.get("codec_type") == "video"), None)
        audio = any(s.get("codec_type") == "audio" for s in streams)
        duration = float(info.get("format", {}).get("duration", 0))
        width = int(video.get("width", 0)) if video else 0
        height = int(video.get("height", 0)) if video else 0
        passed = bool(video and audio and 5 <= duration <= 180 and height > width and width >= 480 and height >= 854)
        return {"passed": passed, "duration_seconds": duration, "width": width, "height": height, "has_audio": audio, "reason": None if passed else "technical_qa_failed", "human_visual_privacy_approval": False}
    except (OSError, subprocess.SubprocessError, ValueError, KeyError, json.JSONDecodeError):
        return {"passed": False, "reason": "ffprobe_failed"}


class Engine:
    def __init__(self, database):
        self.db = sqlite3.connect(database)
        self.db.execute("CREATE TABLE IF NOT EXISTS jobs (run_id TEXT PRIMARY KEY, account_id TEXT NOT NULL, plan_id TEXT NOT NULL, status TEXT NOT NULL, attempts INTEGER NOT NULL DEFAULT 0, result TEXT NOT NULL DEFAULT '{}', UNIQUE(account_id, plan_id))")
        self.db.commit()

    def submit(self, request):
        validate(request)
        try:
            self.db.execute("INSERT INTO jobs(run_id,account_id,plan_id,status) VALUES(?,?,?,'queued')", (request["run_id"], request["account_id"], request["plan_id"]))
            self.db.commit()
            return "queued"
        except sqlite3.IntegrityError:
            return "duplicate_rejected"

    def execute(self, request, renderer=None, max_attempts=3):
        validate(request)
        if not isinstance(max_attempts, int) or not 1 <= max_attempts <= 5:
            raise ValueError("invalid retry limit")
        row = self.db.execute("SELECT status,attempts FROM jobs WHERE run_id=?", (request["run_id"],)).fetchone()
        if row is None:
            raise ValueError("run must be submitted first")
        status, attempts = row
        if status not in ("queued", "retryable_failure"):
            return status
        if renderer is None:
            self._update(request["run_id"], "renderer_not_connected", attempts, {"error": "renderer_not_connected"})
            return "renderer_not_connected"
        while attempts < max_attempts:
            attempts += 1
            self._update(request["run_id"], "running", attempts, {})
            try:
                result = renderer(request)
                if not isinstance(result, dict) or not isinstance(result.get("video_path"), str):
                    raise ValueError("invalid renderer response")
                qa = inspect_mp4(result["video_path"])
                if not qa["passed"]:
                    self._update(request["run_id"], "qa_failed", attempts, {"qa": qa})
                    return "qa_failed"
                # Technical pass is NOT public-release approval or completion.
                self._update(request["run_id"], "awaiting_human_qa", attempts, {"qa": qa, "video_path": result["video_path"]})
                return "awaiting_human_qa"
            except Exception as exc:
                # Never persist exception text: third-party exceptions can contain secrets.
                self._update(request["run_id"], "retryable_failure" if attempts < max_attempts else "failed", attempts, {"error": type(exc).__name__})
        return "failed"

    def _update(self, run_id, status, attempts, result):
        self.db.execute("UPDATE jobs SET status=?, attempts=?, result=? WHERE run_id=?", (status, attempts, json.dumps(result, ensure_ascii=False), run_id))
        self.db.commit()


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("request", help="local request JSON path")
    parser.add_argument("--db", default="automation_jobs.sqlite3")
    args = parser.parse_args()
    request = json.loads(Path(args.request).read_text(encoding="utf-8"))
    engine = Engine(args.db)
    submitted = engine.submit(request)
    print(json.dumps({"submission": submitted, "status": engine.execute(request) if submitted == "queued" else "duplicate_rejected"}))


if __name__ == "__main__":
    main()
