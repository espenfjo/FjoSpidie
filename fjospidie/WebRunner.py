import logging
from browsermobproxy import Server
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from harpy.har import Har
import os
from xvfbwrapper import Xvfb

from Utils import get_md5

URLS = []

class WebRunner(object):
    """
    Stuff to run firefox and do the actual analysis of the web page
    """
    def __init__(self, report):
        self.spidie = report
        self.logger = logging.getLogger(__name__)
        self.xvfb = Xvfb(width=1920, height=1080)

    def run_webdriver(self, start_url, port, config, download_dir):
        """
        Run Selenium WebDriver
        """
        useragent = None
        referer = None
        webdriver = None
        urllib3_logger = logging.getLogger('urllib3')
        urllib3_logger.setLevel(logging.DEBUG)

        self.logger.info("Starting WebRunner")
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

        self.logger.debug("Running with UserAgent: {}".format(useragent))
        self.logger.debug("Running with Referer: {}".format(referer))
        self.logger.debug("Checking URL: {}".format(config.url))

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
        from types import NoneType
        if config.firefoxprofile is not None and os.path.isdir(config.firefoxprofile):
            self.logger.debug("Using existing firefox profile")
            firefox_profile = FirefoxProfile(profile_directory=config.firefoxprofile)
        else:
            firefox_profile = FirefoxProfile()

        self.logger.debug("Using profile {}".format(firefox_profile.path))

        firefox_profile.set_preference("security.OCSP.enabled", 0)
        firefox_profile.set_preference("browser.download.folderList", 2)
        firefox_profile.set_preference("browser.download.manager.showWhenStarting", False)
        firefox_profile.set_preference("browser.download.dir", download_dir)
        firefox_profile.set_preference("browser.helperApps.neverAsk.saveToDisk",
                                       "application/x-xpinstall;application/x-zip;application/x-zip-compressed;application/octet-stream;application/zip;application/pdf;application/msword;text/plain;application/octet")
        firefox_profile.set_preference("browser.helperApps.alwaysAsk.force", False)
        firefox_profile.set_preference("browser.download.manager.showWhenStarting", False)
        firefox_profile.set_preference("security.mixed_content.block_active_content", False)
        firefox_profile.set_preference("security.mixed_content.block_display_content", False)
        firefox_profile.set_preference("extensions.blocklist.enabled", False)
        firefox_profile.set_preference("network.proxy.type", 1)
        firefox_profile.set_proxy(proxy.selenium_proxy())
        firefox_profile.set_preference("webdriver.log.file", "/tmp/ff.log")
        firefox_profile.set_preference("webdriver.log.driver", "DEBUG")
        firefox_profile.set_preference("browser.newtabpage.enhanced", False)
        firefox_profile.set_preference("browser.newtabpage.enabled", False)
        firefox_profile.set_preference("browser.newtabpage.directory.ping", "")
        firefox_profile.set_preference("browser.newtabpage.directory.source", "")
        firefox_profile.set_preference("browser.search.geoip.url", "")

        try:
            self.xvfb.start()
            capabilities = DesiredCapabilities.FIREFOX
            capabilities['loggingPrefs'] = {'browser':'ALL'}
            if os.path.exists("{}/firefox".format(firefox_profile.path)):
                binary = FirefoxBinary("{}/firefox".format(firefox_profile.path))
            else:
                binary = FirefoxBinary("/usr/bin/firefox")
            webdriver = WebDriver(capabilities=capabilities, firefox_profile=firefox_profile, firefox_binary=binary)
            proxy.new_har(start_url.hostname,
                          options={"captureHeaders": "true", "captureContent": "true", "captureBinaryContent": "true"})
            self.analyse_page(webdriver, start_url)
            for entry in webdriver.get_log('browser'):
                self.logger.info("Firefox: {}".format(entry))
            har = proxy.har
            self.logger.info("Stopping WebRunner")
            proxy.close()
            server.stop()
            webdriver.quit()
            har = Har(har)
        except Exception, e:
            self.logger.error(e)
            proxy.close()
            if webdriver:
                webdriver.quit()
            self.xvfb.stop()
            server.stop()
        return har

    def analyse_page(self, webdriver, start_url):
        """
        Actual run of webdriver
        """
        global URLS
        current_page = webdriver.get(start_url.geturl())

        try:
            screenshot = webdriver.get_screenshot_as_png()
            self.add_scr_to_db(screenshot)
        except Exception, e:
            self.logger.error("Whoops, cant take screenshot: {}".format(e))

        URLS.append(current_page)

    def add_scr_to_db(self, screenshot):
        """
        Add screenshot/render of the web page to the database
        """
        self.logger.debug("Adding screenshot to database")
        md5 = get_md5(screenshot)
        fs_id = None
        if not self.spidie.database.fs.exists({"md5":md5}):
            fs_id = self.spidie.database.fs.put(screenshot, type="screenshot")
        else:
            grid_file = self.spidie.database.fs.get_version(md5=md5)
            fs_id = grid_file._id


        self.spidie.report.screenshot_id = fs_id

    @staticmethod
    def is_old(ipaddress, connections):
        """
        Check if we have seen the given IP address earlier
        """
        if ipaddress in connections:
            return True

        return False


    def find_external_connections(self, harlog):
        """
        Add each connection to the connection list
        """
        connections = []
        for entry in harlog.entries:
            if entry.server_ip_address:
                if not WebRunner.is_old(entry.server_ip_address, connections):
                    connections.append(entry.server_ip_address)

        self.logger.debug(connections)
        return connections
