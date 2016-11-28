import redis
import unittest

   
class SimpleTest(unittest.TestCase):
   def testadd1(self):
	redisClient = redis.StrictRedis(host='localhost', port=6379, db=0)
	# set a key
	redisClient.set('name','Pratik')
	# get the key
	nameValue = redisClient.get('name')
	self.assertEquals(nameValue,'Pratik')
      
if __name__ == '__main__':
   unittest.main()


