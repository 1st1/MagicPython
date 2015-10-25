a = `\
123`
print a



a             : source.python
=             : keyword.operator.assignment.python, source.python
              : source.python
`             : invalid.illegal.operator.python, source.python
\             : separator.continuation.line.python, source.python
              : source.python
123           : constant.numeric.dec.python, source.python
`             : invalid.illegal.operator.python, source.python
print         : source.python, support.function.builtin.python
 a            : source.python
