from __future__ import annotations

import json
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import streamlit as st

from chat import run_model_tool_loop, trim_history
from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version


ROOT = Path(__file__).parent
ARTIFACTS_DIR = ROOT / "artifacts"
TRANSCRIPTS_DIR = ROOT / "transcripts"
load_lab_env(ROOT)

SENSITIVE_PATTERN = re.compile(
    r"(?i)(password|passwd|token|api[ _-]?key|otp|mfa|recovery[ _-]?code|secret)"
    r"(\s*[:=]\s*|\s+(?:is|la|là)\s+)[^\s,;]+"
)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def redact(value: Any) -> Any:
    """Redact common credential patterns before rendering or persisting data."""
    if isinstance(value, str):
        return SENSITIVE_PATTERN.sub(lambda match: f"{match.group(1)}=[REDACTED]", value)
    if isinstance(value, list):
        return [redact(item) for item in value]
    if isinstance(value, dict):
        return {str(key): redact(item) for key, item in value.items()}
    return value


def pretty_json(value: Any) -> str:
    return json.dumps(redact(value), ensure_ascii=False, indent=2, default=str)


def initial_transcript(version_info: dict[str, str], provider: str, model: str | None) -> dict[str, Any]:
    return {
        "session_id": f"ui_{uuid.uuid4().hex}",
        "version": version_info["version"],
        "artifact_version": version_info["artifact_version"],
        "timestamp": now_iso(),
        "updated_at": now_iso(),
        "provider": provider,
        "model": model,
        "system_prompt": "artifacts/system_prompt.md",
        "tools": "artifacts/tools.yaml",
        "messages": [],
    }


def save_transcript(transcript: dict[str, Any]) -> Path:
    transcript["updated_at"] = now_iso()
    TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    path = TRANSCRIPTS_DIR / f"{transcript['session_id']}.transcript.json"
    path.write_text(json.dumps(redact(transcript), ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    return path


def ensure_session(provider_name: str, model: str | None, version: str) -> None:
    version_info = artifact_version_dict(
        build_artifact_version(version, ARTIFACTS_DIR / "system_prompt.md", ARTIFACTS_DIR / "tools.yaml")
    )
    current = st.session_state.get("transcript")
    if not current or current.get("provider") != provider_name or current.get("version") != version:
        st.session_state.transcript = initial_transcript(version_info, provider_name, model)
        st.session_state.chat_history = []
        st.session_state.last_transcript_path = None


def render_tool_trace(rounds: list[dict[str, Any]]) -> None:
    for round_record in rounds:
        calls = round_record.get("tool_calls", [])
        results = round_record.get("tool_results", [])
        if not calls and not results:
            continue
        with st.expander(f"Tool trace - round {round_record.get('round', '?')}", expanded=True):
            for index, call in enumerate(calls):
                st.markdown(f"**Tool:** `{call.get('name', 'unknown')}`")
                st.code(pretty_json(call.get("args", {})), language="json")
                result = results[index] if index < len(results) else {"error": "missing_tool_result"}
                if isinstance(result.get("result"), dict) and result["result"].get("error"):
                    st.error(pretty_json(result))
                else:
                    st.json(redact(result))


def main() -> None:
    st.set_page_config(page_title="Northstar IT Helpdesk", page_icon="🛠️", layout="wide")
    st.title("Northstar Labs IT Helpdesk")
    st.caption("Synthetic helpdesk environment. Tool calls and results are shown for auditability.")

    with st.sidebar:
        st.header("Session settings")
        provider_name = st.selectbox("Provider", ["gemini", "openrouter", "openai", "anthropic"])
        version = st.selectbox("Artifact version", ["v0", "v1", "v2", "v3"], index=3)
        model = st.text_input("Model override", placeholder="Leave blank for provider default") or None
        history_window = st.number_input("History pairs", min_value=1, max_value=20, value=5)
        clear_requested = st.button("Clear conversation", use_container_width=True)

        version_info = artifact_version_dict(
            build_artifact_version(version, ARTIFACTS_DIR / "system_prompt.md", ARTIFACTS_DIR / "tools.yaml")
        )
        st.caption(f"Artifact: `{version_info['artifact_version']}`")

    ensure_session(provider_name, model, version)
    transcript = st.session_state.transcript
    if clear_requested:
        st.session_state.chat_history = []
        transcript["messages"] = []
        path = save_transcript(transcript)
        st.session_state.last_transcript_path = str(path)
        st.rerun()

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message.get("rounds"):
                render_tool_trace(message["rounds"])

    prompt = st.chat_input("Mô tả vấn đề IT của bạn...")
    if not prompt:
        if st.session_state.get("last_transcript_path"):
            st.caption(f"Transcript: `{st.session_state.last_transcript_path}`")
        return

    with st.chat_message("user"):
        st.markdown(prompt)

    system_prompt = (ARTIFACTS_DIR / "system_prompt.md").read_text(encoding="utf-8")
    declarations = load_tool_declarations(ARTIFACTS_DIR / "tools.yaml")
    provider = make_provider(provider_name)
    selected_model = model or getattr(provider, "default_model", None)
    messages = [
        {"role": "system", "content": system_prompt},
        *trim_history(st.session_state.chat_history, int(history_window)),
        {"role": "user", "content": prompt},
    ]

    error_logs: list[dict[str, str]] = []
    try:
        result = run_model_tool_loop(
            provider=provider,
            messages=messages,
            tools=to_openai_tools(declarations),
            model=selected_model,
            max_tool_rounds=4,
        )
        assistant_text = result["assistant_text"] or ""
        rounds = redact(result.get("rounds", []))
        tool_results = redact(result.get("tool_events", []))
        for event in tool_results:
            event_result = event.get("result", {})
            if isinstance(event_result, dict) and event_result.get("error"):
                error_logs.append({"tool": str(event.get("tool")), "error": str(event_result.get("error"))})
    except Exception as exc:
        assistant_text = f"Provider error: {type(exc).__name__}: {exc}"
        rounds = []
        tool_results = []
        error_logs.append({"type": type(exc).__name__, "message": str(exc)})

    with st.chat_message("assistant"):
        st.markdown(assistant_text)
        render_tool_trace(rounds)
        if error_logs:
            st.error(pretty_json(error_logs))

    st.session_state.chat_history.append({"role": "user", "content": redact(prompt)})
    st.session_state.chat_history.append({"role": "assistant", "content": redact(assistant_text), "rounds": rounds})
    transcript["messages"].append({
        "timestamp": now_iso(),
        "user_input": redact(prompt),
        "assistant_text": redact(assistant_text),
        "tool_calls": redact([call for round_record in rounds for call in round_record.get("tool_calls", [])]),
        "tool_results": tool_results,
        "error_logs": error_logs,
    })
    path = save_transcript(transcript)
    st.session_state.last_transcript_path = str(path)
    st.caption(f"Transcript saved: `{path}`")


if __name__ == "__main__":
    main()