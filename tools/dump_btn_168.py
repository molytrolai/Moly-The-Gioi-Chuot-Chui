import subprocess

JAVA_EXE = r"C:\Program Files\Microsoft\jdk-21.0.12.101-hotspot\bin\java.exe"
FFDEC_JAR = r"tools\ffdec-26.3.0\ffdec-cli.jar"

cmd = [JAVA_EXE, "-jar", FFDEC_JAR, "-dumpSWF", "archive/clients/local-overrides/mole.61.com/resource/login/LoginHome.swf"]
res = subprocess.run(cmd, capture_output=True, text=True, errors="replace")

in_btn = False
for line in res.stdout.splitlines():
    if "chid: 168" in line:
        in_btn = True
        print(line)
    elif in_btn:
        if "Define" in line and "chid:" in line:
            break
        print(line)
