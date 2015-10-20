import os, sys
sys.path.append('/home/gingo/app')
sys.path.append('/home/gingo/app/gingosrv')

from gingo import app as application

if __name__=='__main__':
	application.run('192.168.1.5', 5000)
