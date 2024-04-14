from multiprocessing import cpu_count

bind = '0.0.0.0:8000'
daemon = False
workers = int(cpu_count() / 2)
worker_class = "gevent"
threads = int(cpu_count())
