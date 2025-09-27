from parser import KindleClippingsParser
from converter import KindleClippingsConverter

def main():
    # file path
    clippings_file = "My Clippings.txt"

    # parse to JSON
    parser = KindleClippingsParser()
    parser.parse_file(clippings_file)
    json_data = parser.export_to_json()
    # or you want a json file
    # parser.export_to_json_file()

    # output txt
    converter = KindleClippingsConverter(json_data)
    converter.generate_content_txt()
    # you can write your function in converter.py
    # converter.generate_english_txt()
    # converter.generate_chinese_txt()

if __name__ == "__main__":
    main()