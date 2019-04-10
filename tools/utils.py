import ujson as json
import pickle

def load_txt(loadpath, loadinfo):
    with open(loadpath, 'r', encoding='utf-8') as fh:
        print(loadinfo)
        file = fh.read().splitlines()
        print('load txt done')
    return file

def save_txt(data, savepath, saveinfo):
    with open(savepath, 'w', encoding='utf-8') as f:
        print(saveinfo)
        for item in data:
            f.write("%s\n" % item)
        print('txt save done')


def loads_json(loadpath, loadinfo):
    with open(loadpath, 'r', encoding='utf-8') as fh:
        print(loadinfo)
        dataset = []
        for line in fh:
            example = json.loads(line)
            dataset.append(example)
        print('load json done')
    return dataset


def load_json(loadpath, loadinfo):
    with open(loadpath, 'r', encoding='utf-8') as fh:
        print(loadinfo)
        dataset = json.load(fh)
        print('load json done')
    return dataset


def dump_json(data, savepath, saveinfo):
    with open(savepath, 'w', encoding='utf-8') as fh:
        print(saveinfo)
        json.dump(data, fh)
        print('json save done')


def dumps_json(data, savepath, saveinfo):
    with open(savepath, 'w', encoding='utf-8') as fh:
        print(saveinfo)
        for example in data:
            fh.write(json.dumps(example) + '\n')
        print('json save done')


def dump_pickle(data, savepath, saveinfo):
    with open(savepath, 'wb') as fh:
        print(saveinfo)
        pickle.dump(data, fh)
        print('pickle save done')


def load_pickle(loadpath, loadinfo):
    with open(loadpath, 'rb') as fh:
        print(loadinfo)
        dataset = pickle.load(fh)
        print('load pickle done')
    return dataset


def get_word_span(context, wordss, spanss, start, length):
    """
    Get the word level start, stop given the character level start, stop
    :param context: raw text
    :param wordss: tokenized text in sent-word structure
    :param spanss: 2d span
    :param start: character level start
    :param length: tokens length
    :return: (sentence_idx, word_idx) start stop
    Note: start is included but stop is excluded,
    text[start:stop] will get the correct results
    also applicable to the returned value
    """
    # spanss = get_2d_spans(context, wordss)
    stop = start + length
    idxs = []
    for sent_idx, spans in enumerate(spanss):
        for word_idx, span in enumerate(spans):
            if not (stop <= span[0] or start >= span[1]):
                idxs.append((sent_idx, word_idx))

    assert len(idxs) > 0, "{} {} {} {}".format(context, spanss, start, stop)
    return idxs[0], (idxs[-1][0], idxs[-1][1] + 1)


def get_2d_spans(text, tokenss):
    """
    get character level start and stop for each token
    :param text: raw text
    :param tokenss: tokenized text, with sentence-word like structure
    :return: word level start and stop
    Note: start is included but stop is excluded,
    text[start:stop] will get the correct results
    """
    spanss = []
    cur_idx = 0
    for tokens in tokenss:
        spans = []
        for token in tokens:
            if text.find(token[0], cur_idx) < 0:
                print(tokens[0])
                print("{} {} {}".format(token[0], cur_idx, text))
                raise Exception()
            cur_idx = text.find(token[0], cur_idx)
            spans.append((cur_idx, cur_idx + len(token[0])))
            cur_idx += len(token[0])
        spanss.append(spans)
    return spanss