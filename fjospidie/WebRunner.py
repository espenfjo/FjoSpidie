import logging
import time
import sys
from browsermobproxy import Server
from browsermobproxy import Client
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from harpy.har import Har
import psycopg2
import hashlib
URLs = []


class WebRunner:

    def __init__(self, report):
        self.spidie = report

    def run_webdriver(self, start_url, port, config, download_dir):
        global useragent
        global referer
        webdriver = None
        urllib3_logger = logging.getLogger('urllib3')
        urllib3_logger.setLevel(logging.DEBUG)
        logging.info("Starting WebRunner")
        firefox_profile = None
        server = None
        proxy = None
        har = None

        if config.referer:
            referer = config.referer
        else:
            referer = 'http://www.google.com/search?q={}+&oq={}&oe=utf-8&rls=org.mozilla:en-US:official&client=firefox-a&channel=fflb&gws_rd=cr'.format(
                config.url, config.url)

        if config.useragent:
            useragent = config.useragent
        else:
            useragent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:24.0) Gecko/20100101 Firefox/24.0'

        logging.debug("Running with UserAgent: {}".format(useragent))
        logging.debug("Running with Referer: {}".format(referer))
        logging.debug("Checking URL: {}".format(config.url))

        server = Server("lib/browsermob/bin/browsermob-proxy", {'port': port})
        server.start()
        proxy = server.create_proxy()
        proxy.headers({'User-Agent': useragent, 'Accept-Encoding': "", 'Connection': 'Close'})
        request_js = (
            'var referer = request.getProxyRequest().getField("Referer");'
            'addReferer(request);'
            'function addReferer(r){'
            'if (! referer ) {'
            'r.addRequestHeader("Referer","' + referer + '");'
            '}'
            'return;'
            '}')
        proxy.request_interceptor(request_js)
        if config.firefoxprofile:
            firefox_profile = FirefoxProfile(profile_directory=config.firefoxprofile)
        else:
            firefox_profile = FirefoxProfile()

        logging.debug("Using profile {}".format(firefox_profile.path))

        firefox_profile.set_preference("security.OCSP.enabled", 0)
        firefox_profile.set_preference("browser.download.folderList", 2)
        firefox_profile.set_preference("browser.download.manager.showWhenStarting", False)
        firefox_profile.set_preference("browser.download.dir", download_dir)
        firefox_profile.set_preference("browser.helperApps.neverAsk.saveToDisk",
                                       "application/x-xpinstall;application/x-zip;application/x-zip-compressed;application/octet-stream;application/zip;application/pdf;appl\
                                       ication/msword;text/plain;application/octet")
        firefox_profile.set_preference("browser.helperApps.alwaysAsk.force", False)
        firefox_profile.set_preference("browser.download.manager.showWhenStarting", False)
        firefox_profile.set_preference("security.mixed_content.block_active_content", False)
        firefox_profile.set_preference("security.mixed_content.block_display_content", False)
        firefox_profile.set_preference("extensions.blocklist.enabled", False)
        firefox_profile.set_preference("network.proxy.type", 1)
        firefox_profile.set_proxy(proxy.selenium_proxy())
        firefox_profile.set_preference("webdriver.log.file", "/tmp/ff.log");
        firefox_profile.set_preference("webdriver.log.driver", "DEBUG");
        try:
            capabilities = DesiredCapabilities.FIREFOX
            capabilities['loggingPrefs'] = { 'browser':'ALL' }
            binary = FirefoxBinary('firefox/firefox')
            webdriver = WebDriver(capabilities=capabilities, firefox_profile=firefox_profile, firefox_binary=binary)
            proxy.new_har(start_url.hostname,
                          options={"captureHeaders": "true", "captureContent": "true", "captureBinaryContent": "true"})
            self.analyse_page(webdriver, start_url)
            for entry in webdriver.get_log('browser'):
                    logging.info("Firefox: {}".format(entry))
            har = proxy.har
            logging.info("Stopping WebRunner")
            proxy.close()
            server.stop()
            webdriver.quit()
            har = Har(har)
        except Exception, e:
            logging.error(e)
            proxy.close()
            if webdriver:
                webdriver.quit()
            server.stop()
        return har

    def analyse_page(self, webdriver, start_url):
        global URLs
        current_page = webdriver.get(start_url.geturl())

        try:
            screenshot = webdriver.get_screenshot_as_png()
            self.add_scr_to_db(screenshot)
        except Exception, e:
            logging.error("Whoops, cant take screenshot: {}".format(e))

        URLs.append(current_page)

    def add_scr_to_db(self, screenshot):
        logging.debug("Adding screenshot to database")
        md5 = self.__get_md5(screenshot)
        fs_id = None
        if not self.spidie.database.fs.exists({"md5":md5}):
            fs_id = self.spidie.database.fs.put(screenshot, manipulate=False)
        else:
            grid_file = self.spidie.database.fs.get_version(md5=md5)
            fs_id = grid_file._id
            

        self.spidie.report.screenshot_id = fs_id

    def find_external_connections(self, harlog):
        connections = []
        for entry in harlog.entries:
            if entry.server_ip_address:
                if not self.is_old(entry.server_ip_address, connections):
                    connections.append(entry.server_ip_address)

        logging.debug(connections)
        return connections

    def is_old(self, ipaddress, connections):
        for old_connection in connections:
            if old_connection == ipaddress:
                return True

        return False

    def __get_md5(self, data):
        md5 = hashlib.md5()
        md5.update(data)
        return md5.hexdigest()
