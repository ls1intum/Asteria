import nltk
import re
from anytree import AnyNode
from nltk.parse import stanford
from nltk.parse.stanford import StanfordParser as sp
from nltk.tree import ParentedTree

from TextExtractor.sentence_simplifier import SBAR
from TextExtractor.sentence_simplifier.SBAR_helpers import make_tree_sbar, find_sbar, find_np, find_vp, \
    find_vbz, find_vp_in_sbar, make_sent
from TextExtractor.sentence_simplifier.sentences_splitter import tokenize, pos_tag, simplify


class sentence_simplifier:
    def __init__(self):
        self.parser1 = stanford.StanfordParser()
        self.parser = sp()
        self.split = []
        self.simple_sent = []
        self.index = []
        self.index1 = 0
        self.n = 0
        self.but = 0
        self.scount = 0
        self.parts = []
        self.ht_3_last_obj = []

    def simplify_sentences(self, txt):
        sentences = nltk.sent_tokenize(txt)
        simplified_sentences = []
        for sentence in sentences:
            print(sentences.index(sentence)),
            print("ComplexSentence: " + sentence)
            tokenized_sent = tokenize(sentence)

            pos_tagged = pos_tag(tokenized_sent)
            parse_trees = self.parser.tagged_parse(pos_tagged)
            tree = next(parse_trees)
            p_tree = ParentedTree.convert(tree)

            leaf_values = p_tree.leaves()
            for i in pos_tagged:
                if ('and') in i:
                    self.n = self.n + 1

                if ('but') in i:
                    self.but = self.but + 1
            tree1 = ParentedTree.convert(tree)
            m = 0
            for t in tree1.subtrees():
                if t.label() == 'SBAR':
                    m = m + 1

            if (self.n + self.but) > 0:
                sent1 = sentence
                sent = " ".join(tokenize(sent1))
                simplified = simplify(sent)
                for i in simplified:
                    i = i.replace(" -RRB- ", "()")
                    print(f"i = {i}\n")
                    simplified_sentences.append(i)
                    i = list(i)
                    if ord(i[0]) >= 97 and ord(i[0]) <= 122:
                        i[0] = chr(ord(i[0]) - 32)
                    while i.count(",") > 0:
                        del (i[i.index(",")])
                    if (".") not in (i):
                        print("Simple sentence: " + "".join(i) + ".")
                    else:
                        print("Simple sentence: " + "".join(i))
                self.n = 0
                self.but = 0

            elif self.n == 0 and m > 0 and len(re.findall(r",", sentence)) == 0 and len(
                    re.findall(r"While", sentence)) == 0:
                try:
                    sent = sentence
                    tokenized_sent = tokenize(sent)
                    pos_tagged = nltk.pos_tag(tokenized_sent)
                    parse_trees = self.parser.tagged_parse(pos_tagged)
                    sent_list = [s for s in sent.split()]
                    tree = next(parse_trees)[0]
                    # tree.draw()
                    t = AnyNode(id='ROOT')
                    make_tree_sbar(tree, t, sent_list)
                    sbar = t
                    vp_sbar = t
                    vp = t
                    np = t
                    vbz = 'asvf'
                    find_sbar(t)
                    find_vp_in_sbar(sbar)
                    f = True
                    find_vp(t)
                    f = True
                    find_np(t)
                    f = True
                    find_vbz(t)
                    simple_sentences = []
                    simple_sentences.append([])
                    make_sent(np)
                    make_sent(vp)
                    simple_sentences.append([])
                    make_sent(np)
                    if vbz != 'asvf':
                        simple_sentences[-1].append(vbz)
                    make_sent(vp_sbar)
                    for i in simple_sentences:
                        simplified_sentences.append(i)
                        i = list(i)
                        while i.count(",") > 0:
                            i.pop(i.index(","))
                        if (".") not in (i):
                            print("Simple sentence: " + " ".join(i) + ".")
                        else:
                            print("Simple sentence: " + " ".join(i))
                except:
                    continue
            elif m > 0 and (len(re.findall(r",", sentence)) > 0 or len(re.findall(r"While", sentence)) > 0):
                try:
                    tokenized_sent = tokenize(sentence)
                    simple_sentences = SBAR.simplify(" ".join(tokenized_sent))
                    for i in simple_sentences:
                        simplified_sentences.append(i)
                        if (".") not in (i):
                            print("Simple sentence: " + i)
                        else:
                            print("Simple sentence: " + i)
                except:
                    continue
            else:
              simplified_sentences.append(sentence)
        return simplified_sentences
