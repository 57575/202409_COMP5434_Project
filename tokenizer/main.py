# %%
import spacy_tokenizer

if __name__ == "__main__":
    directory_path = (
        "C:/Users/49871/Desktop/PolyU/Course/projects/comp5434bdc/Partial/pdf_json"
    )
    tokenizer = spacy_tokenizer.SpacyTokenizer()
    tokenizer.set_directory_path(directory_path)
    tokenizer.run()
# %%
