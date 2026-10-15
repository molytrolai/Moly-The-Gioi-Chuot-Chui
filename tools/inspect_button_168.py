import subprocess
from pathlib import Path

JAVA_EXE = r"C:\Program Files\Microsoft\jdk-21.0.12.101-hotspot\bin\java.exe"
FFDEC_JAR = r"tools\ffdec-26.3.0\ffdec-cli.jar"

cmd = [JAVA_EXE, "-jar", FFDEC_JAR, "-dumpSWF", "archive/clients/local-overrides/mole.61.com/resource/login/LoginHome.swf"]
res = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
lines = res.stdout.splitlines()

capture = False
for line in lines:
    if "chid: 168" in line:
        capture = True
        print(line)
    elif capture:
        if "chid:" in line and "Define" in line:
            break
        print(line)
