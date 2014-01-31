import string
# The list of reserved words
ReservedWords = """
and
begin
Boolean
div
do
downto
else
end
false
fixed
float
for
function
if
integer
mod
not
or
procedure
program
read
repeat
string
then
true
to
until
var
while
write
writeln
"""
ReservedWords = ReservedWords.split()
 
# The list of single string tokens
SingleCharacterSymbols = """
:= :
, =
/ >=
> <=
( )
< - <>
. + ; *
"""
SingleCharacterSymbols = SingleCharacterSymbols.split()

 
IDENTIFIER_START = string.letters
IDENTIFIER_CHARS = string.letters + string.digits + "_"
INTEGER = string.digits
FIXED = string.digits + "."
FLOAT = string.digits + "." + "e" + "E" + "+" + "-"
STRING_STARTCHARS = "'" + '"'
WHITESPACE_CHARS = " \t\n"
 
# TokenTypes for special tokens and others
STRING = "String"
IDENTIFIER = "Identifier"
NUMBER = "Number"
WHITESPACE = "Whitespace"
COMMENT = "Comment"
EOF = "Eof"