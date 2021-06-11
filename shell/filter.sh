clear;
gzip -cd new_R39-L6-READ2-Sequences.txt.gz > data_file;
grep -A1 "@HWI-" data_file > filtered_data_temp;
grep -v -- "--" filtered_data_temp > filtered_data;
cut -d: -f '4 5' filtered_data > cut_data_temp;
cut -d# -f1 cut_data_temp > cut_data;


# awk -f '{NR % 2 == 0 print cut filtered_data -d: -f "4 5" > cut_data else }'

# awk -f cut.awk filtered_data > cut_data

rm data_file;
rm filtered_data_temp;
rm cut_data_temp;
rm filtered_data;

# sed 'N;s/\n/ - /' new_R39-L6-READ2-Sequences.txt > temp_output.txt 
# grep -v -A1 ":1101:" new_R39-L6-READ2-Sequences.txt > temp_output2.txt
# sed '/HWI-ST591/d' temp_output2.txt > output2.txt
# rm temp_output2.txt
