# -*- coding: utf-8 -*-
import torch
import json,jsonpickle
import torch.nn as nn
import copy
import os

class TreeNode():
    def __init__(self, embedding=None, child_list=None):
        self.parent=None
        self.children = []
        if embedding is not None:
            assert isinstance(embedding, torch.Tensor), 'Node embedding should be a tensor!'
        self.embedding = embedding
        self.h = None
        self.c = None

        if child_list is not None:
            self.add_child(child_list)

    def add_child(self, node):
        if isinstance(node, TreeNode):
            if node.parent is not None:
                node = copy.deepcopy(node)
            node.parent = self
            self.children.append(node)
        elif isinstance(node, tuple) or isinstance(node, list):
            for i in node:
                self.add_child(i)
        else:
            raise ValueError(f'{type(node)} is not the acceptable copy_node type')

    def apply(self,func,*args):
        for child in self.children:
            child.apply(func,*args)
        func(self,*args)
        return self

    def clone(self):
        new_node = copy.deepcopy(self)
        return new_node

    def __repr__(self):
        return f'Node: {str(self.embedding)}'

class TextTree(TreeNode):
    def __init__(self,content='',embeddings=None,child_list=None):
        super(TextTree,self).__init__(embeddings,child_list)
        self.content = content

    def to_json_dict(self):
        return {self.content: self.children}

    def __repr__(self):
        return str(self.to_json_dict())

    def save(self, save_path):
        config_dict = jsonpickle.encode(self)
        with open(save_path,'w') as f:
            json.dump(json.loads(config_dict),f,indent=4)

    def __str__(self):
        return jsonpickle.encode(self)

    @classmethod
    def load(self, load_path):
        with open(load_path, 'r') as f:
            config_dict = f.read()
        return jsonpickle.decode(config_dict)


# from text_analyzer import tree
if __name__ == "__main__":
    root = "dataset/train"
    data = os.walk(root)
    print(data)