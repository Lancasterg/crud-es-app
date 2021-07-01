from os import remove

import requests

file_names = ['abc.png', 'test123.png', 'another_file.txt']


def main():
    for file_name in file_names:
        open(file_name, 'w')

        with open(file_name, 'rb') as open_file:
            headers = {'Content-type': 'multipart/form-data', 'Slug': file_name}
            r = requests.put('http://localhost:5000', files={'file': open_file}, headers=headers)
            print(r.status_code)
        remove(file_name)


if __name__ == '__main__':
    main()
