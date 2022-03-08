"""
自动维护元素定位  当元素定位失败时会执行auto_get_element
"""
import json
import re

import requests
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import Levenshtein


def get_similarity_score(oldstr, newstr):
    score = Levenshtein.ratio(str(oldstr), str(newstr))
    return score


def auto_get_element(driver: Chrome, loc_dict):
    """
    自动获取更新定位方式和定位值
    """
    print("常规定位失败,开始执行自动维护")
    # 1 根据标签(tag)值尝试进行元素获取
    old_tag = loc_dict['tag']
    # 1.1 根据遍历原有标签查看存在属性  使用正则匹配
    try:
        old_id = re.findall(r'id="(.*?)"', old_tag)[0]
    except:
        old_id = None
    try:
        old_name = re.findall(r'name="(.*?)"', old_tag)[0]
    except:
        old_name = None
    try:
        old_class = re.findall(r'class="(.*?)"', old_tag)[0]
    except:
        old_class = None
    try:
        old_text = re.findall(r'>(.*?)</', old_tag)[0]
    except:
        old_text = ''
    try:
        old_value = re.findall(r'value="(.*?)"', old_tag)[0]
    except:
        old_value = ''
    try:
        old_onclick = re.findall(r'onclick="(.*?)"', old_tag)[0]
    except:
        old_onclick = None
    try:
        old_style = re.findall(r'style="(.*?)"', old_tag)[0]
    except:
        old_style = ''
    try:
        old_placeholder = re.findall(r'placeholder="(.*?)"', old_tag)[0]
    except:
        old_placeholder = None
    try:
        old_href = re.findall(r'href="(.*?)"', old_tag)[0]
    except:
        old_href = None
    try:
        old_type = re.findall(r'type="(.*?)"', old_tag)[0]
    except:
        old_type = None
    try:
        old_tag_name = re.findall(r'<(.+?) ', old_tag)[0]
    except:
        old_tag_name = re.findall(r'<(.+?)>', old_tag)[0]
    # 1.2 根据原本的tag name 获取元素集
    tag_elements = driver.find_elements(By.TAG_NAME, old_tag_name)
    # 2 全量元素集 根据标签的属性值进行打分 获取分数最高的tag
    target_tag = ''
    target_index = 0
    now_score = 0
    highest_score = 0
    # 2.1 遍历获取到的元素集
    for i in range(len(tag_elements)):
        now_score: float = 0.0
        new_id = tag_elements[i].get_attribute('id')
        new_name = tag_elements[i].get_attribute('name')
        new_class = tag_elements[i].get_attribute('class')
        new_text = tag_elements[i].get_attribute('textContent')
        new_value = tag_elements[i].get_attribute('value')
        new_onclick = tag_elements[i].get_attribute('onclick')
        new_style = tag_elements[i].get_attribute('style')
        new_href = tag_elements[i].get_attribute('href')
        new_type = tag_elements[i].get_attribute('type')
        new_placeholder = tag_elements[i].get_attribute('placeholder')
        # 2.2 对元素集的元素属性与之前获取到的数据进行对比打分
        # name相似度占比重最高 一般name一样就通过元素  id可能为动态id
        now_score += get_similarity_score(old_name, new_name)
        now_score += get_similarity_score(old_id, new_id)
        now_score += get_similarity_score(old_placeholder, new_placeholder)
        now_score += get_similarity_score(old_text, new_text)
        now_score += get_similarity_score(old_class, new_class)
        now_score += get_similarity_score(old_value, new_value)
        now_score += get_similarity_score(old_onclick, new_onclick)
        now_score += get_similarity_score(old_style, new_style)
        now_score += get_similarity_score(old_href, new_href)
        now_score += get_similarity_score(old_type, new_type)

        # 2.3 获取到评分最高的tag
        if highest_score < now_score:
            target_tag = tag_elements[i]
            target_index = i
            highest_score = now_score

    # 3 将最新的tag数据进行返回 (进行调用接口进行更新)
    loc_id = str(loc_dict['id'])
    loc_dict = {'loc_method': 'tag name',
                'element_location': old_tag_name,
                'tag': target_tag.get_attribute('outerHTML'),
                'index': target_index
                }
    res = requests.post(url='http://192.168.1.103:8001/api/open_edit_element/%s/' % loc_id, data=json.dumps(loc_dict),
                        headers={'content-type': 'application/json'})
    return target_tag
