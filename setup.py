Program = "main"
Script = "main.py"

from distutils.core import setup
import py2exe

#Helpful links
# http://www.blog.pythonlibrary.org/2010/07/31/a-py2exe-tutorial-build-a-binary-series/
# http://www.py2exe.org/index.cgi/IncludingTypelibs
# http://mail.python.org/pipermail/python-win32/2010-March/010329.html
#http://www.py2exe.org/index.cgi/Tutorial#Step5
# http://stackoverflow.com/questions/1153643/how-do-i-debug-a-py2exe-application-failed-to-initialize-properly-error

excludes = ['_gtkagg', '_tkagg', 'bsddb', 'curses', 'email', 'pywin.debugger',
            'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
            'Tkconstants', 'Tkinter']


setup(windows=[{
			"script": Script,
			"dest_base": Program,}],
	  data_files = [
			'boom.wav',
			'dead.wav',
			'drain.wav',
			'hit.wav',
			'shot1.wav',
			'shot2.wav',
			],

	zipfile = None,
		options = {"py2exe" : {
#	  "compressed": 2,
	  "optimize": 2,
	  "bundle_files": 1,	#3 if having issues
  # "dll_excludes": ['MSVCP90.dll'],
	"dll_excludes": [ "mswsock.dll", "powrprof.dll" ], # http://stackoverflow.com/questions/2104611/memoryloaderror-when-trying-to-run-py2exe-application
   "excludes": excludes,
	  "packages": [
			"win32com.gen_py"],
	  }}
	  )
