import pandas as pd
from maquina import *
from of import *
from slot import *
from functions import *
from datetime import datetime
import numpy as np

df_acabamentos=importar_acabamentos()
df_clientes=importar_clientes()
grupos=[]

maquinas=import_maquinas()

slots=alocar_slots()

definir_capacidades()

ofs=import_ofs()

materialkey,stock=import_stocks()



#todo adicionar setups

