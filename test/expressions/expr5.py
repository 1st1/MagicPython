a = (from, a)
b = [from, b]
c = {from: {import: a}}



a             : source.python
=             : keyword.operator.assignment.python, source.python
              : source.python
(             : punctuation.parenthesis.begin.python, source.python
from          : keyword.control.flow.python, source.python
, a           : source.python
)             : punctuation.parenthesis.end.python, source.python
b             : source.python
=             : keyword.operator.assignment.python, source.python
              : source.python
[             : punctuation.definition.list.begin.python, source.python
from          : keyword.control.flow.python, source.python
, b           : source.python
]             : punctuation.definition.list.end.python, source.python
c             : source.python
=             : keyword.operator.assignment.python, source.python
              : source.python
{             : punctuation.definition.dict.begin.python, source.python
from          : keyword.control.flow.python, source.python
:             : source.python
{             : punctuation.definition.dict.begin.python, source.python
import        : keyword.control.flow.python, source.python
: a           : source.python
}             : punctuation.definition.dict.end.python, source.python
}             : punctuation.definition.dict.end.python, source.python
