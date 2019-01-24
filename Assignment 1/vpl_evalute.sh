#!/bin/bash

# . common_script.sh

set_grade() {
    echo "#!/bin/bash" >> vpl_execution
    echo "echo 'Grade :=>> $1'" >> vpl_execution
    chmod +x vpl_execution
}

# Test format and break into parts: part-1-25.sql
# & generates a preamble.sql & cleanup.sql file
python3 checker.py query.sql

if [ $? -ne 0 ]; then
    set_grade 0
    exit
fi

# Find IP Address of this machine
ipaddr=$(ip addr show dev ens3 | grep "inet " | perl -ne '/inet (.*)\// && print $1')

# Run preamble
echo -e "\nRunning PREAMBLE queries"
psql -t -h "$ipaddr" -p 5432 -U vpl_user -d vpl_db -f preamble.sql > /dev/null

# Run queries
for part in $(seq 1 25); do
    echo -e "\nRunning queries for Part $part"
    psql -t -h "$ipaddr" -p 5432 -U vpl_user -d vpl_db -f "part-$part.sql" > "part-$part.out"
    # cat "$part.out"
done

# Run cleanup
echo -e "\nRunning CLEANUP queries"
psql -t -h "$ipaddr" -p 5432 -U vpl_user -d vpl_db -f cleanup.sql > /dev/null

# Match output with model solution
grade=0

# Model files are already present!
tar --overwrite -xf model.tar

# Match all parts
for part in $(seq 1 25); do
    diff -qwB "part-$part.out" "part-$part.model" > /dev/null 2>&1
    error=$?
    if [ $error -eq 0 ]; then
        grade=$((grade+4))
    fi
done

set_grade $grade;
