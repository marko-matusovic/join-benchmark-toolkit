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

if pwd | grep -q "/Users/marko-mac/"; then
    echo "Running on marko's macbook"
    # Works only on my laptop (macs are weird)
    # Removing invalid characters from the tables
    sed -i '' 's/\\"//g' tables/*.csv
    sed -i '' 's/\\"//g' tables/*.csv
    # remove annoying lines
    sed -i '' '8718195d' tables/movie_info.csv
    sed -i '' '9810425d' tables/movie_info.csv
else
    # Works on Linux
    # Removing invalid characters from the tables
    sed -i 's/\\"//g' tables/*.csv
    sed -i 's/\\"//g' tables/*.csv
    # remove annoying lines
    sed -i '8718195d' tables/movie_info.csv
    sed -i '9810425d' tables/movie_info.csv
fi
