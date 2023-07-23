import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
accesslog = "-"
loglevel = "debug"
access_log_format = '%(h)s:%(p)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

def worker_exit(server, worker):
    worker.log.info("Worker %s exited" % worker.pid)