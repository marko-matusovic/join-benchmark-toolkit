# Download the tgz file
rm imdb.tgz
wget https://homepages.cwi.nl/~boncz/job/imdb.tgz

# Clean up the unpacking destination
rm -rf tables
mkdir tables

# Unpack the tgz file
tar zxvf imdb.tgz -C tables

./remove-quotes.sh

# Clean up
rm -rf tables/schematext.sql
rm imdb.tgz
