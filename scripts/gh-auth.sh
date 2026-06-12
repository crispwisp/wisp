#!/usr/bin/env bash
# gh-auth — authenticate the GitHub CLI the boring, reliable way: a token.
#
# The interactive device flow (typing a code into a browser, waiting out a
# disabled Authorize button) is fragile to automate and easy to fumble. The
# documented, TOS-clean alternative is `gh auth login --with-token`. This
# wrapper feeds it a token from a local secrets file or the environment, then
# verifies the session — no browser, no clicking, fully scriptable.
#
# Token sources, in order of precedence:
#   1. $GH_TOKEN / $GITHUB_TOKEN
#   2. a `github_token:` line in $WISP_CREDENTIALS
#      (default ~/.local/share/wisp/credentials, mode 600, never committed)
#
# Create the token once at https://github.com/settings/tokens
#   - classic: scopes  repo, read:org, gist, workflow  (+ user, delete_repo if needed)
#   - or a fine-grained token scoped to your repos
# then paste it into the credentials file as:  github_token: ghp_xxx
#
# Usage:
#   gh-auth.sh             authenticate (no-op if already logged in)
#   gh-auth.sh --force     re-authenticate even if a session exists
#   gh-auth.sh --status    just report the current session
set -euo pipefail

CRED="${WISP_CREDENTIALS:-$HOME/.local/share/wisp/credentials}"
HOST="github.com"

token_from_creds() {
  [ -f "$CRED" ] || return 1
  # first `github_token:` value, whitespace-trimmed
  awk -F': *' '/^[[:space:]]*github_token:/ {print $2; exit}' "$CRED" | tr -d '[:space:]'
}

case "${1:-}" in
  --status)
    gh auth status -h "$HOST"
    exit $?
    ;;
esac

if [ "${1:-}" != "--force" ] && gh auth status -h "$HOST" >/dev/null 2>&1; then
  echo "already authenticated as $(gh api user --jq .login 2>/dev/null || echo '?')"
  exit 0
fi

TOKEN="${GH_TOKEN:-${GITHUB_TOKEN:-$(token_from_creds || true)}}"
if [ -z "${TOKEN:-}" ]; then
  echo "no token found." >&2
  echo "set \$GH_TOKEN or add a 'github_token:' line to $CRED" >&2
  echo "create one at https://github.com/settings/tokens" >&2
  exit 1
fi

printf '%s' "$TOKEN" | gh auth login -h "$HOST" --with-token
gh auth status -h "$HOST"
echo "logged in as $(gh api user --jq .login)"
