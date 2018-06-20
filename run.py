from app import create_app
import argparse

def set_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config",
                        action="store", dest="config",
                        help="Config name")
    options = parser.parse_args()
    return options


if __name__ == '__main__':
    
    options = set_options()
    config_name = 'development'
    if options.config:
        config_name = options.config

    app = create_app(config_name)
    app.run()
