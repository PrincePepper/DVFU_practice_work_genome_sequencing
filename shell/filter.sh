gzip -cd file.gz > data_file;

grep -A1 "@HWI" data_file > filtered_data;

rm data_file;


# sed 'N;s/\n/ - /' new_R39-L6-READ2-Sequences.txt > temp_output.txt 
# grep -v -A1 ":1101:" new_R39-L6-READ2-Sequences.txt > temp_output2.txt
# sed '/HWI-ST591/d' temp_output2.txt > output2.txt
# rm temp_output2.txt
