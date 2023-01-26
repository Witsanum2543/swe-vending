try :
    from run import app
    import unittest
    import requests
except Exception as e:
    print("Some Modules are Missing {}" .format(e))

class FlaskTest(unittest.TestCase):
    
    def test_create_vending_machine_api(self):

        data = {
            'name': 'ven1',
            'location': 'b',
            'items' : {"orio": 50}
        }
        response = requests.post('http://localhost:8080/create-vending-machine', json=data)

        self.assertEqual(response.json(), data)
        
     

if __name__ == "__main__":
    unittest.main()