// input string
params.greeting = 'Hello world!'
// explicit channel definition
// nextflow processes communicate through FIFO queues that are called channels
// it is not neccesary to set channel here an an explicit input for the process
greeting_ch = Channel.of(params.greeting)

// process that splits the input string into separate letters and writes them into files
process splitLetters { 
  input:
  val x from greeting_ch

  output:
  file 'chunk_*' into letters

  """
  printf '$x' | split -b 6 - chunk_
  """
}

// process that reads chunks and builds it up into a phrase
process convertToUpper {
  input:
  file y from letters.flatten()

  output:
  stdout into result

  """
  cat $y | tr '[a-z]' '[A-Z]'
  """
}

// view the contents of the convertToUpper process output
result.view { it.trim() }
