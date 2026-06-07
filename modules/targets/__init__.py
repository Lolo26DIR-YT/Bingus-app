from .vehicles import TARGETS as VEHICLE_TARGETS
from .buildings import TARGETS as BUILDING_TARGETS
from .electronics import TARGETS as ELECTRONICS_TARGETS
from .servers import TARGETS as SERVER_TARGETS
from .misc import TARGETS as MISC_TARGETS

ALL_TARGETS = VEHICLE_TARGETS + BUILDING_TARGETS + ELECTRONICS_TARGETS + SERVER_TARGETS + MISC_TARGETS

CATEGORIES = [
    {"key": "vehicles", "label": "🚗 Véhicules", "targets": VEHICLE_TARGETS},
    {"key": "buildings", "label": "🏢 Bâtiments & Coffres-forts", "targets": BUILDING_TARGETS},
    {"key": "electronics", "label": "📹 Systèmes électroniques", "targets": ELECTRONICS_TARGETS},
    {"key": "servers", "label": "🖥️ Serveurs & Bases de données", "targets": SERVER_TARGETS},
    {"key": "misc", "label": "🔧 Systèmes divers", "targets": MISC_TARGETS},
]
