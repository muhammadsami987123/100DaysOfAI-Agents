"""Simple non-interactive smoke test for InvestmentAdvisorBot"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent

def run():
    cmd = [sys.executable, str(HERE / 'main.py'), '--income', '1500', '--age', '29', '--risk', 'medium', '--goal', 'retirement', '--export-json', '--non-interactive']
    print('Running:', ' '.join(cmd))
    p = subprocess.run(cmd, capture_output=True, text=True)
    print('Return code:', p.returncode)
    print(p.stdout)
    print(p.stderr)

if __name__ == '__main__':
    run()
