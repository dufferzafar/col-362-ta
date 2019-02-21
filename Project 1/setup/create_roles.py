import psycopg2
import sys

sys.path.append("..")
from config import SERVERS, CREDENTIALS
from utils import group_IP

QUERY = """
    REVOKE USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public FROM {group};
    REVOKE SELECT ON ALL TABLES IN SCHEMA public FROM {group};
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
    for group in CREDENTIALS.keys():
        conn = connect(group_IP(group))
        query = QUERY.format(group=group, pswd=CREDENTIALS[group])
        print(query)
        conn.autocommit = True
        conn.cursor().execute("DROP DATABASE IF EXISTS {group};".format(group=group))
        conn.commit()
        conn.cursor().execute(query)
        conn.commit()
        conn.close()
