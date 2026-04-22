import init # type: ignore
from process_data import listMultilevelStats as listStats  # type: ignore
init.checkForUpdates()
init.checkForNewBuildings()
print(listStats('W_MultiAge_ANNI23A'))
