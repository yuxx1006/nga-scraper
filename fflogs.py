# from gevent import monkey
# monkey.patch_all()
# from gevent.pywsgi import WSGIServer
from selenium import webdriver
# from selenium.webdriver import Firefox
from selenium.webdriver.chrome.options import Options
import time
from lxml import etree
from flask import Flask, request, Response
import json

#const
URL = "https://cn.fflogs.com/character/"
HEADERS = ['boss', 'best_percent', 'highest_dps', 'kills',
           'fastest', 'med', 'score', 'rank']

browser = None
app = Flask(__name__)


def get_chrome():
    # browser = webdriver.Remote(
    #     command_executor="http://39.102.87.81:4444/wd/hub",
    #     desired_capabilities=DesiredCapabilities.CHROME
    # )
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    browser = webdriver.Chrome(options=chrome_options)
    # browser = Firefox()
    return browser


# -------------- Test Routes ----------------
@app.route('/', methods=['GET'])
def home():
    return '''<h1>TEST</h1>
<p>The connection works</p>'''


@app.route('/server/<server_name>/role/<role_name>', methods=['GET', 'POST'])
def scrape_fflogs(server_name, role_name):
    # start = time.time()
    if 'region' in request.args:
        region = request.args['region']
    else:
        region = 'cn'
    if 'zone' in request.args:
        zone = request.args['zone']
    else:
        zone = '33' # default value
    if 'spec' in request.args:
        spec = request.args['spec']
    else:
        spec = ''

    global browser
    try:
        if browser is None:
            browser = get_chrome()
            print("retrieve Chrome browsers")
    except:
        raise RuntimeError('webdriver is not available.')

    browser.get(URL + "{}/{}/{}#zone={}&spec={}".format(region, server_name, role_name, zone, spec))
    time.sleep(1)
    parser = etree.HTML(browser.page_source)
    rows = parser.xpath('//table[@id="boss-table-{}"]/tbody/tr'.format(zone))
    fflogs = []
    for index, tr in enumerate(list(rows)):
        try:
            columns = []
            boss = tr.xpath('.//a[@class="Boss zone-boss-cell"]/text()')[0]
            columns.append(boss)

            cols = [col.text.replace('\n', '').replace('\t', '') for col in list(tr)]
            columns.extend(cols)
            while '' in columns:
                columns.remove('')
            data = dict(zip(HEADERS, columns))
            data['index'] = index
            fflogs.append(data)
        except Exception as e:
            raise RuntimeError("Failed to scrape data")
    # print(fflogs)
    # closing the browser window
    # browser.close()
    # print("--- % seconds ---" % (time.time() - start))
    try:
        json_response = json.dumps({'fflogs': fflogs}, indent=4, sort_keys=True, ensure_ascii=False)
    except Exception as error:
        json_response = json.dumps({'error': error})
    response = Response(json_response, content_type='application/json; charset=utf-8')
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
    response.status_code = 200
    return response

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


if __name__ == "__main__":
    # chrome driver
    browser = get_chrome()
    browser.implicitly_wait(5)
    browser.maximize_window()

    app.run(host='0.0.0.0', port=5015, debug=False, threaded=False)
    # http_server = WSGIServer(('0.0.0.0', 5015), app)
    # http_server.serve_forever()

