import os
from typing import Union

import glob
import json

import spacy
from spacy import displacy
import paper_schema


class SpacyTokenizer:
    __directory_path = ""
    __files = []
    __exist_files = []
    __nlp: any

    def __init__(self):
        a = spacy.prefer_gpu(0)
        self.__nlp = spacy.load("en_core_web_trf")

    def run(self):
        self.__open_all_files("*.json")
        self.__open_exist_files("*.json")
        s = "未处理文件数:{}".format(len(self.__files))
        print(s)
        for file_path in self.__files:
            paper = self.__read_json(file_path)
            result_words = []
            if len(paper.metadata.title) > 0:
                result_words += self.__text_tokenize(paper.metadata.title)
            if len(paper.body_text) > 0:
                result_words += self.__paragraph_tokenize(paper.body_text)
            if len(paper.abstract) > 0:
                result_words += self.__paragraph_tokenize(paper.abstract)
            if len(paper.back_matter) > 0:
                result_words += self.__paragraph_tokenize(paper.back_matter)
            self.__wirte_json(self.get_directory_path(), paper.paper_id, result_words)

    def draw_dependency_parse(self, text: str):
        doc = self.__nlp(text)
        displacy.serve(doc, style="dep")

    def __text_tokenize(self, text: str):
        result: list[str] = []
        doc = self.__nlp(text)
        for token in doc:
            result.append(token.lemma_)
        return result

    def __paragraph_tokenize(
            self,
            paragraph: Union[
                list[paper_schema.Paragraph], list[paper_schema.AbstractParagraph]
            ],
    ):
        result: list[str] = []
        for sentence in paragraph:
            # remove cite
            for cite in sentence.cite_spans:
                sentence.text = sentence.text.replace(cite.text, "", 1)
            # remove ref
            for ref in sentence.ref_spans:
                sentence.text = sentence.text.replace(ref.text, "", 1)
            doc = self.__nlp(sentence.text)
            for token in doc:
                # remove stop_words, punction and space
                if not (token.is_stop or token.is_punct or token.is_space):
                    # lemmatization
                    result.append(token.lemma_)
        return result

    def __wirte_json(self, file_path: str, file_name: str, result: list):
        file_path = file_path + "/results/" + file_name + ".json"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as json_file:
            json.dump(result, json_file)

    def __read_json(self, file_path: str):
        if self.__files:
            with open(file_path, "r") as file:
                data = json.load(file)
                paper = paper_schema.PaperSchema(**data)
                return paper
        else:
            raise ValueError("No JSON files found in the directory.")

    def __open_all_files(self, file_type: str):
        if len(self.__directory_path) > 0 and len(file_type) > 0:
            dir = self.__directory_path + "/results/" + file_type
            files = glob.glob(dir)
            self.__exist_files = files
        else:
            raise ValueError("empty directory path or file type")

    def __open_exist_files(self, file_type: str):
        if len(self.__directory_path) > 0 and len(file_type) > 0:
            dir = self.__directory_path + "/" + file_type
            files = glob.glob(dir)
            self.__files = files
        else:
            raise ValueError("empty directory path or file type")
        self.__remove_exist_files()

    def __remove_exist_files(self):
        for exist in self.__exist_files:
            name = os.path.basename(exist)
            self.__files.remove(self.get_directory_path() + "\\" + name)

    def set_directory_path(self, directory_path: str):
        self.__directory_path = directory_path

    def get_directory_path(self):
        return self.__directory_path
