import csv
import re

f = open('./review_data/review1.csv', 'r')
rdr = csv.reader(f)

sqlFile = open('./review_data/sql.txt', 'w')

for line in rdr:
    print(line)
    id = line[1]
    id = re.sub('[^ A-Za-z0-9가-힣]', '', id)

    content = line[4]
    content = re.sub('[^ A-Za-z0-9가-힣]', '', content)

    created_at = line[8]
    
    user_name = line[2]
    user_name = re.sub('[^ A-Za-z0-9가-힣]', '', user_name)
    
    source_type = 'PLAYSTORE'
    like_count = 0
    sql = f"INSERT INTO REVIEW (id, content, created_at, username, source_type, like_count) value ('{id}', '{content}', '{created_at}', '{user_name}', '{source_type}', {like_count});\n"
    sqlFile.write(sql)
    



sqlFile.close()
f.close()
