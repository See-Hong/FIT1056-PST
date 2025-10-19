from gui.main_dashboard import launch
from app.admin_utils import init_logger, backup_data

if __name__ == "__main__":
    init_logger()
    backup_data()

    launch()