import psycopg2
import sys

sys.path.append("..")
from config import SERVERS, CREDENTIALS

QUERY = """
    DROP USER IF EXISTS {group};
    CREATE USER {group} WITH PASSWORD \'{pswd}\';
    """


def connect(ip):
    print("Connecting to %s:5432" % (ip))
    try:
        conn = psycopg2.connect(
            user="postgres",
            host=ip,
            port="5432",
            password="vpl-362"
        )
        return conn

    except psycopg2.Error as e:
        print("Error connecting to postgres server at %s:5432" % (ip))
        return None


if __name__ == '__main__':
    conns = [connect(ip) for ip in SERVERS.values()]
    if None in conns:
        exit(1)

    for group in CREDENTIALS.keys():
        group_no = int(group.split("_")[-1])
        conn = conns[group_no % 3]

        query = QUERY.format(group=group, pswd=CREDENTIALS[group])
        print(query)
        conn.cursor().execute(query)
        conn.commit()
