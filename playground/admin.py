from django.contrib import admin
from .models import Ville
from .models import Agence
from .models import Agent
from .models import Colis
from .models import Courrier
from .models import BoitePostale
from .models import Reexpedition
from .models import Activite
from .models import Expediteur
from .models import Panier
from .models import PrixBoiteReexpedition
from .models import PrixColisCourrier
from .models import Recu

admin.site.register(Ville) 
admin.site.register(Agence) 
admin.site.register(Agent) 
admin.site.register(Colis) 
admin.site.register(Courrier) 
admin.site.register(BoitePostale) 
admin.site.register(Reexpedition) 
admin.site.register(Activite) 
admin.site.register(Expediteur) 
admin.site.register(Panier) 
admin.site.register(PrixBoiteReexpedition) 
admin.site.register(PrixColisCourrier) 
admin.site.register(Recu) 