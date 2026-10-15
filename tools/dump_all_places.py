import subprocess

JAVA_EXE = r"C:\Program Files\Microsoft\jdk-21.0.12.101-hotspot\bin\java.exe"
FFDEC_JAR = r"tools\ffdec-26.3.0\ffdec-cli.jar"

cmd = [JAVA_EXE, "-jar", FFDEC_JAR, "-dumpSWF", "archive/clients/local-overrides/mole.61.com/resource/login/LoginHome.swf"]
res = subprocess.run(cmd, capture_output=True, text=True, errors="replace")

in_main_timeline = False
for line in res.stdout.splitlines():
    if "Tag: 254" in line or "tagId=  1" in line or "ShowFrame" in line:
        pass
    if "PlaceObject" in line:
        print(line)
