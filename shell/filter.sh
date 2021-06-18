gzip -cd $1 | awk -F':' -f cut.awk -v patterns_file=$2 > output;
# gzip -cd $1 | grep -v -A1 -f grep_patterns > output;
