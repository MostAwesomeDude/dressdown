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

grammar = makeGrammar(g, {"t": t})
