import GPT_API
import logging
import tiktoken
import multiprocessing
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
import requests
import Keys

enc = tiktoken.get_encoding("cl100k_base")

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

my_api_key = Keys.GOOGLE_API_KEY
my_cse_id = Keys.GOOGLE_CSE_KEY

class SearchBot:
    def __init__(self, search_input: "str"):
        self.input = search_input

    def google_search(self, search_term, api_key, cse_id, **kwargs) -> dict:
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
        return res['items']

    def _search_crop_process(self, link: dict) -> str:
        try:
            page = requests.get(link['link'])
            soup = BeautifulSoup(page.content, "html.parser")
            raw_text = soup.get_text().replace("\n", "")
            cropped = enc.decode(enc.encode(raw_text)[:4000])
        except:
            cropped = "The search has encountered an error, no page will be returned."
        print(len(cropped))
        search_test = GPT_API.GPT(
            "You are summarizeGPT. You will be given the raw text extracted from a website. You must create a summary of the core content on the page in a full and complete form. Results with no content or error messages should be ignored. Emphasize facts and statistics from the page.",
            model="gpt-3.5-turbo")
        summary = search_test.create_chat_completion(cropped)
        logging.debug(summary)
        return summary

    def search_pipeline(self) -> str:
        results = self.google_search(self.input, my_api_key, my_cse_id, num=3)
        summary_string = ""
        pool = multiprocessing.Pool(processes=3)
        website_summaries = pool.map(self._search_crop_process, results)
        for i in website_summaries:
            summary_string += (i+"\n")

        return summary_string

