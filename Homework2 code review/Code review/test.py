from subprocess import call
import time
import signal

 
def test_request(arg=None):
    time.sleep(2)
    return arg
 
class Timeout():
    class Timeout(Exception):
        pass
 
    def __init__(self, sec):
        self.sec = sec
 
    def __enter__(self):
        signal.signal(signal.SIGALRM, self.raise_timeout)
        signal.alarm(self.sec)
 
    def __exit__(self, *args):
        signal.alarm(10)   
 
    def raise_timeout(self, *args):
        raise Timeout.Timeout()



def noinput():
	test_program = 'python 1.py'
	call(test_program, shell=True)
	print("============================ No input test passed! ===========================")
	return

def notweet():
	test_program = 'python 1.py @RunzhouH'
	call(test_program, shell=True)
	print("============================ No tweet test passed! ===========================")
	return

def falsescreen():
	test_program = 'python 1.py @fsdlfkiaoadfoidhoi13r'
	call(test_program, shell=True)
	print("============================ False screen test passed! ===========================")
	return


start_time = time.time()

def main():
	try:
		with Timeout(15):
			noinput()
			noinputtime = time.time() - start_time
			print("============================ %s seconds =============================" %noinputtime)
	except Timeout.Timeout:
		print("============================ Run out of 15 seconds! ===========================")
		print("============================ No input test failed! ===========================")

	try :
		with Timeout(15):
			notweet()
			notweettime = time.time() - start_time
			print("============================ %s seconds =============================" %notweettime)
	except Timeout.Timeout:
		print("============================ Run out of 15 seconds! ===========================")
		print("============================ No tweet test failed! ===========================")

	try :
		with Timeout(15):
			notweet()
			notweettime = time.time() - start_time
			print("============================ %s seconds =============================" %notweettime)
	except Timeout.Timeout:
		print("============================ Run out of 15 seconds! ===========================")
		print("=========================== False screen test failed! ==========================")

if __name__ == '__main__':
	main()