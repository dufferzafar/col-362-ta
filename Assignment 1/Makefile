default: ping

# See if the cluster is up
ping:
	@./run-all uptime

ls:
	@./run-all ls -la "~"

# Reboot machines
restart-all:
	@./run-all -sudo -P shutdown -r now

ports:
	@./run-all -sudo netstat -ntulp
