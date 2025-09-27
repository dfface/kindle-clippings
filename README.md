# Kindle Clippings

## Intro

Parse "My Clippings.txt" (now support Chinese and English of Kindle) to JSON like:

```json
[
  {
    "book_name": "Three Body",
    "clippings": [
      {
        "id": 1,
        "content": "I really like it",
        "page": "37",
        "location": "347-348",
        "date": "2025-08-21",
        "time": "06:02:11"
      },
      {
        "id": 2,
        "content": "I really like it",
        "page": "40",
        "location": "375-376",
        "date": "2025-08-21",
        "time": "06:05:25"
      }
    ]
  }
]
```

Convert to your custom format, for example:

```txt
Three Body
============================================================

1. I really like it
[page 37, position 347-348, 2025-08-21 06:02:11]

1. I really like it
[page 40, position 375-376, 2025-08-21 06:05:25]
```

Or you want to establish a website using the parsed JSON data, do it yourself!

## Usage

Put "My Clipping.txt" in the same path of the program, then run:

```bash
python3 main.py
```

You can also write your own converter and `main.py`:

```python
from parser import KindleClippingsParser
from converter import KindleClippingsConverter

def main():
    # file path
    clippings_file = "My Clippings.txt"

    # parse to JSON
    parser = KindleClippingsParser()
    parsed = parser.parse_file(clippings_file)
    json_data = parsed.export_to_json()
    # or you want a json file
    # parsed.export_to_json_file()

    # output txt
    converter = KindleClippingsConverter(json_data)
    converter.generate_content_txt()
    # you can write your function in converter.py
    # converter.generate_english_txt()
    # converter.generate_chinese_txt()

if __name__ == "__main__":
    main()
```
