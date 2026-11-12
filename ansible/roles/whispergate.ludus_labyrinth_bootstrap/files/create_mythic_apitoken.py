#!/usr/bin/env python3
"""Create a Mythic operator API token via GraphQL login."""
from __future__ import annotations

import json
import os
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request


def parse_cli_value(raw: str, key: str) -> str:
    """Pull a secret out of `mythic-cli config get` output.

    Current mythic-cli prints `MYTHIC_ADMIN_PASSWORD = <secret>`. Older builds
    print `MYTHIC_ADMIN_PASSWORD <secret>` or only the secret.
    """
    text = raw.replace("\r", "").strip()
    if not text:
        return ""
    keyed = re.search(rf"(?im)^{re.escape(key)}\s*=\s*(\S+)\s*$", text)
    if keyed:
        return keyed.group(1).strip().strip('"').strip("'")
    keyed = re.search(rf"(?im)^{re.escape(key)}\s+(\S+)\s*$", text)
    if keyed and keyed.group(1) != "=":
        return keyed.group(1).strip().strip('"').strip("'")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if len(lines) == 1 and "=" not in lines[0] and " " not in lines[0]:
        return lines[0].strip().strip('"').strip("'")
    return ""


def read_dotenv_value(path: str, key: str) -> str:
    if not path or not os.path.isfile(path):
        return ""
    wanted = key.lower()
    try:
        with open(path, encoding="utf-8", errors="replace") as handle:
            for line in handle:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                name, value = line.split("=", 1)
                if name.strip().lower() == wanted:
                    return value.strip().strip('"').strip("'")
    except OSError as exc:
        print(f"warning: could not read {path}: {exc}", file=sys.stderr)
    return ""


def graphql_urls(url: str) -> list[str]:
    base = url.rstrip("/")
    return [base + "/", base]


def auth_urls(graphql_url: str) -> list[str]:
    parsed = urllib.parse.urlparse(graphql_url)
    root = urllib.parse.urlunparse((parsed.scheme, parsed.netloc, "", "", "", ""))
    return [root + "/auth", root + "/auth/"]


def access_token_from(body: dict) -> str:
    if body.get("access_token"):
        return str(body["access_token"])
    login_body = (body.get("data") or {}).get("login") or {}
    return str(login_body.get("access_token") or "")


def post_json(url: str, payload: dict, headers: dict | None = None) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json", **(headers or {})},
        method="POST",
    )
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=60) as resp:
            body = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        raise RuntimeError(f"HTTP {exc.code} from {url}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"request to {url} failed: {exc.reason}") from exc
    try:
        return json.loads(body)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"non-JSON response from {url}: {body[:300]}") from exc


def login(graphql_url: str, username: str, password: str) -> str:
    """Log in through Mythic's /auth endpoint.

    /graphql is behind Hasura's auth hook and rejects calls that do not already
    have a bearer token, including the login mutation.
    """
    payload = {"username": username, "password": password}
    errors: list[str] = []
    for url in auth_urls(graphql_url):
        try:
            body = post_json(url, payload)
        except RuntimeError as exc:
            errors.append(str(exc))
            continue
        if body.get("errors"):
            errors.append(f"{url}: {json.dumps(body['errors'])[:400]}")
            continue
        if body.get("error"):
            errors.append(f"{url}: {body.get('error')}")
            continue
        token = access_token_from(body)
        status = str(body.get("status") or "")
        if token and status.lower() not in {"error", "failed"}:
            return token
        errors.append(f"{url}: login response had no access_token")
    raise RuntimeError("Mythic login failed. " + " | ".join(errors))


def create_token(url: str, access: str, name: str) -> str:
    # This Mythic build requires token_type and rejects name and scopes.
    # Do not send a variables object: Hasura rejects variables the query does not declare.
    del name
    query = """
    mutation CreateToken {
      createAPIToken(token_type: "User") {
        status
        error
        token_value
      }
    }
    """
    body = post_json(
        url,
        {"query": query},
        headers={"Authorization": f"Bearer {access}"},
    )
    if body.get("errors"):
        raise RuntimeError(json.dumps(body["errors"])[:400])
    block = (body.get("data") or {}).get("createAPIToken") or {}
    value = block.get("token_value") or ""
    if block.get("status") == "success" and value:
        return value
    raise RuntimeError(block.get("error") or "createAPIToken did not return a token")


def write_error(message: str) -> None:
    state_dir = os.environ.get("MYTHIC_TOKEN_ERROR_DIR", "")
    text = message.strip() + "\n"
    print(text, file=sys.stderr, end="")
    if not state_dir:
        return
    try:
        os.makedirs(state_dir, exist_ok=True)
        path = os.path.join(state_dir, "mythic-token.err")
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text)
    except OSError as exc:
        print(f"warning: could not write mythic-token.err: {exc}", file=sys.stderr)


def resolve_password() -> str:
    dotenv = read_dotenv_value(os.environ.get("MYTHIC_DOTENV", ""), "MYTHIC_ADMIN_PASSWORD")
    if dotenv:
        return dotenv
    parsed = parse_cli_value(os.environ.get("MYTHIC_ADMIN_PASSWORD", ""), "MYTHIC_ADMIN_PASSWORD")
    if parsed:
        return parsed
    return ""


def main() -> int:
    graphql_url = os.environ.get("MYTHIC_GRAPHQL_URL", "https://127.0.0.1:7443/graphql/")
    username = os.environ.get("MYTHIC_ADMIN_USER", "mythic_admin")
    token_name = os.environ.get("MYTHIC_TOKEN_NAME", "labyrinth-bootstrap")
    password = resolve_password()
    if not password:
        write_error(
            "Mythic admin password was empty. mythic-cli output could not be parsed "
            "and .env did not contain MYTHIC_ADMIN_PASSWORD."
        )
        return 1
    try:
        access = login(graphql_url, username, password)
        token_errors: list[str] = []
        for url in graphql_urls(graphql_url):
            try:
                print(create_token(url, access, token_name))
                return 0
            except RuntimeError as exc:
                token_errors.append(f"{url}: {exc}")
        raise RuntimeError(" | ".join(token_errors))
    except RuntimeError as exc:
        write_error(str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
