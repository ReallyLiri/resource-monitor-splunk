import json
import requests
import warnings
import logging
from time import sleep, time
from collections import defaultdict

warnings.filterwarnings("ignore")

with open("config.json", 'r') as f:
	config = json.load(f)

refresh_interval_sec = config['check_interval_sec']

errors = defaultdict(int)


def log_splunk(url, name, code, message, downtime):
	params = {
		'time': time(),
		'host': 'Monitoring-Service',
		'index': 'main',
		'source': name.lower().replace(' ', '-'),
		'sourcetype': 'json',
		'event': {
			'url': url,
			'name': name,
			'code': code,
			'message': message,
			'downtime_min': int(downtime * refresh_interval_sec / 60)
		},
	}
	response = requests.post(
		config['splunk_url'],
		data=json.dumps(params, sort_keys=True),
		headers={'Authorization': "Splunk {}".format(config['splunk_token'])},
		verify=False
	)
	logging.info(response)


def on_error(url, name, code, message):
	errors[url] += 1
	log_splunk(url, name, code, message, errors[url])


def on_success(url, name):
	if url in errors:
		del errors[url]
	log_splunk(url, name, 200, 'success', 0)


def routine_check(name, url):
	try:
		logging.info("GET: {}".format(url))
		response = requests.get(url, verify=False, timeout=3)
		code = response.status_code
		if code != 200:
			logging.warning("GET {} failed - {} - {}".format(url, code, response.text))
			on_error(url, name, code, response.text)
		else:
			on_success(url, name)
			logging.info("GET {} succeeded".format(url))
	except Exception as ex:
		on_error(url, name, 500, str(ex))
		logging.warning("GET {} failed - {}".format(url, ex))


def routine_checks():
	address = config['address']
	for subdomain in config['subdomains']:
		for name, path in config['paths'].items():
			check_name = f"{name} in {subdomain} env"
			url = f"{address.format(subdomain)}{path}"
			routine_check(check_name, url)


if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO)
	while True:
		try:
			logging.info("Starting routine...")
			routine_checks()
			logging.info("Done, going to sleep")
		except Exception as ex:
			logging.error("Unexpected error!!! {}".format(ex))
		finally:
			sleep(refresh_interval_sec)
