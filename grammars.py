from parsley import makeGrammar
from terml.nodes import termMaker as t

g = """
crlf = '\r' '\n' -> t.Break()
doublecrlf = crlf crlf -> t.DoubleBreak()
not_crlf = ~crlf anything
crlfs = doublecrlf | crlf

single_star = '*' ~'*'
double_star = '*' '*'

bold = double_star (~double_star nested_decos)+:b double_star -> t.Bold(b)

italics = single_star (~single_star nested_decos)+:i single_star
       -> t.Italics(i)

underline = '_' (~'_' nested_decos)+:u '_' -> t.Underline(u)

greentext = crlfs:head '>' nested_decos+:body crlfs:tail
         -> t.Greentext(head, body, tail)

decorations = bold | italics | underline

nested_decos = decorations | not_crlf

entities = greentext | crlfs | decorations

paragraphs = (entities | anything)*:l -> t.Paragraphs(l)
"""

g = """
eol = '\r' '\n' | '\n' | '\r'
number = anything:x ?(x in "0123456789") -> x
plaintext = (letter | number | ' ')+:cs -> "".join(cs)
line = plaintext:cs eol -> cs

rest_h1 = line:l '='+ eol -> t.H1(l)
rest_h2 = line:l '-'+ eol -> t.H2(l)

atx_h1 = '#' ' ' plaintext:l '#'* -> t.H1(l)
atx_h2 = '##' ' ' plaintext:l '#'* -> t.H2(l)
atx_h3 = '###' ' ' plaintext:l '#'* -> t.H3(l)
atx_h4 = '####' ' ' plaintext:l '#'* -> t.H4(l)
atx_h5 = '#####' ' ' plaintext:l '#'* -> t.H5(l)
atx_h6 = '######' ' ' plaintext:l '#'* -> t.H6(l)

headers = rest_h1 | rest_h2 | atx_h1 | atx_h2 | atx_h3 | atx_h4 | atx_h5
        | atx_h6

markup = headers

dressdown = (markup | plaintext)*
"""

grammar = makeGrammar(g, {"t": t})
