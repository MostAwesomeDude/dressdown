# Copyright 2014 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
from unittest import TestCase

from ometa.runtime import ParseError
from terml.nodes import termMaker as t

from grammars import grammar

class TestDressdown(TestCase):

    def test_atx_h1(self):
        i = "# h1"
        o = [t.H1("h1")]
        self.assertEqual(grammar(i).dressdown(), o)

class Testgrammar(TestCase):

    def test_crlf(self):
       self.assertEqual(grammar("\r\n").crlf(), t.Break())

    def test_doublecrlf(self):
        self.assertEqual(grammar("\r\n\r\n").doublecrlf(), t.DoubleBreak())

    def test_not_crlf(self):
        self.assertEqual(grammar("a").not_crlf(), "a")

    def test_not_crlf_fail(self):
        self.assertRaises(ParseError, grammar("\r\n").not_crlf)

    def test_bold(self):
        self.assertEqual(grammar("**asdf**").bold(), t.Bold(["asdf"]))

    def test_bold_nested(self):
        self.assertEqual(grammar("**a*sd*f**").bold(),
                         t.Bold(["a", t.Italics(["sd"]), "f"]))

    def test_italics(self):
        self.assertEqual(grammar("*asdf*").italics(), t.Italics(["asdf"]))

    def test_italics_nested(self):
        self.assertEqual(grammar("*a**sd**f*").italics(),
                         t.Italics(["a", t.Bold(["sd"]), "f"]))

    def test_underline(self):
        self.assertEqual(grammar("_asdf_").underline(), t.Underline(["asdf"]))

    def test_underline_nested(self):
        self.assertEqual(grammar("_a*sd*f_").underline(),
                         t.Underline(["a", t.Italics(["sd"]), "f"]))

    def test_quote(self):
        self.assertEqual(grammar("\r\n>mfw\r\n").greentext(),
                         t.Greentext(t.Break(), "mfw", t.Break()))

    def test_paragraphs_empty(self):
        self.assertEqual(grammar("").paragraphs(), t.Paragraphs([]))

    def test_paragraphs_trivial(self):
        self.assertEqual(grammar("asdf").paragraphs(), t.Paragraphs(["asdf"]))

    def test_paragraphs_break(self):
        text = "asdf\r\njkl"
        self.assertEqual(grammar(text).paragraphs(),
                         t.Paragraphs(["asdf", t.Break(), "jkl"]))

    def test_paragraphs_multiple(self):
        text = "asdf\r\n\r\njkl"
        self.assertEqual(grammar(text).paragraphs(),
                         t.Paragraphs(["asdf", t.DoubleBreak(), "jkl"]))

    def test_paragraphs_italics(self):
        text = "*asdf*"
        self.assertEqual(grammar(text).paragraphs(),
                         t.Paragraphs([t.Italics(["asdf"])]))

    def test_paragraphs_italics_cross(self):
        text = "*as\r\n\r\ndf*"
        self.assertEqual(grammar(text).paragraphs(),
                         t.Paragraphs(["*as", t.DoubleBreak(), "df*"]))
