bind = '0.0.0.0:5000'
backlog = 2048

workers = 17
worker_class = 'sync'
worker_connections = 1000
timeout = 1800
keepalive = 2

reload = True

daemon = True
pidfile = "/tmp/gunicorn.pid"
umask = 0
user = None
group = None
tmp_upload_dir = None

errorlog = 'gunicorn.error.log'
loglevel = 'info'
accesslog = 'gunicorn.access.log'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
