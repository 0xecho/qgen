import requests
from lxml import etree
from tempfile import NamedTemporaryFile

def get_input(nid):
    url = "https://www.udebug.com/udebug-custom-get-selected-input-ajax"
    headers = {
        "sec-ch-ua": "Chromium;v=94, Google Chrome;v=94, ;Not A Brand;v=99",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "content-type": "application/x-www-form-urlencoded",
        "x-requested-with": "XMLHttpRequest",
        "sec-ch-ua-mobile": "?0",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        "sec-ch-ua-platform": "Linux",
        "origin": "https://www.udebug.com",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://www.udebug.com/UVa/10035",
        "accept-language": "en-US,en;q=0.9",
        "cookie": "has_js=1; _ga=GA1.2.804459500.1646560045; _gid=GA1.2.1131252605.1646560045; _gat=1"
    }
    data = {
        "input_nid": nid
    }
    response = requests.post(url, headers=headers, data=data)
    input_value = response.json()["input_value"].strip()
    return input_value

def get_output(uva_id, problem_nid, form_build_id, input_data):
    url = f"https://www.udebug.com/UVa/{uva_id}"
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "content-type": "application/x-www-form-urlencoded",
        "sec-ch-ua": "\"Chromium\";v=\"94\", \"Google Chrome\";v=\"94\", \";Not A Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Linux\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1"
    }
    data = f"problem_nid={problem_nid}&input_data={input_data}&node_nid=&op=Get+Accepted+Output&output_data=&user_output=&form_build_id={form_build_id}&form_id=udebug_custom_problem_view_input_output_form"
    response = requests.post(url, headers=headers, data=data)
    response_etree = etree.HTML(response.text)
    output_data = response_etree.xpath("//textarea[@id='edit-output-data']/text()")[0].strip()
    return output_data

def fetch_test_cases(UVa_id):
    """
        Fetch test cases from uDebug.
        Input: UVA Problem ID
        Output: A dict with input_testcases and output_testcases
        The test cases are saved in a temporary folder
    """
    url = "https://www.udebug.com/UVa/{}".format(UVa_id)
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-language": "en-US,en;q=0.9",
        "sec-ch-ua": "\"Chromium\";v=\"94\", \"Google Chrome\";v=\"94\", \";Not A Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Linux\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch test cases")
        return None
    response_text = response.text
    response_etree = etree.HTML(response_text)
    problem_nid = response_etree.xpath("//input[@name='problem_nid']/@value")[0]
    form_build_id = response_etree.xpath("//input[@name='form_build_id']/@value")[0]
    data_ids = response_etree.xpath("//a[@data-id]")
    data_ids = set([data_id.attrib["data-id"] for data_id in data_ids])
    for nid in data_ids:
        input_data = get_input(nid)
        output_data = get_output(UVa_id, problem_nid, form_build_id, input_data)
        temp_input_file = NamedTemporaryFile(mode="w+", suffix=".in", delete=False)
        temp_output_file = NamedTemporaryFile(mode="w+", suffix=".out", delete=False)
        temp_input_file.write(input_data)
        temp_output_file.write(output_data)
        temp_input_file.close()
        temp_output_file.close()
        yield temp_input_file.name, temp_output_file.name