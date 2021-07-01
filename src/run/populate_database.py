from src.utils.es_interface import ElasticInterface


# TODO rewrite this to use put requests

def main():
    ElasticInterface().populate_dummy_data()


if __name__ == '__main__':
    main()
