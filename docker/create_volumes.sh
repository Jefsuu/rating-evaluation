declare -a StringArray=("postgresql_data"
                        
)

for val in ${StringArray[@]};
do mkdir -p volumes/$val
done


for val in ${StringArray[@]};
do sudo chown 1001:1001 volumes/$val
done