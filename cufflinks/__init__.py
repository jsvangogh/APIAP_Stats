"""

A productivity tool that binds pandas and plotly.
It also provides tools for color generation and transformation. 

Author: @jorgesantos

"""



import cufflinks.datetools
import cufflinks.utils
import cufflinks.datagen
import cufflinks.tools
import cufflinks.colors
import cufflinks.pandastools
import cufflinks.ta

from cufflinks.plotlytools import *
from plotly.plotly import plot
from cufflinks.utils import pp
from cufflinks.tools import subplots,scatter_matrix,figures
from cufflinks.extract import to_df
from cufflinks.auth import set_config_file,get_config_file
from cufflinks.offline import is_offline,go_offline,go_online
from cufflinks.version import __version__

try:
	if get_config_file()['offline']:
		go_offline()
	else:
		go_online()
except:
	pass
