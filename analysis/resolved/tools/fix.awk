BEGIN {
    size = 0
    first = 1
}

{
    if (size + $1 <= 8000) {
        size = size + $1
        if (first) {
            files = $2
            first = 0
        }
        else {
            files = files " " $2
        }
    }
    else {
        print files
        size = $1
        files = $2
    }
}

END {
    print files
}
