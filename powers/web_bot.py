from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


test_url = 'https://www.sccourts.org/caseSearch/'
county = 'Abbeville'

class BotException(Exception):
	pass

def format_county_name(bond_county):
	"""For search county must be full name followed by a comma
		e.g Charleston,
	"""
	pass


def run_bot(url, county, warrant_id):
	"""Go to landing page select county then fill out form."""
	driver = webdriver.Chrome()
	driver.get(url)

	driver.implicitly_wait(2)
	# Find the County
	try:
		driver.find_element_by_link_text(county).click()
	except:
		driver.close()
		BotException("County not found: {}".format(county))

	driver.implicitly_wait(2)
	# Accept terms and conditions
	try:
		driver.find_element_by_id("ContentPlaceHolder1_ButtonAccept").click()
	except:
		driver.close()
		BotException("Could not enter county site")

	driver.implicitly_wait(10)
	# Fill in form with warrant number
	try:
		case_field = driver.find_element_by_id('ContentPlaceHolder1_TextBoxCaseNumber')
		case_field.send_keys(warrant_id)
		driver.find_element_by_id('ContentPlaceHolder1_ButtonSearch').click()
		driver.implicitly_wait(5)
	except:
		driver.close()
		BotException("Unhandled exception filling form.")

	# Parse Results
	results_table = driver.find_element_by_id('ContentPlaceHolder1_SearchResults')
	if not results_table:
		driver.close()
		BotException("No results with warrant number: {}".format(warrant_id))

	try:
		driver.close()
		# 7th element refers to Case Status Column
		table_rows = results_table.find_elements(By.XPATH, '//td')
		return table_rows[7].text
	except:
		driver.close()
		BotException("Error fetching case status.")


run_bot(test_url, 'Charleston,', '20190420152183')