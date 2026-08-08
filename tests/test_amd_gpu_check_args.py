import subprocess
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "check-docker-amd-gpu.sh"


def wsl_path(path: Path) -> str:
    drive = path.drive.rstrip(":").lower()
    relative = path.relative_to(path.anchor).as_posix()
    return f"/mnt/{drive}/{relative}"


SCRIPT_WSL = wsl_path(SCRIPT)


def test_amd_gpu_check_rejects_unknown_extra_arg_before_diagnostics():
    proc = subprocess.run(
        ["bash", SCRIPT_WSL, "--bad-option"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert proc.returncode == 1
    assert "Unknown option: --bad-option" in proc.stderr


def test_amd_gpu_check_shell_syntax():
    subprocess.run(["bash", "-n", SCRIPT_WSL], check=True)