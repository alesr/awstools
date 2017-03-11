import string
import random
import unittest
from AwsIoT import AwsIoT


class TestAwsIoT(unittest.TestCase):
    def test_create_and_delete_thing(self):
        """Test if Things can be accurately created and deleted"""

        iot = AwsIoT()

        # generate a random name for the Thing
        name = "Thing-" + ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(8)])

        # create the Thing
        arn = iot.create_thing(name)

        # check if it was created correctly
        thing_props = iot.describe_thing(name)
        self.assertEqual(name, thing_props['thingName'])

        # check if the Thing can be deleted
        iot.delete_thing(name)
        try:
            iot.describe_thing(name)
        except Exception as e:
            self.assertTrue("%s not found" % name in e.message)

    def test_create_and_delete_certificates(self):
        iot = AwsIoT()

        # create certificate and check that the description is correct, and that it is active
        cert = iot.create_keys_and_certificate()
        cert_desc = iot.describe_certificate(cert['certificateId'])
        self.assertEqual(cert['certificateArn'], cert_desc['certificateArn'])

        self.assertEqual(cert_desc['status'], "ACTIVE")

        # delete a certificate and check
        iot.delete_certificate(cert['certificateId'])
        try:
            iot.describe_certificate(cert['certificateId'])
        except Exception as e:
            self.assertTrue("%s does not exist" % cert['certificateId'] in e.message)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAwsIoT)
    unittest.TextTestRunner(verbosity=2).run(suite)