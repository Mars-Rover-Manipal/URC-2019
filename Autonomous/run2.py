import time
import subprocess

test_cmd = "".join([
    "import time;",
    "print('starting script{}...');",
    "time.sleep(1);",
    "print('script{} done.')"
])

for i in range(2):
    subprocess.Popen(
        ["python", "-c", test_cmd.format(*[str(i)] * 2)], shell=True).wait()
    print('-'*80)