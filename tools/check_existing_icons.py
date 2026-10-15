import os
from pathlib import Path

def main():
    print("Searching for existing toolbar icon files in workspace...")
    for root, dirs, files in os.walk("."):
        if any(skip in root for skip in [".git", "node_modules", "tools\\ffdec"]):
            continue
        for f in files:
            if any(num in f for num in ["3279", "6834", "6836", "6839", "6841", "6844", "6846", "6849", "6851", "6854", "6856", "6859", "6861", "6864", "6866", "6929", "6931"]):
                print("Found:", os.path.join(root, f))

if __name__ == "__main__":
    main()
