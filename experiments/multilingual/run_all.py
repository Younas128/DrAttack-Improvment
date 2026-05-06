"""
Runner script for multilingual DrAttack experiments.
Executes Urdu and Pashto attacks sequentially against GPT-5.5.
"""
import subprocess, sys, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def run_script(name, path):
    print(f"\n{'#'*70}")
    print(f"# RUNNING: {name}")
    print(f"{'#'*70}\n")
    result = subprocess.run(
        [sys.executable, path],
        cwd=SCRIPT_DIR,
        capture_output=False,
        text=True,
    )
    if result.returncode != 0:
        print(f"[!] {name} exited with code {result.returncode}")
    else:
        print(f"\n[OK] {name} completed successfully.")

if __name__ == "__main__":
    run_script("DrAttack URDU", os.path.join(SCRIPT_DIR, "drattack_urdu.py"))
    run_script("DrAttack PASHTO", os.path.join(SCRIPT_DIR, "drattack_pashto.py"))
    print(f"\n{'='*70}")
    print("ALL MULTILINGUAL ATTACKS COMPLETE")
    print(f"Results saved to:")
    print(f"  - {os.path.join(SCRIPT_DIR, 'results_urdu_gpt55.json')}")
    print(f"  - {os.path.join(SCRIPT_DIR, 'results_pashto_gpt55.json')}")
    print(f"{'='*70}")
