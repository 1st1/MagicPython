a = 'qqq{:%Y-%m-%d %H:%M:%S}www'
a = 'qqq{0:{fill}{align}16}www'




a             : source.python
=             : keyword.operator.assignment.python, source.python
              : source.python
'             : punctuation.definition.string.begin.python, source.python, string.quoted.single.single.python
qqq           : source.python, string.quoted.single.single.python
{             : constant.character.format.python, source.python, string.quoted.single.single.python
:             : constant.character.format.python, source.python, string.quoted.single.single.python, support.other.format.python
%Y-%m-%d %H:%M:%S : constant.character.format.python, source.python, string.quoted.single.single.python
}             : constant.character.format.python, source.python, string.quoted.single.single.python
www           : source.python, string.quoted.single.single.python
'             : punctuation.definition.string.end.python, source.python, string.quoted.single.single.python
a             : source.python
=             : keyword.operator.assignment.python, source.python
              : source.python
'             : punctuation.definition.string.begin.python, source.python, string.quoted.single.single.python
qqq           : source.python, string.quoted.single.single.python
{0            : constant.character.format.python, source.python, string.quoted.single.single.python
:             : constant.character.format.python, source.python, string.quoted.single.single.python, support.other.format.python
{fill}        : constant.character.format.python, source.python, string.quoted.single.single.python
{align}       : constant.character.format.python, source.python, string.quoted.single.single.python
16            : constant.character.format.python, source.python, string.quoted.single.single.python
}             : constant.character.format.python, source.python, string.quoted.single.single.python
www           : source.python, string.quoted.single.single.python
'             : punctuation.definition.string.end.python, source.python, string.quoted.single.single.python