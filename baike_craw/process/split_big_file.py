import os

with open(os.path.join('../data/xinguan_hudongbaike', 'entity_pages.xml'), 'r', encoding='utf-8') as f:
        chunk_data = f.read(250000000)
        i = 1
        while chunk_data != '':
            file_name = 'entity_pages_' + str(i) + '.xml'
            with open(os.path.join('../data/xinguan_hudongbaike', file_name),  'w', encoding='utf-8') as dest_f:
                dest_f.write(chunk_data)
                dest_f.close()
            chunk_data = f.read(250000000)
            i = i + 1