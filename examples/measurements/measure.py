# -*- coding: utf-8 -*-
import os
import time
import psutil
import socket

FILE = socket.gethostname()


# store these as .csv files
class Measure():
    def __init__(self):
        self.pid = os.getpid()
        self.process = psutil.Process(self.pid)

        self.write_to_file = True

    def start_measurement(self, interval):
        # creates an empty file at the tmp location
        a = open(FILE + ".csv", "w+")
        a.close()

        while True:
            print "running"
            cpu = self.measure_cpu()
            print cpu
            mem = self.measure_memory()
            self.save_measurement(cpu, *mem)
            time.sleep(interval)

    def save_measurement(self, cpu, rss, vms, mem_percentage):
        if not self.write_to_file:
            return
        timestamp = time.strftime("%H:%M:%S", time.gmtime())
        with open(FILE + '.csv', 'a+') as csv_file:
            print "saving to file"
            csv_file.write("{0},{1},{2}\n".format(timestamp, cpu, mem_percentage))

    def make_note(self, note):
        if not self.write_to_file:
            return

        with open(FILE + '.csv', 'a+') as csv_file:
            csv_file.write(', , ,{0}\n'.format(note))

    def measure_cpu(self):
        return self.process.get_cpu_percent(interval=1)

    def measure_memory(self):
        mem = self.process.get_memory_info()
        return mem[0], mem[1], self.process.get_memory_percent()

if __name__ == "__main__":
    measure = Measure()
    measure.start_measurement(interval=5)
