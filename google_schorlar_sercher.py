import os
from bs4 import BeautifulSoup

#from selenium import webdriver
import undetected_chromedriver.v2 as webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from tqdm import tqdm

class GoogleScharlarSearcher :
    BASE_URL = "https://scholar.google.com"

    def __init__(
            self,
            institution_dict = None,
            expertise_dict = None,
        ) :
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--use_subprocess")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.institution_dict = institution_dict
        self.expertise_dict = expertise_dict

        self.crossref_fetcher = CrossRefFetcher()



    def searchPaperByName(self, name) :
        self.driver.get(self.BASE_URL)
        self.driver.implicitly_wait(10)
        # search given paper name
        search = self.driver.find_element(by=By.XPATH, value='//*[@id="gs_hdr_tsi"]')
        search.send_keys(name)
        search.send_keys(Keys.RETURN)
        self.driver.implicitly_wait(10)
        # click the first paper

    def searchAuthorByName(self, name, continue_search = False, search_width = 1000) :
        """
        If continue_search is True, search every co-author until search_width
        """
        self.driver.get(self.BASE_URL)
        self.driver.implicitly_wait(10)
        # search by author name
        searcher = self.driver.find_element(by=By.XPATH, value='//*[@id="gs_hdr_tsi"]')
        searcher.send_keys(name)
        searcher.send_keys(Keys.RETURN)
        self.driver.implicitly_wait(10)

        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        author_list = soup.find_all("h4", class_="gs_rt2")

        author_list = list(map(
            lambda author : Author(
                name = author.text,
                google_schorlar_profile_url = self.BASE_URL +author.find("a")["href"],
            ),
            author_list
        ))

        print(f"authors found : {list(map(lambda author : author.name, author_list))}")
        whole_paper_dict = {}
        for author in author_list :
            author, paper_dict = self.fillAuthor(author)
            whole_paper_dict.update(paper_dict)


        if continue_search and len(author_list) < search_width :
            pass


        return author_list, whole_paper_dict

    def addInstitution(
        self,
        html_str
    ) :
        '''
        initialize Institution instance and append to
        self.instaitution_dict if not exist
        args :
            institution_html :
                expected to have name,
                google_schorlar_institution_url field
        return :
            institution name
        '''
        #institution_name = html_str.find("a").text
        institution_name = html_str.text

        if institution_name not in self.institution_dict :
            try :
                google_schorlar_institution_url = self.BASE_URL + html_str.find("a")["href"]
            except Exception as e :
                google_schorlar_institution_url = None
            homepage_url = None
            self.institution_dict[institution_name] = Institution(
                name = institution_name,
                google_scholar_url = google_schorlar_institution_url,
                homepage_url = homepage_url,
            )
        return institution_name

    def addExpertise(
        self,
        html_str_list
    ) :
        '''
        initialize Expertise instance and append to
        self.expertise_dict if not exist
        args :
            html_str_list :
                list of html_str. each elements are html str
                expected to have name,
                google_schorlar_expertise_url field
        return :
            expertise name
        '''
        expertise_name_list = []
        for html_str in html_str_list :
            expertise_name = html_str.text
            if expertise_name not in self.expertise_dict :
                google_schorlar_expertise_url = self.BASE_URL + html_str["href"]
                self.expertise_dict[expertise_name] = Expertise(
                    name = expertise_name,
                    url = google_schorlar_expertise_url,
                )
            expertise_name_list.append(expertise_name)
        return expertise_name_list

    def fillAuthor(self, author) :
        """
        fill in author instance
        args :
            author :
                expected to have name, google_schorlar_profile_url field
        """
        # load page html        
        self.driver.get(author.google_schorlar_profile_url)
        self.driver.implicitly_wait(10)
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # fill in expertise
        expertise_html_list = soup.find_all("a", class_="gsc_prf_inta")
        expertise_name_list = self.addExpertise(expertise_html_list)
        author.expertise_list = expertise_name_list

        # fill in institution
        institution_html = soup.find("div", class_="gsc_prf_il")
        try :
            institution_name = self.addInstitution(institution_html)
            author.affiliation = institution_name
        except Exception as e :
            print(e)
            print(soup)
            raise e

        paper_dict = self.makePaperDictFromAuthor(author)
        #DOI_list = list(paper_dict.keys())
        #author.paper_list = DOI_list

        return author, paper_dict
    

    def makePaperDictFromAuthor(self, author, search_width_limit = 20) :
        """
        make paper instance from author instance
        args :
            author : Author
                expected to have name, google_schorlar_profile_url field
        return :
            paper_list : list[Paper]
        """

        # load page html        
        self.driver.get(author.google_schorlar_profile_url)
        self.driver.implicitly_wait(10)
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # search papers
        # click "show more" button until it is disabled
        '''
        while True :
            load_more_button = self.driver.find_element(by=By.XPATH, value='//*[@id="gsc_bpf_more"]')
            self.driver.implicitly_wait(10)
            load_more_button.click()
            time.sleep(2)
            if load_more_button.get_property("disabled") :
                break
        '''
        # get papaer html list
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        paper_html_list = soup.find_all("tr", class_="gsc_a_tr")
        paper_html_list = paper_html_list[:search_width_limit]

        paper_list = []

        print(f"filling google schorlar metadata of papers from {author.name}...")
        with tqdm(total=len(paper_html_list)) as pbar:
            for paper_html in paper_html_list :
                google_schorlar_url = self.BASE_URL + paper_html.find("a", class_="gsc_a_at")["href"]
                title = paper_html.find("a", class_="gsc_a_at").text
                
                self.driver.get(google_schorlar_url)
                self.driver.implicitly_wait(10)
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                metadata_list = soup.find_all("div", class_="gs_scl")
                
                html_title = soup.find("a", class_="gsc_oci_title_link")

                google_schorlar_metadata = {}
                for metadata in metadata_list :
                    field = metadata.find("div", class_="gsc_oci_field").text
                    value = metadata.find("div", class_="gsc_oci_value").text
                    google_schorlar_metadata[field] = value
                

                paper = Paper(title = title, google_schorlar_metadata = google_schorlar_metadata)
                paper_list.append(paper)

                pbar.set_postfix_str(title)
                pbar.update(1)

        author.paper_title_list = list(map(lambda paper : paper.title, paper_list))


        paper_dict = {}

        for paper in paper_list :
            paper_dict[paper.title] = paper
        return paper_dict

        # query_crossref
        print(f"fetching crosserf metadata of papers from {author.name}...")
        for paper in tqdm(paper_list) :
            self.crossref_fetcher.fetchMetaDatafromTitle(paper)
            paper_dict[paper.DOI] = paper

        return paper_dict