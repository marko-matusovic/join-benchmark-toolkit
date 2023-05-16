echo "Removing from aka_name.csv"
sed -i '' 's/\\\"//g' tables/aka_name.csv        
echo "Removing from char_name.csv"
sed -i '' 's/\\\"//g' tables/char_name.csv       
echo "Removing from company_type.csv"
sed -i '' 's/\\\"//g' tables/company_type.csv    
echo "Removing from keyword.csv"
sed -i '' 's/\\\"//g' tables/keyword.csv         
echo "Removing from movie_companies.csv"
sed -i '' 's/\\\"//g' tables/movie_companies.csv 
echo "Removing from movie_keyword.csv"
sed -i '' 's/\\\"//g' tables/movie_keyword.csv   
echo "Removing from person_info.csv"
sed -i '' 's/\\\"//g' tables/person_info.csv
echo "Removing from aka_title.csv"
sed -i '' 's/\\\"//g' tables/aka_title.csv       
echo "Removing from comp_cast_type.csv"
sed -i '' 's/\\\"//g' tables/comp_cast_type.csv  
echo "Removing from complete_cast.csv"
sed -i '' 's/\\\"//g' tables/complete_cast.csv   
echo "Removing from kind_type.csv"
sed -i '' 's/\\\"//g' tables/kind_type.csv       
echo "Removing from movie_info.csv"
sed -i '' 's/\\\"//g' tables/movie_info.csv      
sed -i '' 's/\\,/",/g' tables/movie_info.csv
echo "Removing from movie_link.csv"
sed -i '' 's/\\\"//g' tables/movie_link.csv      
echo "Removing from role_type.csv"
sed -i '' 's/\\\"//g' tables/role_type.csv
echo "Removing from cast_info.csv"
sed -i '' 's/\\\"//g' tables/cast_info.csv       
echo "Removing from company_name.csv"
sed -i '' 's/\\\"//g' tables/company_name.csv    
echo "Removing from info_type.csv"
sed -i '' 's/\\\"//g' tables/info_type.csv       
echo "Removing from link_type.csv"
sed -i '' 's/\\\"//g' tables/link_type.csv       
echo "Removing from movie_info_idx.csv"
sed -i '' 's/\\\"//g' tables/movie_info_idx.csv  
echo "Removing from name.csv"
sed -i '' 's/\\\"//g' tables/name.csv            
echo "Removing from title.csv"
sed -i '' 's/\\\"//g' tables/title.csv

echo "Complete"