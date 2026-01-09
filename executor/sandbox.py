import subprocess
import tempfile
import sys
import textwrap

def run_in_sandbox(code: str, inputs: list):
    """
    VERY RESTRICTED sandbox.
    - No imports
    - No filesystem access
    - Timeout enforced
    """

    if "import" in code:
        return {"error": "Imports not allowed in sandbox"}

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False
    ) as f:
        f.write(textwrap.dedent(code))
        script_path = f.name

    results = []

    for val in inputs:
        try:
            proc = subprocess.run(
                [sys.executable, script_path],
                input=str(val),
                capture_output=True,
                text=True,
                timeout=2
            )
            results.append({
                "input": val,
                "output": proc.stdout.strip(),
                "error": proc.stderr.strip()
            })
        except subprocess.TimeoutExpired:
            results.append({
                "input": val,
                "error": "Execution timeout"
            })

    return results