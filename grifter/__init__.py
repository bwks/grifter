import sys
import logging

# from .api import (
#     generate_loopbacks,
#     add_blackhole_interfaces,
#     update_guest_data,
#     update_guest_interfaces,
#     generate_vagrant_file,
# )
from .cli import (
    cli,
)
# from .loaders import (
#     load_data,
#     render_from_template,
#     load_config_file,
# )
# from .validators import (
#     validate_required_keys,
#     validate_required_values,
# )

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.ERROR)
logger.addHandler(handler)
