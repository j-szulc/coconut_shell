from coconut_shell import *

__author__ = "Jakub Szulc"
__copyright__ = "Jakub Szulc"
__license__ = "MIT"

sh("echo 'Hello World!\n dupa'") | sh("nl") | cat()