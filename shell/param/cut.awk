{   
    if (!(NR % 2)) {
        i = 1;
        max_len = 0;
        max_word = 1;
        for(i = 1; i <= NF; i++) {
            if (length($i) > max_len) {
                max_len = length($i);
                max_word = $i;
            }
        }
        if (length(max_word) >= len) {
            print prev;
            print max_word;
        }
        else {
            print prev > deleted_data;
            print max_word > deleted_data;
        }
    }
    else
        prev = $0;
}
