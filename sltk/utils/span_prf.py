#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
1. extract spans from labels in a sentence
2. calculate prf
'''

def get_span(sent_labels, id2label_dict):
    """
    get success answer spans in a sequence
    :param pred_label: ndarray !NOTE: the span is 前闭后开
    :return: list of tuple spans
    """
    span = []
    for i, word_label_id in enumerate(sent_labels):
        if id2label_dict[word_label_id] == 'S':
            if i + 1 == len(sent_labels):
                span.append((i, i + 1))
            elif id2label_dict[sent_labels[i + 1]] == 'O':
                span.append((i, i + 1))
            continue
        if id2label_dict[word_label_id] == 'B':
            if i + 1 == len(sent_labels): # 判断是不是最后一个字
                continue
            elif id2label_dict[sent_labels[i + 1]] == 'E': # 判断是不是BE
                span.append((i, i + 2))
            elif id2label_dict[sent_labels[i + 1]] == 'I': # 判断是不是BI...IE
                j = i
                while j + 1 != len(sent_labels) and id2label_dict[sent_labels[j + 1]] == 'I':
                    j += 1
                if j + 1 != len(sent_labels) and id2label_dict[sent_labels[j + 1]] == 'E':
                    span.append((i, j+2))
    return span

def get_span_nodict(sent_labels):
    """
    get success answer spans in a sequence
    :param pred_label: ndarray !NOTE: the span is 前闭后开
    :return: list of tuple spans
    """
    span = []
    for i, word_label in enumerate(sent_labels):
        if word_label == 'S':
            if i + 1 == len(sent_labels):
                span.append((i, i + 1))
            elif sent_labels[i + 1] == 'O':
                span.append((i, i + 1))
            continue
        if word_label == 'B':
            if i + 1 == len(sent_labels): # 判断是不是最后一个字
                continue
            elif sent_labels[i + 1] == 'E': # 判断是不是BE
                span.append((i, i + 2))
            elif sent_labels[i + 1] == 'I': # 判断是不是BI...IE
                j = i
                while j + 1 != len(sent_labels) and sent_labels[j + 1] == 'I':
                    j += 1
                if j + 1 != len(sent_labels) and sent_labels[j + 1] == 'E':
                    span.append((i, j+2))
    return span

def em_recall(g_spans, p_spans):
    """
    calculate em recall
    :param g_spans: list of gold span tuples
    :param p_spans: list of pred span tuples
    :return: a list of em_recall value for each gold span. each value in output list corresponds to one gold answer span.
    """
    anss_l = [0] * len(g_spans)
    for i, g in enumerate(g_spans):
        for p in p_spans:
            if g == p:
                anss_l[i] = 1
                break
    return anss_l

def bin_recall(g_spans, p_spans):
    anss_l = [0] * len(g_spans)
    for i, g in enumerate(g_spans):
        for p in p_spans:
            if set(range(g[0], g[1])).intersection(set(range(p[0], p[1]))):
                anss_l[i] = 1
                break
    return anss_l

def prop_recall(g_spans, p_spans):
    anss_l = [0] * len(g_spans)
    for i, g in enumerate(g_spans):
        g_set = set(range(g[0], g[1]))
        for p in p_spans:
            overlap_num = len(set(range(p[0], p[1])).intersection(g_set))
            prop_r = 1.0 * overlap_num / len(g_set)
            if prop_r > anss_l[i]:
                anss_l[i] = prop_r
    return anss_l

def em_precision(g_spans, p_spans):
    """
    calculaye em_precision
    :param g_spans: list of gold spans in tuple
    :param p_spans: list of pred spans in tuple
    :return: list of precision value for each pred span in p_spans
    """
    anss_l = [0] * len(p_spans)
    for i, p in enumerate(p_spans):
        for g in g_spans:
            if g == p:
                anss_l[i] = 1
                break
    return anss_l

def bin_precision(g_spans, p_spans):
    anss_l = [0] * len(p_spans)
    for i, p in enumerate(p_spans):
        for g in g_spans:
            if set(range(g[0], g[1])).intersection(set(range(p[0], p[1]))):
                anss_l[i] = 1
                break
    return anss_l

def prop_precision(g_spans, p_spans):
    anss_l = [0] * len(p_spans)
    for i, p in enumerate(p_spans):
        p_set = set(range(p[0], p[1]))
        for g in g_spans:
            overlap_num = len(set(range(g[0], g[1])).intersection(p_set))
            prop_r = 1.0 * overlap_num / len(p_set)
            if prop_r > anss_l[i]:
                anss_l[i] = prop_r
    return anss_l