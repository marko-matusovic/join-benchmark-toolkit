# Download the tgz file
rm imdb.tgz
wget https://homepages.cwi.nl/~boncz/job/imdb.tgz

# Clean up the unpacking destination
rm -rf tables
mkdir tables

# Unpack the tgz file
tar zxvf imdb.tgz -C tables

# Clean up
rm -rf tables/schematext.sql
rm imdb.tgz

# Removing invalid characters from the tables
sed -i 's/\\"//g' tables/*.csv
sed -i 's/\\,//g' tables/*.csv
# The command above works on Linux, on MacOS you should use the one below:
# sed -i '' 's/\\"//g' tables/*.csv
# sed -i '' 's/\\,//g' tables/*.csv
