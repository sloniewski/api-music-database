from app import create_app

# engine = create_engine(
#     config.conf_string,
#     pool_pre_ping=True,
# )
# Base = declarative_base()

app = create_app('development')

if __name__ == '__main__':
    app.run()
