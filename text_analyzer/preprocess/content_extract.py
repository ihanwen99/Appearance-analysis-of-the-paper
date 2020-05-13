# -*- coding:utf-8 -*-

import os
import re
from tree import TextTree
import argparse

def contain_email(text):
    return re.search('@.+?\.',text)

def is_disciption(text):
    if re.match('figure \d:',text.lower()):
        return True
    if re.match('table \d:',text[:9].lower()):
        return True
    if re.match('stage \d:',text[:9].lower()):
        return True
    if re.match('algorithm \d:',text[:9].lower()):
        return True
    return False

def is_subtitle(para,level=0):
    parse_pattern = '(\d\.?)+? [A-Z]' if level == 0 else '(\d\.?)'*level + ' [A-Z]'
    if para.lower().strip() == 'abstract' and level <= 1:
        return True
    elif re.match(parse_pattern,para):
        return True
    return False

def is_too_short(para):
    return len(re.split(' +',para)) <= 5


def basic_paraphrase(text):
    paras = []
    current_para = ''
    for sep in re.split('\n', text):
        sep = sep.strip()
        if is_disciption(sep):
            continue
        if sep == '' and current_para.strip() != '':
            current_para = re.sub('(\- )|(\ufb01)','',current_para)
            current_para = re.sub(' +',' ',current_para)
            paras.append(current_para.strip())
            current_para = ''
        else:
            current_para += sep.strip()+' '
    return paras


def parse_title(paragraphs):
    title = ''
    is_second_line = False
    for i in paragraphs:
        if re.search('IEEE.+?Conference',i):
            continue
        if re.search('([A-Z]\.)|†|¨|ˇ|´',i):
            break
        if contain_email(i):
            continue
        if is_second_line:
            if re.search('([A-Z][a-z]+? and [A-Z][a-z]+?)|:|(University)|,|\*|∗|( [B-Z] )', i):
                break
        if i.lower().strip() == 'abstract':
            break

        title += i+' '
        if is_second_line:
            break
        else:
            is_second_line = True

    title = title.strip()
    if title=='' or (not re.match('[A-Za-z]',title[0])):
        return None

    return title

def construct_tree(paragraphs):
    title = parse_title(paragraphs)
    if title is None:
        return None
    print(title)
    idx = 0
    while idx < len(paragraphs):
        if paragraphs[idx].lower() == 'abstract':
            break
        idx += 1
    if idx == len(paragraphs):
        return None

    subtitles = []
    new_para = paragraphs[idx:]
    for i,para in enumerate(new_para):
        if is_subtitle(para,1):
            subtitles.append(i)
    subtitles.append(len(new_para))
    if len(subtitles) <= 2:
        return None

    root = TextTree(title)
    sub_part = []
    for bg,_ in enumerate(subtitles[:-1]):
        sub_node = parse_section(new_para[subtitles[bg]:subtitles[bg+1]],1)
        sub_part.append(sub_node)
    root.add_child(sub_part)
    return root


def parse_section(paragraph,level):
    node = TextTree(paragraph[0])
    subtitles = []
    new_para = paragraph[1:]
    for i,para in enumerate(new_para):
        if is_subtitle(para,level+1):
            subtitles.append(i)
    subtitles.append(len(new_para))
    if len(subtitles) <= 2:
        sub_part = parse_paragraph(new_para)
    else:
        sub_part = []
        for idx, _ in enumerate(subtitles[:-1]):
            sub_node = parse_section(new_para[subtitles[idx]:subtitles[idx + 1]], level+1)
            sub_part.append(sub_node)

    node.add_child(sub_part)
    return node

def parse_paragraph(para):
    para_list = []
    for i in para:
        if is_too_short(i):
            continue
        elif 'A'<= i[0] <= 'Z':
            para_list.append(TextTree(i))
        elif 'a'<= i[0] <= 'z' and para_list!=[]:
            para_list[-1].content += i
        else:
            pass
    return para_list


if __name__=='__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--in_path', default="./dataset/train/conference", type=str)
    arg_parser.add_argument('--out_path', default="./../dataset/train/conference", type=str)
    args = arg_parser.parse_args()
    os.makedirs(args.out_path,exist_ok=True)

    cnt = 0
    suc = 0
    for paper in os.listdir(args.in_path):
        with open(os.path.join(args.in_path, paper), 'r', encoding='utf-8') as f:
            original_txt = f.read()

        paragraphs = basic_paraphrase(original_txt)

        tree = construct_tree(paragraphs)
        cnt += 1
        if tree is not None:
            suc +=1
            tree.save(os.path.join(args.out_path,paper[:-4]+'.json'))
    print(f'{suc}/{cnt}')




