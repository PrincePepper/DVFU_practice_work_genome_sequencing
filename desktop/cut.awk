BEGIN {
    k = 3;
    i = 0;
    while ((getline line < patterns_file) > 0) {
        input_patterns[i] += line;
        i++;
    }
    close(patterns_file);
    for (i in input_patterns) patterns[input_patterns[i]] = "";
}
{
    if (NR % 4 == 1 && !($3 in patterns)) {
        k = 0;
        print;
    }
    else {
        if (k < 3) print;
        k++;
    }
}