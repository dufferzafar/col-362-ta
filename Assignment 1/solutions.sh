
cd "$1"

python3 ../checker.py solutions.sql

if [ $? -ne 0 ]; then exit; fi;

echo -e "\nRunning PREAMBLE queries"
psql -t -h vpl1 -p 5432 -U vpl_user -d vpl_db -f preamble.sql > /dev/null

for part in $(seq 1 25); do
    echo -e "\nRunning queries for Part $part"
    psql -t -h vpl1 -p 5432 -U vpl_user -d vpl_db -f "part-$part.sql" > "part-$part.model"
done;

echo -e "\nRunning CLEANUP queries"
psql -t -h vpl1 -p 5432 -U vpl_user -d vpl_db -f cleanup.sql > /dev/null
