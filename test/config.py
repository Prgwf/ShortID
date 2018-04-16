import json
import optparse

def parse_opt():
    parser = optparse.OptionParser()

    parser.add_option('-c', dest='config')

    (options, args) = parser.parse_args()

    return options


def load_config(options):
    file = options.config
    with open(file, 'r') as f:
        config = json.load(f)
    return config

if __name__ == '__main__':
#     config = {
# 'SQLALCHEMY_DATABASE_URI': 'mysql://root:token@localhost:3306/shortid_db',
# 'SQLALCHEMY_TRACK_MODIFICATIONS': 'true',
# 'SECRET_KEY': 'dont do badthings to me please'
# }
#     with open('config', 'w') as f:
#         json.dump(config, f)

    options = parse_opt()
    config = load_config(options)
    for key, values in config.items():
        print(key, values)
