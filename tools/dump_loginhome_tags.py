import subprocess

JAVA_EXE = r"C:\Program Files\Microsoft\jdk-21.0.12.101-hotspot\bin\java.exe"
FFDEC_JAR = r"tools\ffdec-26.3.0\ffdec-cli.jar"

cmd = [JAVA_EXE, "-jar", FFDEC_JAR, "-dumpSWF", "archive/clients/local-overrides/mole.61.com/resource/login/LoginHome.swf"]
res = subprocess.run(cmd, capture_output=True, text=True, errors="replace")

for line in res.stdout.splitlines():
    if "PlaceObject2" in line or "DefineButton2" in line or "DefineText" in line or "DefineBits" in line:
        if any(w in line for w in ["start", "btn", "logo", "168", "169", "171", "172", "174", "183", "186", "226", "228", "232", "234", "197"]):
            print(line)
