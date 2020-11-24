# from gevent import monkey
# monkey.patch_all()
# from gevent.pywsgi import WSGIServer
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# from selenium.webdriver import Chrome, Firefox, ActionChains
import time
from lxml import etree
from flask import Flask
import json

#const
URL = "https://cn.fflogs.com/character/cn"
HEADERS = ['boss', 'best_percent', 'highest_dps', 'kills',
           'fastest', 'med', 'score', 'rank']
app = Flask(__name__)

# -------------- Test Routes ----------------
@app.route('/', methods=['GET'])
def home():
    return '''<h1>TEST</h1>
<p>The connection works</p>'''


@app.route('/cnlogs/server/<server_name>/role/<role_name>/zone/<zone>', methods=['GET','POST'])
def scrape_page(server_name, role_name, zone):
    start = time.time()
    browser = webdriver.Remote(
        command_executor="http://localhost:4444/wd/hub",
        desired_capabilities=DesiredCapabilities.CHROME
    )
    # browser = Firefox()
    browser.implicitly_wait(1)
    browser.maximize_window()

    browser.get(URL + "/{}/{}#zone={}".format(server_name, role_name, zone))
    time.sleep(2)
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
    print(fflogs)
    # closing the browser window
    browser.close()
    print("--- % seconds ---" % (time.time() - start))
    try:
        return json.dumps({'fflogs': fflogs}, indent=4, sort_keys=True, ensure_ascii=False)
    except Exception as error:
        return json.dumps({'error': error})


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5015, debug=True)
    # http_server = WSGIServer(('0.0.0.0', 5015), app)
    # http_server.serve_forever()
