import logging
import time
import sys
from browsermobproxy import Server
from browsermobproxy import Client
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.webdriver import WebDriver
from harpy.har import Har

referer = 'http://www.google.com/search?q=hei+&oq=SUP&sourceid=firefox&ie=UTF-8'
useragent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2b5) Gecko/20091204 Firefox/3.6b5 Java/1.7.0_11'
URLs = []

def run_webdriver(start_url, port, config):
    global useragent
    global referer
    urllib3_logger = logging.getLogger('urllib3')
    urllib3_logger.setLevel(logging.DEBUG)
    logging.info("Starting WebRunner")
    firefox_profile = None
    server = None
    proxy = None
    har = None
    if config.referer:
        referer = config.referer
    if config.useragent:
        useragent = config.useragent

    server = Server("lib/browsermob/bin/browsermob-proxy", {'port': port})
    server.start()
    proxy = server.create_proxy()
#    proxy = Client("localhost:8080")
    proxy.headers({'User-Agent': useragent, 'Accept-Encoding': ""})

    request_js=(
        'var referer = request.getProxyRequest().getField("Referer");'
        'addReferer(request);'
               'function addReferer(r){'
                   'if (! referer ) {'
                       'r.addRequestHeader("Referer","'+referer+'");'
                   '}'
                   'return;'
                '}')
    proxy.request_interceptor(request_js)
    if config.firefoxprofile:
        firefox_profile = FirefoxProfile(config.firefoxprofile)

    else:
        firefox_profile = FirefoxProfile()

    firefox_profile.set_preference("security.OCSP.enabled", 0)
    firefox_profile.set_preference("browser.download.folderList", 2)
    firefox_profile.set_preference("browser.download.manager.showWhenStarting", False)
    #firefox_profile.set_preference("browser.download.dir", downloadDir.toString())
    firefox_profile.set_preference("browser.helperApps.neverAsk.saveToDisk",
                                   "application/x-xpinstall;application/x-zip;application/x-zip-compressed;application/octet-stream;application/zip;application/pdf;appl\
                                   ication/msword;text/plain;application/octet")
    firefox_profile.set_preference("browser.helperApps.alwaysAsk.force", False)
    firefox_profile.set_preference("browser.download.manager.showWhenStarting", False)
    firefox_profile.set_preference("network.proxy.type", 1)
    firefox_profile.set_proxy(proxy.selenium_proxy())
    try:
        webdriver = WebDriver(firefox_profile)
        proxy.new_har(start_url.hostname, httpheaders=True)
        analyse_page(webdriver, start_url)
        har = proxy.har
        logging.info("Stopping WebRunner")
        proxy.close()
        server.stop()
        webdriver.quit()
        har = Har(har)
    except Exception, e:
        logging.error(e)
        proxy.close()
        webdriver.quit()
        server.stop()
    return har


def analyse_page(webdriver, start_url):
    global URLs
    current_page = webdriver.get(start_url.geturl())
    URLs.append(current_page)


def find_external_connections(harlog):
    connections = []
    for entry in harlog.entries:
        if entry.server_ip_address:
            if not is_old(entry.server_ip_address, connections):
                connections.append(entry.server_ip_address)


    logging.debug(connections)
    return connections

def is_old(ipaddress, connections):
    for old_connection in connections:
        if old_connection == ipaddress:
            return True

    return False
