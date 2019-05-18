import sys

from seleniumwire import webdriver  # Import from seleniumwire
from selenium.webdriver.firefox.options import Options

import tldextract
from urllib.parse import urlparse

import sqlite3
import json

options = Options()
options.headless = True
# Create a new instance of the Firefox driver
driver = webdriver.Firefox(options=options)

original_domain = sys.argv[1]
url = 'https://{}'.format(original_domain)
driver.get(url)

conn = sqlite3.connect("requests.db")
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS requests(
        original_domain TEXT NOT NULL,
        original_url TEXT NOT NULL,
        time_request INT DEFAULT (strftime('%s','now')),
        request TEXT,
        status_code INT,
        subdomain TEXT,
        domain TEXT,
        tld TEXT, 
        scheme TEXT, 
        netloc TEXT, 
        path TEXT, 
        params TEXT, 
        query TEXT, 
        fragment TEXT, 
        request_header TEXT,
        response_header TEXT
    );
''')
conn.commit()

insert_stmt = """
INSERT INTO requests(
        original_domain,
        original_url,
        request,
        status_code,
        subdomain,
        domain,
        tld, 
        scheme, 
        netloc, 
        path, 
        params, 
        query, 
        fragment, 
        request_header,
        response_header
) 
VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, json(?), json(?));
"""

# Access requests via the `requests` attribute
for request in driver.requests:
    if request.response:
        rpath = request.path
        subdomain, domain, tld = tldextract.extract(rpath)
        parsedRequest = urlparse(rpath)
        scheme, netloc, path, params, query, fragment = parsedRequest
        status_code = request.response.status_code
        data = (
            original_domain,
            url,
            rpath,
            request.response.status_code,
            subdomain,
            domain,
            tld,
            scheme,
            netloc,
            path,
            params,
            query,
            fragment,
            json.dumps(dict(request.headers)),
            json.dumps(dict(request.response.headers)),
        )

        c.execute(insert_stmt, data);

conn.commit()

driver.close()
driver.quit()

print(original_domain)
