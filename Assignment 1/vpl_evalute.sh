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
tar --overwrite -xf model.old.tar

# Match all parts
for part in $(seq 1 25); do

    # Part 24 is handled separately
    if [ $part -eq 24 ]; then

        # Some students have printed journals with 0 impact factor
        # While others have not, so we only check one row
        # ijet journal should have 0.125 impact factor
        part24=$(grep "ijet" "part-$part.out" | cut -d"|" -f 2 | grep -c "0\.125")
        if [ $part24 -eq 1 ]; then
            grade=$((grade+2))
        else
            echo "Part $part is wrong."
        fi

    else

        diff -qwB "part-$part.out" "part-$part.model" > /dev/null 2>&1
        error1=$?

        diff -qwB "part-$part.out" "part-$part.old.model" > /dev/null 2>&1
        error2=$?

        if [ $error1 -eq 0 -o $error2 -eq 0 ]; then
            grade=$((grade+2))
        else
            echo "Part $part is wrong."
        fi

    fi

done

set_grade $grade;
