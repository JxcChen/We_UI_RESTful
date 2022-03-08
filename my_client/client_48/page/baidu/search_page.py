import platform
from ..base_page import BasePage
if platform.system() == 'Windows':
    file_path = str(__file__).split("\\")[-4]
else:
    file_path = str(__file__).split("/")[-4]


class SearchPage(BasePage):
    def search_key(self, key):
        search_input = self.open_get_element(7)
        search_input.send_keys(key)
        search_button = self.open_get_element(8)
        search_button.click()
        return self

    def search_key2(self, key):
        search_input = self.open_get_loc(7)['locator']
        self.send_key(search_input, key)
        search_input = self.open_get_loc(9)['locator']
        self.click_ele(search_input)
        return self
