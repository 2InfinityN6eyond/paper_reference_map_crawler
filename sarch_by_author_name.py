
import json

from containers import Institution, Author, Paper, Expertise
from google_schorlar_sercher import GoogleScharlarSearcher

if __name__ == "__main__" :

    # read from file if file is available.
    institution_dict = {}
    expertise_dict = {}
    whole_author_list = []
    whole_paper_dict = {}

    INSTITUTION_FILE_PATH = "./institution_dict.json"
    if os.path.exists(INSTITUTION_FILE_PATH) :
        with open(INSTITUTION_FILE_PATH, "r") as f :
            institution_dict_raw = json.load(f)
        for k, v in institution_dict_raw.items() :
            institution_dict[k] = Institution(**v)

    EXPERTISE_FILE_PATH = "./expertise_dict.json"
    if os.path.exists(EXPERTISE_FILE_PATH) :
        with open(EXPERTISE_FILE_PATH, "r") as f :
            expertise_dict_raw = json.load(f)
        for k, v in expertise_dict_raw.items() :
            expertise_dict[k] = Expertise(**v)

    AUTHOR_FILE_PATH = "./author_list.json"
    if os.path.exists(AUTHOR_FILE_PATH) :
        with open(AUTHOR_FILE_PATH, "r") as f :
            author_list_raw = json.load(f)
        for author in author_list_raw :
            whole_author_list.append(Author(**author))

    WHOLE_PAPER_FILE_PATH = "./whole_paper_dict.json"
    if os.path.exists(WHOLE_PAPER_FILE_PATH) :
        with open(WHOLE_PAPER_FILE_PATH, "r") as f :
            whole_paper_dict = json.load(f)
        for k, v in whole_paper_dict.items() :
            whole_paper_dict[k] = Paper(**v)

    
    AUTHOR_NAME_LIST_FILE_PATH = "./author_name_list.json"
    with open(AUTHOR_NAME_LIST_FILE_PATH, "r") as f :
        author_name_list = json.load(f)

    author_name_to_append_list = author_name_list

    pre_existing_author_name_list = list(map(lambda author : author.name, whole_author_list))
    author_name_to_append_list = list(filter(lambda name : name not in pre_existing_author_name_list, author_name_to_append_list))

    