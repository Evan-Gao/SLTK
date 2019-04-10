import os
from utils import load_json, dumps_json

home = '/research/king3/ik_grp/yfgao/semi-supervised-QG/data'

train_raw = load_json(os.path.join(home, 'train_raw.json'), 'load squad train raw')
test_raw = load_json(os.path.join(home, 'test_raw.json'), 'load squad test raw')


def merge_answer_spans(data):
    # merge answer spans in the same sentence
    for article in data:
        for para in article['paragraphs']:
            answer_list = [[] for _ in range(len(para['context_processed']))]
            for qa in para['qas']:
                if 'answer_position' not in qa.keys():
                    continue
                start, end = qa['answer_position']
                if start[0] != end[0]:
                    continue
                answer_sentidx = start[0]
                answer_se = (start[1], end[1])
                if answer_se not in answer_list[answer_sentidx]:
                    answer_list[answer_sentidx].append(answer_se)
            # sort every sublist of answer_list
            answer_list_final = []
            for answer_list_i in answer_list:
                answer_list_final_i = []
                answer_list_tmp = sorted(answer_list_i, key=lambda x: x[0])
                # detect if there is any overlapped answer phrases
                pivot = 0
                for answer_pos in answer_list_tmp:
                    if answer_pos[0] < pivot:
                        continue
                    else:
                        answer_list_final_i.append(answer_pos)
                        pivot = answer_pos[1]
                answer_list_final.append(answer_list_final_i)
            para['merged_answer'] = answer_list_final
    return data


def iob_iobes(tags):
    """IOB -> IOBES
    Args:
        tags: list(str)

    Returns:
        new_tags: list(str)
    """
    new_tags = []
    for i, tag in enumerate(tags):
        if tag == 'O':
            new_tags.append(tag)
        elif tag == 'B':
            if i + 1 != len(tags) and tags[i + 1] == 'I':
                new_tags.append(tag)
            else:
                new_tags.append(tag.replace('B', 'S'))
        elif tag == 'I':
            if i + 1 < len(tags) and tags[i + 1] == 'I':
                new_tags.append(tag)
            else:
                new_tags.append(tag.replace('I', 'E'))
        else:
            raise Exception('Invalid IOB format!')
    return new_tags


def extract_feature(data):
    # extract needed features
    extracted = []
    for article in data:
        for para in article['paragraphs']:
            for sent, answer_spans in zip(para['context_processed'], para['merged_answer']):
                if len(answer_spans) == 0:
                    continue
                sent_featured = list(zip(*sent))[:3]
                answer_feature = ['O'] * len(sent_featured[0])
                for answer_pos in answer_spans:
                    answer_feature[answer_pos[0]] = 'B'
                    for i in range(answer_pos[0]+1, answer_pos[1], 1):
                        answer_feature[i] = 'I'
                answer_feature_new = iob_iobes(answer_feature)
                sent_featured.append(answer_feature_new)
                extracted.append(sent_featured)
    return extracted


train_merged_ans = merge_answer_spans(train_raw)
train_processed = extract_feature(train_merged_ans)
test_merged_ans = merge_answer_spans(test_raw)
test_processed = extract_feature(test_merged_ans)
dumps_json(train_processed, os.path.join(home, 'train_bilstmcnncrf.json'), 'saving train processed')
dumps_json(test_processed, os.path.join(home, 'test_bilstmcnncrf.json'), 'saving test processed')


print('debug')

