import subprocess
import re

JAVA_EXE = r"C:\Program Files\Microsoft\jdk-21.0.12.101-hotspot\bin\java.exe"
FFDEC_JAR = r"tools\ffdec-26.3.0\ffdec-cli.jar"

def dump_symbols(swf_path):
    print(f"=== SYMBOLCLASS FOR {swf_path} ===")
    cmd = [JAVA_EXE, "-jar", FFDEC_JAR, "-dumpSWF", swf_path]
    res = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
    in_symbol_class = False
    for line in res.stdout.splitlines():
        if "SymbolClass" in line or "ExportAssets" in line:
            in_symbol_class = True
            print(line)
        elif in_symbol_class:
            if line.strip().startswith("0") or line.strip().startswith("Tag:"):
                # end of tag
                if not ("Tag:" in line and "SymbolClass" in line):
                    in_symbol_class = False
            else:
                print(line)

if __name__ == "__main__":
    dump_symbols("archive/clients/local-overrides/mole.61.com/resource/login/LoginHome.swf")
    dump_symbols("archive/clients/local-overrides/mole.61.com/resource/login/Login.swf")
