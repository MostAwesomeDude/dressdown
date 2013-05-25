from parsley import makeGrammar
from terml.nodes import termMaker as t

g = """
crlf = '\r' '\n' -> "<br />"
doublecrlf = crlf crlf -> "</p><p>"
not_crlf = ~crlf anything
crlfs = doublecrlf | crlf

single_star = '*' ~'*'
double_star = '*' '*'

bold = double_star (~double_star nested_decos)+:b double_star
    -> "<b>%s</b>" % "".join(b)

italics = single_star (~single_star nested_decos)+:i single_star
    -> "<i>%s</i>" % "".join(i)

underline = '_' (~'_' nested_decos)+:u '_' -> "<u>%s</u>" % "".join(u)

greentext = crlfs:head '>' nested_decos+:body crlfs:tail
         -> '%s<span class="quote">&gt;%s</span>%s' % (head, "".join(body), tail)

decorations = bold | italics | underline

nested_decos = decorations | not_crlf

entities = greentext | crlfs | decorations

paragraphs = (entities | anything)*:l -> "<p>%s</p>" % "".join(l)
"""

grammar = makeGrammar(g, {"t": t})
