// input string
params.str = 'Hello world!'

// process that splits the input string into separate letters and writes them into files
process splitLetters {
    output:
    file 'chunk_*' into letters

    """
    printf '${params.str}' | split -b 6 - chunk_
    """
}

// process that reads chunks and builds it up into a phrase
process convertToUpper {
    input:
    file x from letters.flatten()

    output:
    stdout result

    """
    cat $x | tr '[a-z]' '[A-Z]'
    """
}

// view the contents of the convertToUpper process output
result.view { it.trim() }
