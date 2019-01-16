#!/bin/bash

. common_script.sh

set_grade() {
    echo "#!/bin/bash" >> vpl_execution
    echo "echo 'Grade :=>>$1'" >> vpl_execution
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
psql -t -h "$ipaddr" -p 5432 -U vpl_user -d vpl_db -f preamble.sql

# Run queries
for part in part-*.sql; do
    psql -t -h "$ipaddr" -p 5432 -U vpl_user -d vpl_db -f "$part" > "$part.out"
done

# Run cleanup
psql -t -h "$ipaddr" -p 5432 -U vpl_user -d vpl_db -f cleanup.sql

# Match output with model solution
grade=0

# Unzip model solutions: part-10.sql.model
ls
unzip model.zip

for part in part-*.sql; do
    # parts-13.sql.out parts-13.sql.model
    diff -quB "$part.out" "$part.model"

    # if diff says zero, +5
    if [ $? -eq 0 ]; then
        grade=$((grade+4))
    fi
done

set_grade grade;
