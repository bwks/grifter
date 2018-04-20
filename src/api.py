import yaml

from utils import (
    explode_port,
    generate_loopbacks,
    render_from_template,
    update_hosts,
)

custom_filters = [explode_port]

with open('examples/hosts.yml', 'r') as f:
    data = yaml.load(f)

loopbacks = generate_loopbacks(data)
update_hosts(data['hosts'])


with open('examples/Vagrantfile', 'w') as f:
    vagrantfile = render_from_template('./templates', 'host.j2', custom_filters, hosts=data['hosts'], loopbacks=loopbacks)
    f.write(vagrantfile)
    print(vagrantfile)

