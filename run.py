from subprocess import Popen, Popen
import os
import time
from datetime import datetime
print(os.getcwd())


def enviroments(x): return "TRACE_SAMPLES={}\nTRACE_SIZE={}\nTRACE_INTER_ARRIVAL={}\nTRACE_READ_RATIO={}\nTRACE_SAS_SIZE={}\nTRACE_DISTRIBUTION={}\nTRACE_MEAN={}\nTRACE_STD={}\nTRACE_CONCURRENCY={}\nQUEUE_SIMULATOR_AVG_SERVICE_TIME={}\nQUEUE_SIMULATOR_NUM_DELAYS_REQUIRED={}\nOUTPUT_PATH=/usr/src/app/results/".format(
    x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9], x[10])


if __name__ == '__main__':
    # print(docker)
    lines = None
    with open("params.csv", 'r') as f:
        lines = f.readlines()
        lines = list(map(lambda x: x.strip(), lines))
        lines = list(map(lambda x: x.split(','), lines))

    for index, l in enumerate(lines):
        env = enviroments(l)
        with open("test.env", 'w') as f:
            f.write(env)
            f.close()
        docker = Popen(["docker", "run", "--rm", '--name', 'test_{}'.format(index), '--env-file', './test.env',
                        '-v', str(os.getcwd())+'/results:/usr/src/app/results', 'nachocode/cinvestav-ds-middleware'])
        time.sleep(1.5)
        print("{} - Test[{}] Completed - {}".format(datetime.now(), index, l))
