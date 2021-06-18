{
    if (NF == 1) {
        print;
    }
    else {
        i = 0;
        max_len = 0;
        max_word = 1;
        for(i = 1; i <= NF; i++) {
            if (length($i) > max_len) {
                max_len = length($i);
                max_word = $i;
            }
        }
        print max_word;
    }
}

# '{if (NF == 1)print;else {i = 0;max_len = 0;max_word = 1;for(i = 0; i <= NF; i++) {if (length($i) > max_len) {max_len = length($i);max_word = $i;}}print max_word;}}'

# NF - кол-во полей
# NR - номер строки 
# 
