#!/bin/sh
echo "Parsing mailing list $1\n"
mlstats --backend=mailman --db-name=mlstats --db-user=root --db-password=5tartQu3ry1ng! $1
echo "\nDone.\n"
