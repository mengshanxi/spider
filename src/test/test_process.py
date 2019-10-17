import os, signal

if __name__ == "__main__":
    out = os.popen("ps aux | grep delete").read()
    print(len(out.splitlines()))
    for line in out.splitlines():
        print(line)
        if 'delete' in line:
            pid = int(line.split()[1])
            try:
                print(pid)
                result = os.kill(pid, signal.SIGKILL)
                print('已杀死pid为%s的进程,　返回值是:%s' % (pid, result))

            except OSError:
                print('没有如此进程!!!')
