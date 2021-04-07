import unittest
import requests
import json

class TestChars(unittest.TestCase):

    SITE_URL = 'http://localhost:51040'
    print("Testing for server: " + SITE_URL)
    CHARS_URL = SITE_URL + '/hp/'
    RESET_URL = SITE_URL + '/hp/reset/'

    def reset_data(self):
        r = requests.put(self.RESET_URL)

    def is_json(self, resp):
        try:
            json.loads(resp)
            return True
        except ValueError:
            return False

    def test_get_cid(self):
        self.reset_data()
        cid = 1
        r = requests.get(self.CHARS_URL + 'cid/' + str(cid))
        self.assertTrue(self.is_json(r.content.decode()))
        resp = json.loads(r.content.decode())

        self.assertEqual(resp['name'], 'Harry Potter')
        self.assertEqual(resp['species'], 'human')
        self.assertEqual(resp['gender'], 'male')
        self.assertEqual(resp['house'], 'Gryffindor')
        self.assertEqual(resp['actor'], 'Daniel Radcliffe')

    def test_get_name(self):
        self.reset_data()
        name = 'harrypotter'
        r = requests.get(self.CHARS_URL + 'name/' + name)
        self.assertTrue(self.is_json(r.content.decode()))
        resp = json.loads(r.content.decode())
        testchar = resp['character']

        self.assertEqual(testchar['name'], 'Harry Potter')
        self.assertEqual(testchar['species'], 'human')
        self.assertEqual(testchar['gender'], 'male')
        self.assertEqual(testchar['house'], 'Gryffindor')
        self.assertEqual(testchar['actor'], 'Daniel Radcliffe')

    def test_get_index(self):
        self.reset_data()
        r = requests.get(self.CHARS_URL)
        self.assertTrue(self.is_json(r.content.decode()))
        resp = json.loads(r.content.decode())

        testchar = {}
        chars = resp['characters']
        testchar = chars[0]

        self.assertEqual(testchar['name'], 'Harry Potter')
        self.assertEqual(testchar['species'], 'human')
        self.assertEqual(testchar['gender'], 'male')
        self.assertEqual(testchar['house'], 'Gryffindor')
        self.assertEqual(testchar['actor'], 'Daniel Radcliffe')

    def test_put_cid(self):
        self.reset_data()
        cid = 1
        r = requests.get(self.CHARS_URL + 'cid/' + str(cid))
        self.assertTrue(self.is_json(r.content.decode()))
        resp = json.loads(r.content.decode())
        self.assertEqual(resp['name'], 'Harry Potter')
        self.assertEqual(resp['species'], 'human')
        self.assertEqual(resp['gender'], 'male')
        self.assertEqual(resp['house'], 'Gryffindor')
        self.assertEqual(resp['actor'], 'Daniel Radcliffe')

        c = {}
        c['name'] = 'ABC'
        c['species'] = 'human'
        c['gender'] = 'male'
        c['house'] = 'Hufflepuff'
        c['actor'] = 'ABC'
        r = requests.put(self.CHARS_URL + str(cid), data = json.dumps(m))
        self.assertTrue(self.is_json(r.content.decode()))
        resp = json.loads(r.content.decode())
        self.assertEqual(resp['result'], 'success')

        r = requests.get(self.CHARS_URL + str(cid))
        self.assertTrue(self.is_json(r.content.decode()))
        resp = json.loads(r.content.decode())
        self.assertEqual(resp['name'], c['name'])
        self.assertEqual(resp['species'], c['species'])
        self.assertEqual(resp['gender'], c['gender'])
        self.assertEqual(resp['house'], c['house'])
        self.assertEqual(resp['actor'], c['actor'])

    def test_post_index(self):
        self.reset_data()

        c = {}
        c['name'] = 'ABC'
        c['species'] = 'human'
        c['gender'] = 'male'
        c['house'] = 'Hufflepuff'
        c['actor'] = 'ABC'
        r = requests.post(self.CHARS_URL, data = json.dumps(c))
        self.assertTrue(self.is_json(r.content.decode()))
        resp = json.loads(r.content.decode())
        self.assertEqual(resp['result'], 'success')

        r = requests.get(self.CHARS_URL + 'name/' + 'abc')
        self.assertTrue(self.is_json(r.content.decode()))
        resp = json.loads(r.content.decode())
        testchar = resp['character']
        self.assertEqual(testchar['name'], c['name'])
        self.assertEqual(testchar['species'], c['species'])
        self.assertEqual(testchar['gender'], c['gender'])
        self.assertEqual(testchar['house'], c['house'])
        self.assertEqual(testchar['actor'], c['actor'])

    def test_delete_cid(self):
        self.reset_data()
        cid = 1

        r = requests.delete(self.CHARS_URL + 'cid/' + str(cid))
        self.assertTrue(self.is_json(r.content.decode()))
        resp = json.loads(r.content.decode())
        self.assertEqual(resp['result'], 'success')

        r = requests.get(self.CHARS_URL + str(cid))
        self.assertTrue(self.is_json(r.content.decode()))
        resp = json.loads(r.content.decode())
        self.assertEqual(resp['result'], 'error')

    def test_delete_name(self):
        self.reset_data()
        name = 'harrypotter'

        m = {}
        r = requests.delete(self.CHARS_URL + 'name/' + name, data = json.dumps(m))
        self.assertTrue(self.is_json(r.content.decode()))
        resp = json.loads(r.content.decode())
        self.assertEqual(resp['result'], 'success')

        r = requests.get(self.CHARS_URL + 'name/' + name)
        self.assertTrue(self.is_json(r.content.decode()))
        resp = json.loads(r.content.decode())
        self.assertEqual(resp['result'], 'error')

    def test_delete_index(self):
        self.reset_data()

        m = {}
        r = requests.delete(self.CHARS_URL, data = json.dumps(m))
        self.assertTrue(self.is_json(r.content.decode()))
        resp = json.loads(r.content.decode())
        self.assertEqual(resp['result'], 'success')

        r = requests.get(self.CHARS_URL)
        self.assertTrue(self.is_json(r.content.decode()))
        resp = json.loads(r.content.decode())
        self.assertEqual(resp['characters'], [])

if __name__ == "__main__":
    unittest.main()