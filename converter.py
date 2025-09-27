from datetime import datetime
import os
import re


class KindleClippingsConverter:
    def __init__(self, json_data):
        self.json_data = json_data
    
    def _convert_date_format(self, date_str, format_str='%Y-%m-%d'):
        """
        将日期从 YYYY-MM-DD 格式转换为 自定义（如YYYY年MM月DD日） 格式
        
        Args:
            date_str: 日期字符串，格式为 YYYY-MM-DD
            
        Returns:
            格式化后的日期字符串
        """
        if date_str == "Unknown Date":
            return date_str
        
        try:
            # 解析日期
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            # 格式化为其他格式的日期
            formatted_date = date_obj.strftime(format_str)
            return formatted_date
        except ValueError:
            # 如果解析失败，返回原日期
            return date_str
        
    def _format_each_clipping(self, id, content, page, location, date, time, date_format_template, clipping_format_template) -> str:
        formatted_date = self._convert_date_format(date, date_format_template)
        return clipping_format_template.format(id=id, content=content, page=page, location=location, formatted_date=formatted_date, time=time)
    
    def generate_txt_file_for_each_book(self, date_format_template, clipping_format_template, clipping_format_template_without_page, output_dir):
        """generate txt file for each book from JSON data"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # for each book
        for book_data in self.json_data:
            book_name = book_data.get("book_name", "Unknown Book")
            clippings = book_data.get("clippings", [])
            
            # generate safe file name
            safe_filename = re.sub(r'[<>:"/\\|?*]', '', book_name)
            safe_filename = safe_filename.replace(' ', '_')[:100]  # limit length of file name
            file_path = os.path.join(output_dir, f"{safe_filename}.txt")
            
            # write txt file
            with open(file_path, 'w', encoding='utf-8') as f:
                # write book name
                f.write(f"{book_name}\n")
                f.write("=" * 60 + "\n\n")
                
                # write each clipping
                for i, clipping in enumerate(clippings, 1):
                    id = clipping.get("id", i)
                    content = clipping.get("content", "")
                    page = clipping.get("page", "Unknown")
                    location = clipping.get("location", "Unknown")
                    date = clipping.get("date", "Unknown Date")
                    time = clipping.get("time", "Unknown Time")
                    
                    format_clipping = self._format_each_clipping(id=id, content=content, page=page, location=location, date=date, time=time, date_format_template=date_format_template, clipping_format_template=clipping_format_template)
                    # write formatted clipping
                    if page == "Unknown":
                        format_clipping = self._format_each_clipping(id=id, content=content, page=page, location=location, date=date, time=time, date_format_template=date_format_template, clipping_format_template=clipping_format_template_without_page)
                    f.write(format_clipping)
            
            print(f"Already generated: {file_path}")
        
        print(f"\nDone! Total {len(self.json_data)} book(s)")

    def generate_english_txt(self, output_dir="output"):
        """generate txt file for each book from JSON data"""
        self.generate_txt_file_for_each_book(output_dir=output_dir, date_format_template="%B %d, %Y",
                                             clipping_format_template="{id}. {content}\n[page {page}, position {location}, {formatted_date} {time}]\n\n",
                                             clipping_format_template_without_page="{id}. {content}\n[position {location}, {formatted_date} {time}]\n\n")
    
    def generate_chinese_txt(self, output_dir="output"):
        self.generate_txt_file_for_each_book(output_dir=output_dir, date_format_template="%Y年%m月%d日", 
                                             clipping_format_template="{id}. {content}\n（第{page}页，{location}位置，{formatted_date} {time}）\n\n",
                                             clipping_format_template_without_page="{id}. {content}\n（{location}位置，{formatted_date} {time}）\n\n")