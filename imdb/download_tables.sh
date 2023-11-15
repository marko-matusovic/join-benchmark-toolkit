# Download the tgz file
wget https://homepages.cwi.nl/~boncz/job/imdb.tgz

# Clean up the unpacking destination
rm -rf tables
mkdir tables

# Unpack the tgz file
tar zxvf imdb.tgz -C tables

# Clean up
rm -rf tables/schematext.sql
rm imdb.tgz
