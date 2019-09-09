import os, signal


class TestMysql(object):
    if __name__ == "__main__":
        out = os.popen("netstat -ano | findstr chrome.exe").read()
        print(len(out.splitlines()))
        for line in out.splitlines():
            print(line)
            if 'main.py' in line:
                pid = int(line.split()[1])
                try:
                    print(pid)
                    result = os.kill(pid, signal.SIGKILL)
                    print('已杀死pid为%s的进程,　返回值是:%s' % (pid, result))

                except OSError:
                    print('没有如此进程!!!')
