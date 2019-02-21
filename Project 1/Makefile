default: ping

# See if the cluster is up
ping:
	@./run-all uptime

ls:
	@./run-all ls "~"

# Reboot machines
restart-all:
	@./run-all -sudo -P shutdown -r now

ports:
	@./run-all -sudo netstat -ntulp

status:
	@./run-all "ps -elf | grep [g]unicorn"

stop:
	@./run-all 'pkill gunicorn; pkill gunicorn3'

start:
	@./run-all 'cd proj1/datadrop; gunicorn3 -c guni.conf.py app:app;'

# This didn't work: https://unix.stackexchange.com/a/168602
# @cut -f1 ./hosts | xargs -I{} rsync --filter='dir-merge,-n /.gitignore' -av . {}:~/proj1/
push-src:
	@cut -f1 ./hosts | xargs -I{} rsync -arv --exclude={__pycache__,*.sql,uploads,*.log} . {}:~/proj1/
