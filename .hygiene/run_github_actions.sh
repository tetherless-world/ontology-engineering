#!/usr/bin/env bash
set -euo pipefail

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/set_env.sh"

git -C "$REPO_DIR" rev-parse --is-inside-work-tree >/dev/null
if [[ "$(git -C "$REPO_DIR" rev-parse --abbrev-ref HEAD)" == "HEAD" ]]; then
  echo "ERROR: publisher needs a local Git branch; see the workflow's branch step." >&2
  exit 1
fi
if [[ ! -d "$REPO_DIR/$ONTPUB_SUBDIR" ]]; then
  echo "ERROR: ontology source directory does not exist: $REPO_DIR/$ONTPUB_SUBDIR" >&2
  exit 1
fi
if [[ ! -d "$REPO_DIR/$HYGIENE_TEST_SUBDIR" ]]; then
  echo "ERROR: hygiene test directory does not exist: $REPO_DIR/$HYGIENE_TEST_SUBDIR" >&2
  exit 1
fi

printf 'Ontology sources: %s\nNamespace filter: %s\nQueries: %s\n' \
  "$ONTPUB_SUBDIR" "$HYGIENE_NAMESPACE_REGEX" "$HYGIENE_TEST_SUBDIR"

# Scope cleanup to this invocation. The course Compose file retains its fixed
# container name, so only one local hygiene job can run at a time.
compose=(docker compose --project-name "ontology-hygiene-$$" --file "$HYGIENE_DIR/docker-compose.yml")
cleanup() {
  "${compose[@]}" down --remove-orphans || true
}
trap cleanup EXIT

"${compose[@]}" pull hygiene
"${compose[@]}" up -d hygiene
container_id=$("${compose[@]}" ps -q hygiene)
if [[ -z "$container_id" ]]; then
  echo "ERROR: hygiene container did not start." >&2
  exit 1
fi

docker exec "$container_id" mkdir -p /input /output
docker cp "$REPO_DIR" "$container_id:/input/$ONTPUB_FAMILY"

# Create the result directory after copying the repo; only fresh results count.
mkdir -p "$OUTPUT_DIR"
run_output=$(mktemp -d "$OUTPUT_DIR/run.XXXXXX")
publisher_status=0
docker exec "$container_id" /publisher/publish.sh hygiene || publisher_status=$?

# Try to retain reports even when the publisher returns an error.
if ! docker cp "$container_id:/output/$ONTPUB_FAMILY" "$run_output/"; then
  echo "ERROR: could not copy publisher output; inspect the workflow logs." >&2
  exit 1
fi

echo "Reports copied to $run_output"
report_status=0
python3 "$HYGIENE_DIR/verify_reports.py" "$run_output" || report_status=$?

if [[ "$publisher_status" -ne 0 ]]; then
  echo "ERROR: publisher exited with status $publisher_status." >&2
  exit "$publisher_status"
fi
exit "$report_status"
