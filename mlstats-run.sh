#!/bin/sh
echo "Parsing mailing list $1"
mlstats --backend=mailman --db-name=mlstats --db-user=root --db-password=5tartQu3ry1ng! $1
echo "Done"
