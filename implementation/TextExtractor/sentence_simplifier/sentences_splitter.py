import nltk
from nltk.parse import stanford
from nltk.tree import ParentedTree
from TextExtractor.svo_extractor import get_entities


def pos_tag(tokenized_sent):
    return nltk.pos_tag(tokenized_sent)


def has_conj(tagged_sent):
    cc_list = [('and', 'CC'), ('but', 'CC')]
    for cc_pair in cc_list:
        if cc_pair in tagged_sent:
            return True
    return False


def split_needed(sent_list):
    for sent in sent_list:
        if has_conj(pos_tag(tokenize(sent))):
            return True
    return False


def split_util(sent):
    cc_list = [('and', 'CC'), ('but', 'CC')]
    for cc_pair in cc_list:
        if cc_pair in pos_tag(tokenize(sent)):
            return split(sent, cc_pair)
    return sent


def rem_dup(list):
    final = []
    for item in list:
        if item not in final:
            final.append(item)
    return final


def simplify(sent):
    initial = [sent]
    final = []

    while (split_needed(initial)):
        final = []
        while (initial):
            sent = initial.pop(0)
            if (split_needed([sent])):
                for split_sent in reversed(split_util(sent)):
                    final.append(split_sent)
            else:
                final.append(sent)
        initial = final.copy()

    final = rem_dup(final)
    final = list(reversed(final))

    return final


def tokenize(sent):
    tokenized_sent = nltk.word_tokenize(sent)
    if ('If') in tokenized_sent and ('then') in tokenized_sent:
        tokenized_sent.remove('If')
        tokenized_sent.insert(tokenized_sent.index('then'), 'and')
        tokenized_sent.remove('then')
    if ('because') in tokenized_sent:
        tokenized_sent.insert(tokenized_sent.index('because'), (','))  # ', 'is used
        tokenized_sent.insert(tokenized_sent.index('because') + 1, (','))
        tokenized_sent.insert(tokenized_sent.index('because'), 'and')
        tokenized_sent.remove('because')
    if ('while') in tokenized_sent:
        tokenized_sent.insert(tokenized_sent.index('while'), 'and')
        tokenized_sent.remove('while')
    if ('which') in tokenized_sent:
        first_sent = sent.split("which")[0]
        target = get_entities(first_sent)[1]
        tokenized_sent.insert(tokenized_sent.index('which'), 'and ' + target)
        tokenized_sent = [nltk.word_tokenize(token) for token in tokenized_sent]
        flat_tokenized_sent = [item for sublist in tokenized_sent for item in sublist]
        flat_tokenized_sent.remove('which')
        tokenized_sent = flat_tokenized_sent
    if ('or') in tokenized_sent:
        tokenized_sent.insert(tokenized_sent.index('or'), 'and')
        tokenized_sent.remove('or')
    if ('who') in tokenized_sent:
        while (',') in tokenized_sent:
            tokenized_sent.insert(tokenized_sent.index(','), 'and')
            tokenized_sent.remove(',')
        tokenized_sent.insert(tokenized_sent.index('who'), 'and')
        tokenized_sent.remove('who')

    return tokenized_sent


def split(sent, cc_tuple):
    tokenized_sent = tokenize(sent)
    parser = stanford.StanfordParser()
    pos_tagged = pos_tag(tokenized_sent)
    tree = next(parser.tagged_parse(pos_tagged))
    tree1 = ParentedTree.convert(tree)
    count = 0
    m = 0
    for t in tree1.subtrees():
        if t.label() == 'PP':
            count = count + 1

    index = []
    index1 = 0
    if count > 0 and (('to') not in tokenized_sent and ('washed') not in tokenized_sent) and (
            tokenized_sent.count(",") < 2):
        for i in range(len(pos_tagged) - 3):
            if (pos_tagged[i][1] == 'VBD' or pos_tagged[i][1] == 'VBZ') and pos_tagged[i + 1][1] != 'VBG' and \
                    pos_tagged[i + 3][1] != 'CC' and pos_tagged[i + 1][1] != 'NNP' and pos_tagged[i - 1][1] != 'CC':
                pos_tagged.insert(i + 1, (',', ','))

        for j in range(len(pos_tagged)):
            if pos_tagged[j][1] == 'CC':
                index.append(j)

    for t in tree1.subtrees():
        if t.label() == 'SBAR':
            m = m + 1
    if len(index) > 0 and count > 0 and m == 0:
        c = 0
        for i in range(len(index)):
            pos_tagged.insert(index[i] + c, (',', ','))
            c = c + 1
    if m > 0:
        for j in range(len(pos_tagged)):
            if pos_tagged[j][1] == 'CC':
                index1 = j

    if (index1 > 0 and m > 0) and count == 0:
        pos_tagged.insert(index1, (' ,', ','))  # ', 'is used
        pos_tagged.insert(index1 + 2, (', ', ','))  # ' ,' is used
    tree = next(parser.tagged_parse(pos_tagged))
    p_tree = ParentedTree.convert(tree)

    leaf_values = p_tree.leaves()
    parts = []
    ht_3_last_obj = []

    if cc_tuple in pos_tagged:
        leaf_index = leaf_values.index(cc_tuple[0])
        tree_location = p_tree.leaf_treeposition(leaf_index)
        parent = p_tree[tree_location[:-2]]

        if parent.height() == 3:
            # find the noun being referred to
            for subtree in reversed(list(parent.subtrees())):
                if subtree.parent() == parent:
                    if subtree.label() == 'NN' or subtree.label() == 'NNS':
                        ht_3_last_obj = subtree.leaves() + ht_3_last_obj
                        del p_tree[subtree.treeposition()]
            part = []
            for subtree in reversed(list(parent.subtrees())):
                if subtree.parent() == parent:
                    if subtree.label() != ',' and subtree.label() != 'CC':
                        part = subtree.leaves() + part
                    else:
                        parts.append(part + ht_3_last_obj)
                        part = []
                    del p_tree[subtree.treeposition()]
            parts.append(part + ht_3_last_obj)
            parent.append(ParentedTree('INSRT', ['*']))

        else:
            for subtree in reversed(list(parent.subtrees())):
                if subtree.parent() == parent:
                    # print(subtree)
                    if subtree.label() != ',' and subtree.label() != 'CC':
                        parts.append(subtree.leaves() + ht_3_last_obj)
                    del p_tree[subtree.treeposition()]
            parent.append(ParentedTree('INSRT', ['*']))

    split = []
    rem = p_tree.leaves()
    start_idx = rem.index('*')

    for part in reversed(parts):
        offset = start_idx
        r_clone = rem.copy()
        del r_clone[offset]
        for i, word in enumerate(part):
            r_clone.insert(offset + i, word)
        split.append(r_clone)

    split = [" ".join(sent) for sent in split]

    return split
