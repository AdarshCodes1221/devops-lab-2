#!/usr/bin/env bash
set -euo pipefail
ansible localhost -i localhost, -c local -m ansible.builtin.stat -a "path=terraform/output.end"
ansible localhost -i localhost, -c local -m ansible.builtin.command -a "cat terraform/output.end"
