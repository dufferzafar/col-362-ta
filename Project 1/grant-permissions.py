import subprocess
from utils import group_IP


def run_query(ip, db, query, show_html=False):
    cmd = 'PGPASSWORD="vpl-362" psql -qAt -h {ip} -d {db} -U "postgres" -c "{query}"'.format(ip=ip, db=db, query=query)
    try:
        msg = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        status = 0
    except subprocess.CalledProcessError as err:
        msg = err.output
        status = err.returncode
    msg = msg.decode("utf-8")
    return status, msg


def change_ownership(group):
    print("\nChanging Ownerships...")
    ip = group_IP(group)

    print("\nTables...")
    q_tables = "select tablename from pg_tables where schemaname = 'public';"
    status, tables = run_query(ip, group, q_tables)
    if not status:
        tables = [each.strip() for each in tables.split()]
        for each in tables:
            query = "alter table \"{}\" owner to {};".format(each, group)
            status, output = run_query(ip, group, query)
            print("\tQuery:{}\n\tStatus:{}\n\tOutput:{}\n\n".format(query, status, output))

    print("\nSequences...")
    q_seq = "select sequence_name from information_schema.sequences where sequence_schema = 'public';"
    status, sequences = run_query(ip, group, q_seq)
    if not status:
        sequences = [each.strip() for each in sequences.split()]
        for each in sequences:
            query = "alter sequence \"{}\" owner to {};".format(each, group)
            status, output = run_query(ip, group, query)
            print("\tQuery:{}\n\tStatus:{}\n\tOutput:{}\n\n".format(query, status, output))

    print("\nViews...")
    q_views = "select table_name from information_schema.views where table_schema = 'public';"
    status, views = run_query(ip, group, q_views)
    if not status:
        views = [each.strip() for each in views.split()]
        for each in views:
            query = "alter view \"{}\" owner to {};".format(each, group)
            status, output = run_query(ip, group, query)
            print("\tQuery:{}\n\tStatus:{}\n\tOutput:{}\n\n".format(query, status, output))


def give_permissions(group):
    print("\nGiving Permissions...")
    queries = [
        "GRANT ALL ON ALL TABLES IN schema public TO {group};",
        "GRANT ALL ON ALL SEQUENCES IN schema public TO {group};",
        "GRANT ALL ON ALL FUNCTIONS IN schema public TO {group};",
        "ALTER DATABASE {group} OWNER TO {group};"
    ]

    ip = group_IP(group)
    for query in queries:
        query = query.format(group=group)
        status, output = run_query(ip, group, query)
        print("\tQuery:{}\n\tStatus:{}\n\tOutput:{}\n\n".format(query, status, output))


if __name__ == '__main__':
    for i in range(35):
        group = "group_%s" % (i)
        print("User: ", group)
        give_permissions(group)
        change_ownership(group)
