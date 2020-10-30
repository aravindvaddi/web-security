from django.test import TestCase,Client


# Create your tests here.
class MyTestCase(TestCase):
	fixtures = ['testdata.json']

	def setUp(self):
		self.client = Client()
		# creating a csrf enforcing client to test the csrf fix
		self.csrf_client = Client(enforce_csrf_checks=True)

	def test_xss(self):
		# setting payload
		payload = "<script>alert('okay, you need to fix this')</script>"
		# setting parameters
		params = {'director': payload}
		# sending request
		response = self.client.get('/gift.html', params)
		# checking if the payload showed up as text in the html -- Will fail if the payload runs
		self.assertEqual(response.context.get('director', None), payload)

	def test_csrf(self):
		# setting params for the post method
		params = {'username': 'admin', 'amount' : '100'}
		# sending the request to a csrf secure client
		response = self.csrf_client.post('/gift/0', params)
		# the client denies the request due to lack of csrf
		self.assertEqual(response.status_code, 403)

	def test_sqli(self):
		# logging in as to avoid errors
		self.client.login(username='admin', password='adminpassword')
		# sending the payload
		with open('part1/sqlipayload.gftcrd') as f:
			params = {'card_supplied': 'True', 'card_data': f}
			response = self.client.post('/use.html', params)
		# card_found is always None since the it comes from card_query and the select statment checks if two things that aren't fundamentally equal are equal. This is not None if an sql injection takes place
		self.assertEqual(response.context.get('card_found', None), None)
