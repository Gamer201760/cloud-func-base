poetry export --without-hashes --format=requirements.txt > requirements.txt 
zip -9 ydb_test.zip *.txt *.py ./lib/* ./schemas/*