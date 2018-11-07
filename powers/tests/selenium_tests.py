from powers.models import SuretyCompany, User, Defendant, Bond, Powers
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.conf import settings
from selenium.webdriver.support.ui import Select
from datetime import datetime

class TestAdmin(StaticLiveServerTestCase):

	def setUp(self):
		self.super_user =   {
			'username': 'admin',
			'password': '1Testing!',
			'first_name': 'Charles',
			'last_name': 'Lane',
			'email': 'charleslane23@gmail.com',
			'is_superuser': True,
			'is_staff': True
			}
		self.agent = {
			'username': 'test_user',
			'password': '1Testing!',
			'first_name': 'pablo',
			'last_name': 'escobar',
			'email': 'charleslane23@gmail.com',
			'is_superuser': True,
			'is_staff': True
		}
		if getattr(settings, 'DATABASES')['default']['ENGINE'] == 'django.db.backends.sqlite3':
			pass
		else:
			raise Exception('Running on live database!')

		self.driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')

	def test_agent(self):
		## Signin
		self.driver.get("http://localhost:8000/admin/login/?next=/admin/")

		self.driver.find_element_by_id('id_username').send_keys(self.agent['username'])
		self.driver.find_element_by_id('id_password').send_keys(self.agent['password'])
		self.driver.find_element_by_xpath('//input[@value="Log in"]').click()

		## Check limitations

		link_div = self.driver.find_element_by_class_name('app-powers')
		link_headers = link_div.find_elements_by_tag_name('th')
		link_names = [header.find_element_by_tag_name('a').text for header in link_headers]
		print(link_names, 'names')
		self.assertTrue('Bonds' in link_names)
		self.assertTrue('Surety Companies' not in link_names)


	def test_admin(self):
		##Signin
		self.driver.get("http://localhost:8000/admin/login/?next=/admin/")

		self.driver.find_element_by_id('id_username').send_keys(self.super_user['username'])
		self.driver.find_element_by_id('id_password').send_keys(self.super_user['password'])
		self.driver.find_element_by_xpath('//input[@value="Log in"]').click()

		##Create Powers Batch
		powers_link = self.driver.find_element_by_link_text('Powers')
		powers_link.click()
		batch_link = self.driver.find_element_by_link_text('Create Batch')
		batch_link.click()

		number_powers = self.driver.find_element_by_id('id_number')
		number_powers.send_keys('2')

		value_powers = Select(self.driver.find_element_by_name('type'))
		value_powers.select_by_index(1)

		self.driver.find_element_by_xpath('//input[@value="Create Batch"]').click()



		## Transfer Powers
		transfer_link = self.driver.find_element_by_link_text('Transfer')
		transfer_link.click()

		select = Select(self.driver.find_element_by_name('agent'))
		select.select_by_index(1)
		self.driver.find_element_by_xpath('//input[@value="Submit"]').click()
		self.assertEqual(self.driver.current_url ,'http://localhost:8000/admin/powers/powers/')

		## Edit Defendant
		self.driver.get('http://localhost:8000/admin/')
		defendant_link = self.driver.find_element_by_link_text('Defendants')
		defendant_link.click()
		element = self.driver.find_element_by_class_name("row1")
		defendant_link = element.find_element_by_tag_name('a')
		defendant_link.click()

		datepicker = self.driver.find_element_by_id('id_next_court_date')
		datepicker.clear()
		datepicker.send_keys('2019-10-20')
		self.driver.find_element_by_xpath('//input[@value="Save"]').click()
		self.assertEqual(self.driver.current_url, 'http://localhost:8000/admin/powers/defendant/')

		## Create Bond
		self.driver.get('http://localhost:8000/admin/')
		bonds_link = self.driver.find_element_by_link_text('Bonds')
		bonds_link.click()
		add_bonds_link = self.driver.find_element_by_link_text('Add bond')
		add_bonds_link.click()

		select_defendant = Select(self.driver.find_element_by_name('defendant'))
		select_defendant.select_by_index(1)

		select_agent = Select(self.driver.find_element_by_name('agent'))
		select_agent.select_by_index(1)

		select_powers = Select(self.driver.find_element_by_name('powers'))
		select_powers.select_by_index(2)

		self.driver.find_element_by_id('id_amount').send_keys(10)
		self.driver.find_element_by_id('id_bond_fee').send_keys(10)
		self.driver.find_element_by_id('id_related_court').send_keys('charleston')
		self.driver.find_element_by_id('id_county').send_keys('charleston')
		self.driver.find_element_by_id('id_city').send_keys('charleston')
		self.driver.find_element_by_id('id_state').send_keys('sc')
		self.driver.find_element_by_id('id_warrant_number').send_keys('12222')
		self.driver.find_element_by_id('id_offences').send_keys('Rape and Murder')
		self.driver.find_element_by_xpath('//input[@value="Save"]').click()
		
		self.assertEqual(self.driver.current_url, 'http://localhost:8000/admin/powers/bond/')

		# Print Bond
		self.driver.get('http://localhost:8000/admin/')
		bonds_link = self.driver.find_element_by_link_text('Bonds')
		bonds_link.click()
		print_link = self.driver.find_element_by_link_text('Print Bond')
		print_link.click()





	def tearDown(self):
		# self.driver.quit()
		pass
