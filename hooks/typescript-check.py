#!/usr/bin/env python3
"""
Post-edit TypeScript type checking hook.
Runs tsc --noEmit after editing .ts/.tsx files.
Informational only - never blocks operations.
"""
import json
import subprocess
import sys
import os


TS_EXTENSIONS = {'.ts', '.tsx'}


def find_tsconfig(file_path):
    directory = os.path.dirname(os.path.abspath(file_path))
    while directory != os.path.dirname(directory):
        tsconfig = os.path.join(directory, 'tsconfig.json')
        if os.path.exists(tsconfig):
            return tsconfig
        directory = os.path.dirname(directory)
    return None


def main():
    try:
        input_data = json.load(sys.stdin)
        tool_input = input_data.get('tool_input', {})

        file_path = tool_input.get('file_path', '')
        if not file_path:
            sys.exit(0)

        ext = os.path.splitext(file_path)[1].lower()
        if ext not in TS_EXTENSIONS:
            sys.exit(0)

        tsconfig = find_tsconfig(file_path)
        if not tsconfig:
            sys.exit(0)

        project_dir = os.path.dirname(tsconfig)

        try:
            result = subprocess.run(
                ['npx', 'tsc', '--noEmit', '--pretty'],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=project_dir,
            )

            if result.returncode != 0 and result.stdout:
                print("TypeScript errors found — fix these before committing to maintain type safety:")
                print(f"  File edited: {os.path.basename(file_path)}")
                print(result.stdout[:2000])
                if len(result.stdout) > 2000:
                    print("  ... (truncated)")
                print("Run 'npx tsc --noEmit' locally to see full error output.")

        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

    except Exception:
        pass

    sys.exit(0)


if __name__ == '__main__':
    main()
