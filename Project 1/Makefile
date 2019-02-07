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


# @cut -f1 ./hosts | xargs -I{} rsync --filter='dir-merge,-n /.gitignore' -av . {}:~/proj1/
push-src:
	@cut -f1 ./hosts | xargs -I{} rsync -arv --exclude=__pycache__ . {}:~/proj1/
