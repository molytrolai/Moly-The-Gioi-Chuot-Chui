import subprocess

JAVA_EXE = r"C:\Program Files\Microsoft\jdk-21.0.12.101-hotspot\bin\java.exe"
FFDEC_JAR = r"tools\ffdec-26.3.0\ffdec-cli.jar"

cmd = [JAVA_EXE, "-jar", FFDEC_JAR, "-dumpSWF", "archive/clients/local-overrides/mole.61.com/resource/login/Login.swf"]
res = subprocess.run(cmd, capture_output=True, text=True, errors="replace")

for line in res.stdout.splitlines():
    for bid in [158, 160, 161, 163, 164, 166, 167, 169, 171, 173, 174, 176, 182, 187, 123, 150, 157]:
        if f"chid: {bid}" in line:
            print(line)
