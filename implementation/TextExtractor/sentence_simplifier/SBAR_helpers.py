from anytree import AnyNode


def make_tree_sbar(tree, t, sent_list):
    # this fn. converts nltk tree to anytree
    if tree not in sent_list:
        ttt = AnyNode(id=str(tree.label()), parent=t)
        for tt in tree:
            make_tree_sbar(tt, ttt, sent_list)
    else:
        AnyNode(id=str(tree), parent=t)


def find_sbar(t):
    if t.id == 'SBAR':
        global sbar
        sbar = t
    for tt in t.children:
        find_sbar(tt)


def find_vp_in_sbar(t):
    if t.id == 'VP':
        global vp_sbar
        vp_sbar = t
    for tt in t.children:
        find_vp_in_sbar(tt)


def find_vp(t):
    if t.id == 'SBAR':
        return
    global f
    if t.id == 'VP' and f == True:
        global vp
        vp = t
        f = False
    for tt in t.children:
        find_vp(tt)


def find_np(t):
    if t.id == 'SBAR':
        return
    global f
    if t.id == 'NP' and f == True:
        global np
        np = t
        f = False
    for tt in t.children:
        find_np(tt)


def find_vbz(t):
    if t.id == 'SBAR':
        return
    global f
    if t.id == 'VBZ' and f == True:
        global vbz
        vbz = t.children[0].id
        f = False
    for tt in t.children:
        find_vbz(tt)


def make_sent(t):
    global simple_sentences
    if t.id in sent_list:
        simple_sentences[-1].append(t.id)
    for tt in t.children:
        make_sent(tt)
