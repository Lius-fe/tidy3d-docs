from subprocess import run, CalledProcessError
from bs4 import BeautifulSoup
import nbformat
import yaml
import re
import glob
import os
import shutil
from nbconvert import HTMLExporter

output_dir = './html'

def creat_yaml(meta, anchor={}):
    data = {
        'layout': 'default',
        'custom_css': "cobalt",
        'custom_font': 'font2'
    }
    if 'title' in meta:
        data['title'] = meta['title']
    if 'description' in meta:
        data['description'] = meta['description']
    if 'keywords' in meta:
        data['tags'] = meta['keywords'].split(",")

    # 将字典转换为 YAML 格式
    return '---\n' + yaml.dump(data) + yaml.dump(anchor) + '---\n'

def read_template():
    # 读取 HTML 文件
    with open(f'./_template/template.html', 'r') as f:
        html = f.read()
        # 将 HTML 转换为 BeautifulSoup 对象
        return BeautifulSoup(html, 'html.parser')

def get_anchor_list(soup):
    '''
    h1, h2, h3 can be used to anchor
    '''
    anchor_dict = { "anchor_area": {} }
    h1 = soup.find('h1')
    if h1:
        anchor_dict['anchor_area']['key'] = h1.get('id')
        text = h1.get_text(strip=True)
        # 删除子节点的文本内容
        for child in h1.children:
            if child.name is not None:
                text = text.replace(child.get_text(strip=True), '')
        anchor_dict['anchor_area']['label'] = text
    h2 = soup.find_all('h2')
    if h2:
        anchor_dict['anchor_area']['list'] = []
        for tag in h2:
            dict = {}
            dict['key'] = tag.get('id')
            text = tag.get_text(strip=True)
            # 删除子节点的文本内容
            for child in tag.children:
                if child.name is not None:
                    text = text.replace(child.get_text(strip=True), '')
            dict['label'] = text
            anchor_dict['anchor_area']['list'].append(dict)
    return anchor_dict

def write_template(meta, input_file):
    with open(f'{output_dir}/{input_file}', 'r') as html_file:
        content = html_file.read()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')
        anchor = get_anchor_list(soup)
        for tag in soup.find_all('style'):
            tag.string = re.sub(r'body\s*{\s*(.*?)\s*}', '', tag.string, flags=re.DOTALL)
            tag.string = re.sub(r'html\s*{\s*(.*?)\s*}', '', tag.string, flags=re.DOTALL)
            # 删除 * 样式
            # tag.string = re.sub(r'\*\s*{\s*(.*?)\s*}', '', tag.string, flags=re.DOTALL)
            tag.string = re.sub(r', \*|,\*', '', tag.string, flags=re.DOTALL)
            # 删除 *::before 样式
            # tag.string = re.sub(r'\*\s*::before\s*{\s*(.*?)\s*}', '', tag.string, flags=re.DOTALL)
            tag.string = re.sub(r'\*\:\:before\,', '', tag.string, flags=re.DOTALL)
            # 删除 *::after 样式
            tag.string = re.sub(r'\*\s*::after\s*{\s*(.*?)\s*}', '', tag.string, flags=re.DOTALL)

        for script in soup.head.find_all('script'):
            if 'require.min.js' in str(script):
                script.decompose()
        # prompts = soup.find_all('div', class_='jp-InputPrompt jp-InputArea-prompt')
        # for dom in prompts:
        #     dom = re.sub(r'In [','[',str(dom),flags=re.DOTALL)
        # print(len(prompt))

        template_soup = read_template()
        insert_location = template_soup.find('main', {'id': 'notebook-container'})

        insert_location.append(soup)

        ouptut_html = str(template_soup)
        ouptut_html = ouptut_html.replace('In [','[')
        yam_str = creat_yaml(meta,anchor)
        with open(f'{output_dir}/{input_file}', 'w') as output_file:
            output_file.write(yam_str + str(ouptut_html))

# 获取当前目录下的所有 ipynb 文件
ipynb_files = glob.glob("*.ipynb")
shutil.rmtree(output_dir)

os.mkdir(output_dir)
# index = 0
# 遍历每个 ipynb 文件并读取内容
for input_file in ipynb_files:
    if input_file.endswith('.ipynb'):
        # 打印加粗的文本
        print(f'\033[1m [Converting] : {input_file}\033[0m')

        try:
            # 构建 nbconvert 命令字符串
            cmd = f"jupyter nbconvert --to htmls --output-dir {output_dir} {input_file} --embed-images"

            # 执行命令，并捕获输出和错误
            result = run(cmd, shell=True, capture_output=True, text=True, check=True)

            # 检查命令是否成功完成
            if result.returncode == 0:
                # 定义匹配一级标题的正则表达式
                with open(input_file, 'r', encoding='utf-8') as f:
                    nb = nbformat.read(f, as_version=4)
                    default_title = ""
                    for cell in nb.cells:
                        if cell.cell_type == 'markdown' and cell.source.startswith('#'):
                            _title = cell.source.strip('#').strip()
                            default_title = _title.split("\n")[0]
                            break
                    html_exporter = HTMLExporter()
                    # Modify the HTML title tag to use the notebook's metadata
                    metadata = nb['metadata']
                    title = metadata.get('title', default_title)
                    description = metadata.get('description', '')
                    keywords = metadata.get('keywords', '')
                    dict = {}
                    if title:
                        dict['title'] = title
                    if description:
                        dict['description'] = description
                    if keywords:
                        dict['keywords'] = keywords
                    write_template(dict, os.path.splitext(os.path.basename(input_file))[0]+'.html')
                    index = 1

            else:
                print("Failed to convert notebook to HTML.")
        except CalledProcessError as e:
            # 捕获异常并打印错误信息
            print(f"Command '{e.cmd}' returned non-zero exit status {e.returncode}: {e.stderr}")
            break
