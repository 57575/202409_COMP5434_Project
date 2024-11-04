# %%
import nltk
import glob
import json
import paper_schema


class NltkTokenizer:
    __directory_path = ""
    __files = []

    def run(self):
        self.__open_all_files("*.json")
        paper = self.__read_json(self.__files[0])


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
            dir = self.__directory_path + "/" + file_type
            files = glob.glob(dir)
            self.__files = files
        else:
            raise ValueError("empty directory path or file type")

    def set_directory_path(self, directory_path: str):
        self.__directory_path = directory_path

    def get_directory_path(self):
        return self.__directory_path

    def test_nltk(self):
        sentence = (
            """At eight o'clock on Thursday morning Arthur didn't feel very good."""
        )
        tokens = nltk.word_tokenize(sentence)
        tagged = nltk.pos_tag(tokens)
        print(tokens)
        print(tagged)

    def open_nltk_downloader(self):
        nltk.download()
