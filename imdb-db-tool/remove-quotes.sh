echo "Removing invalid characters from the tables"

sed -i '' 's/\\"//g' tables/aka_name.csv
sed -i '' 's/\\,//g' tables/aka_name.csv

sed -i '' 's/\\"//g' tables/char_name.csv
sed -i '' 's/\\,//g' tables/char_name.csv

sed -i '' 's/\\"//g' tables/company_type.csv
sed -i '' 's/\\,//g' tables/company_type.csv

sed -i '' 's/\\"//g' tables/keyword.csv
sed -i '' 's/\\,//g' tables/keyword.csv

sed -i '' 's/\\"//g' tables/movie_companies.csv
sed -i '' 's/\\,//g' tables/movie_companies.csv

sed -i '' 's/\\"//g' tables/movie_keyword.csv
sed -i '' 's/\\,//g' tables/movie_keyword.csv

sed -i '' 's/\\"//g' tables/person_info.csv
sed -i '' 's/\\,//g' tables/person_info.csv

sed -i '' 's/\\"//g' tables/aka_title.csv
sed -i '' 's/\\,//g' tables/aka_title.csv

sed -i '' 's/\\"//g' tables/comp_cast_type.csv
sed -i '' 's/\\,//g' tables/comp_cast_type.csv

sed -i '' 's/\\"//g' tables/complete_cast.csv
sed -i '' 's/\\,//g' tables/complete_cast.csv

sed -i '' 's/\\"//g' tables/kind_type.csv
sed -i '' 's/\\,//g' tables/kind_type.csv

sed -i '' 's/\\"//g' tables/movie_info.csv
sed -i '' 's/\\,//g' tables/movie_info.csv

sed -i '' 's/\\"//g' tables/movie_link.csv
sed -i '' 's/\\,//g' tables/movie_link.csv

sed -i '' 's/\\"//g' tables/role_type.csv
sed -i '' 's/\\,//g' tables/role_type.csv

sed -i '' 's/\\"//g' tables/cast_info.csv
sed -i '' 's/\\,//g' tables/cast_info.csv

sed -i '' 's/\\"//g' tables/company_name.csv
sed -i '' 's/\\,//g' tables/company_name.csv

sed -i '' 's/\\"//g' tables/info_type.csv
sed -i '' 's/\\,//g' tables/info_type.csv

sed -i '' 's/\\"//g' tables/link_type.csv
sed -i '' 's/\\,//g' tables/link_type.csv

sed -i '' 's/\\"//g' tables/movie_info_idx.csv
sed -i '' 's/\\,//g' tables/movie_info_idx.csv

sed -i '' 's/\\"//g' tables/name.csv
sed -i '' 's/\\,//g' tables/name.csv

sed -i '' 's/\\"//g' tables/title.csv
sed -i '' 's/\\,//g' tables/title.csv
