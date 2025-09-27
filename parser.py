import re
import json
from datetime import datetime
from collections import defaultdict
from common import Unknown

class KindleClippingsParser:
    def __init__(self):
        self.books = defaultdict(list)
    
    def parse_file(self, file_path):
        """解析 My Clippings.txt 文件，支持中英文格式"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='utf-8-sig') as file:
                content = file.read()
        
        entries = content.split('==========')
        
        for entry in entries:
            self._parse_entry(entry)
        
        return self
    
    def _parse_entry(self, entry):
        """解析单个摘录条目"""
        entry = entry.strip()
        if not entry:
            return
        
        lines = [line.strip() for line in entry.split('\n') if line.strip()]
        
        if len(lines) < 3:
            return
        
        # 提取书籍信息
        book_info = self._extract_book_info(lines[0])
        meta_info = self._extract_meta_info(lines[1])
        content = '\n'.join(lines[2:])
        
        if book_info and meta_info and content:
            note = {
                'content': content,
                'page': meta_info['page'],
                'location': meta_info['location'],
                'date': meta_info['date'],
                'time': meta_info['time']
            }
            self.books[book_info].append(note)
    
    def _extract_book_info(self, line):
        """提取书籍信息"""
        line = line.replace('\ufeff', '').strip()
        return line
    
    def _extract_meta_info(self, line):
        """提取元数据信息，支持中英文格式"""
        # 判断是中文格式还是英文格式
        if '您在第' in line and '的标注' in line:
            return self._parse_chinese_format(line)
        else:
            return self._parse_english_format(line)
    
    def _parse_chinese_format(self, line):
        """解析中文格式的元数据"""
        # 示例：- 您在第 15 页（位置 #229-230）的标注 | 添加于 2021年11月27日星期六 下午10:20:56
        
        # 提取页码
        page_match = re.search(r'第\s*(\d+)\s*页', line)
        # 提取位置
        location_match = re.search(r'位置\s*#(\d+-\d+)', line)
        # 提取日期时间
        datetime_match = re.search(r'添加于\s*(.+)', line)
        
        meta_info = {
            'page': page_match.group(1) if page_match else Unknown,
            'location': location_match.group(1) if location_match else Unknown,
            'date': Unknown,
            'time': Unknown
        }
        
        if datetime_match:
            datetime_str = datetime_match.group(1)
            try:
                # 解析中文日期时间格式：2021年11月27日星期六 下午10:20:56
                # 移除星期几信息
                datetime_str = re.sub(r'星期[一二三四五六日]', '', datetime_str).strip()
                
                # 处理上午/下午
                if '下午' in datetime_str:
                    datetime_str = datetime_str.replace('下午', 'PM')
                elif '上午' in datetime_str:
                    datetime_str = datetime_str.replace('上午', 'AM')
                
                # 解析日期时间
                datetime_obj = datetime.strptime(datetime_str, '%Y年%m月%d日 %p%I:%M:%S')
                
                # 分离日期和时间
                meta_info['date'] = datetime_obj.strftime('%Y-%m-%d')
                meta_info['time'] = datetime_obj.strftime('%H:%M:%S')
            except Exception as e:
                print(f"Chinese Datetime Parse Error: {datetime_str} - {e}")
        
        return meta_info
    
    def _parse_english_format(self, line):
        """解析英文格式的元数据"""
        # 示例：- Your Highlight on page 37 | Location 347-348 | Added on Thursday, August 21, 2025 6:02:11 AM
        
        # 提取页码
        page_match = re.search(r'page\s*(\d+)', line)
        # 提取位置
        location_match = re.search(r'Location\s*(\d+-\d+)', line)
        # 提取日期时间
        datetime_match = re.search(r'Added on\s*(.+)', line)
        
        meta_info = {
            'page': page_match.group(1) if page_match else Unknown,
            'location': location_match.group(1) if location_match else Unknown,
            'date': Unknown,
            'time': Unknown
        }
        
        if datetime_match:
            datetime_str = datetime_match.group(1)
            try:
                # 解析英文日期时间格式：Thursday, August 21, 2025 6:02:11 AM
                datetime_obj = datetime.strptime(datetime_str, '%A, %B %d, %Y %I:%M:%S %p')
                
                # 分离日期和时间
                meta_info['date'] = datetime_obj.strftime('%Y-%m-%d')
                meta_info['time'] = datetime_obj.strftime('%H:%M:%S')
            except Exception as e:
                print(f"English Datetime Parse Error: {datetime_str} - {e}")
        
        return meta_info

    def export_to_json(self):
        """导出JSON"""
        result = []
        
        for book_title, notes in self.books.items():
            book_data = {
                "book_name": book_title,
                "clippings": []
            }
            
            for i, note in enumerate(notes, 1):
                clipping_data = {
                    "id": i,
                    "content": note['content'],
                    "page": note['page'],
                    "location": note['location'],
                    "date": note['date'],
                    "time": note['time']
                }
                book_data["clippings"].append(clipping_data)
            
            result.append(book_data)
        
        return result
    
    def export_to_json_file(self, output_file="kindle_clippings.json"):
        """导出为JSON文件，格式符合要求"""
        result = []
        
        for book_title, notes in self.books.items():
            book_data = {
                "book_name": book_title,
                "clippings": []
            }
            
            for i, note in enumerate(notes, 1):
                clipping_data = {
                    "id": i,
                    "content": note['content'],
                    "page": note['page'],
                    "location": note['location'],
                    "date": note['date'],
                    "time": note['time']
                }
                book_data["clippings"].append(clipping_data)
            
            result.append(book_data)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"Generate JSON File: {output_file}")
        
        # 显示统计信息
        self._show_statistics(result)
        
        return result
    
    def _show_statistics(self, result):
        """显示统计信息"""
        total_books = len(result)
        total_clippings = sum(len(book['clippings']) for book in result)
        
        print(f"Total {total_books} book(s), {total_clippings} clipping(s)")
        
        for book in result:
            print(f"  {book['book_name']}: {len(book['clippings'])} clipping(s)")
        
        print()
