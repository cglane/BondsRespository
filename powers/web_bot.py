from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

SC_COUNTIES = {
	"Abbeville,": ["Abbeville", 'Abbe'],
	"Aiken,": ["Aiken"],
	"Bamberg,": ["Bamberg", "Bamb"],
	"Barnwell,": ["Barnwell", "Barn"],
	"Beaufort,": ["Beaufort", "Beau"],
	"Berkeley,": ["berk", "BERK", "berkeley", "Berkley", "Moncks Corner"],
	"Calhoun,": ["Calhoun",],
	"Charleston,": ["Charleson", "Charleston", "Chas", "North Charleston"],
	"Cherokee,": ["Cherokee"],
	"Chester,": ["Chester"],
	"Chesterfield,": ["Chesterfield"],
	"Clarendon,": ["Clarendon"],
	"Colleton,": ["Colleton"],
	"Darlington,": ["Darlington"],
	"Dillon,": ["Dillon"],
	"Dorchester,": ["Dorchester", "DORCH"],
	"Edgefield,": ["Edgefield"],
	"Fairfield,": ["Fairfield"],
	"Florence,": ["Florence"],
	"Georgetown,": ["Georgetown"],
	"Greenville,,": ['Greenville', 'Greenv', "Greenvillie"],
	"Greenwood,": ["Greenwood"],
	"Hampton,": ["Hampton"],
	"Horry,": ["Horry"],
	"Jasper,": ["Jasper"],
	"Kershaw,": ["Kershaw"],
	"Lancaster,": ["Lancaster"],
	"Laurens,": ["Laurens"],
	"Lee,": ["Lee"],
	"Lexington,": ["Lexingon", "Lexington", "Lexinton"],
	"Marion,": ["Marion"],
	"Marlboro,": ["Marlboro"],
	"McCormick,": ["McCormick"],
	"Newberry,": ["Newberry"],
	"Oconee,": ["Oconee"],
	"Orangeburg,": ["Orangeburg", "Orangburg"],
	"Pickens,": ["Pickens"],
	"Richland,": ["Columbia", "Richland"],
	"Saluda,": ["Saluda"],
	"Spartanburg,": ["Spartanburg", "Sparrtanburg"],
	"Sumter,": ["Sumter"],
	"Union,": ["Union"],
	"Williamsburg,": ["Williamsburg"],
	"York,": ["York"]


}
class BotException(Exception):
	pass

class BondStatus():
	def __init__(self):
		self.driver = webdriver.Chrome(ChromeDriverManager().install())

		self.base_url = "https://www.sccourts.org/caseSearch/"

	def _format_county_name(self, bond_county):
		"""For search county must be full name followed by a comma
			e.g Charleston,
		"""
		for key, names in SC_COUNTIES.items():
			if bond_county.lower() in [x.lower() for x in names]:
				return key

	def _accept_terms(self):
		try:
			self.driver.find_element_by_id("ContentPlaceHolder1_ButtonAccept").click()
		except:
			raise BotException("Could not enter county site")

	def _fill_form(self, warrant_id):
		try:
			case_field = self.driver.find_element_by_id('ContentPlaceHolder1_TextBoxCaseNumber')
			case_field.send_keys(warrant_id)
			self.driver.find_element_by_id('ContentPlaceHolder1_ButtonSearch').click()
			self.results_table = self.driver.find_element_by_id('ContentPlaceHolder1_SearchResults')
		except Exception as e:
			raise BotException("No results with warrant number: {}".format(warrant_id))

	def _parse_results(self):
		try:
			# 7th element refers to Case Status Column
			table_rows = self.results_table.find_elements(By.XPATH, '//td')
			return table_rows[7].text
		except:
			raise BotException("Error fetching case status.")

	def find_county(self, county):
		self.driver.get(self.base_url)
		county_key = self._format_county_name(county)
		if not county_key:
			raise BotException("County not found for name: {}".format(county))
		try:
			self.driver.find_element_by_link_text(county_key).click()
		except:
			raise BotException("County not found with key: {}".format(county_key))

	def run_bot(self, county, warrant_id):
		# Go to base url and find county from map
		self.find_county(county)
		self.driver.implicitly_wait(5)

		# Accept terms and conditions
		self._accept_terms()
		self.driver.implicitly_wait(2)

		# Insert warrant id into case id field
		self._fill_form(warrant_id)
		self.driver.implicitly_wait(3)

		# Return results if any
		return self._parse_results()

	def quit(self):
		self.driver.quit()
