gzip -cd $1 | grep -A1 --no-group-separator "@HWI-" | tr "#" ":" | cut -d: -f '4 5' | tee cut_data | awk -FN -v len=$2 -v deleted_data=deleted_data -f cut.awk > clear_data;


# # if
# #     [ -f deleted_data ];
# # then
# #     rm deleted_data;
# # fi;

# grep -A1 --no-group-separator "@HWI-" data_file > filtered_data;

# cat filtered_data | tr "#" ":" | cut -d: -f '4 5' > cut_data;

# # cut -d# -f1 cut_data_temp | tr "N" " " > cut_data;

# # cut -d# -f1 cut_data_temp > cut_data;

# # touch deleted_data;
# awk -FN -v len=$2 -v deleted_data_file=deleted_data -f cut.awk cut_data > clear_data;

# # awk -f '{NR % 2 == 0 print cut filtered_data -d: -f "4 5" > cut_data else }'

# rm data_file;
# rm filtered_data;

# # rm filtered_data_temp;
# # rm cut_data_temp;

# # sed 'N;s/\n/ - /' new_R39-L6-READ2-Sequences.txt > temp_output.txt 
# # grep -v -A1 ":1101:" new_R39-L6-READ2-Sequences.txt > temp_output2.txt
# # sed '/HWI-ST591/d' temp_output2.txt > output2.txt
# # rm temp_output2.txt
