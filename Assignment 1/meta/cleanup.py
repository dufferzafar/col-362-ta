# sys.argv[1] contains dataset file

# file expected format

# v_type/v_name/p_name \t attr_id \t attr_name \t attr_value

import sys
from tqdm import tqdm
f = open(sys.argv[1])


paper_to_id = {}
id_to_paper = {}  # dict of dict with dict for each record

paper_cnt = 0

author_to_id = {}
id_to_author = {}  # dict of strings

author_cnt = 0

paper_by_authors = []  # 2 tuple list paperId,authorId

citation = []  # 2 tuple list c1 cites c2

id_to_venue = {}  # dict of dict
venue_to_id = {}
venue_cnt = 0


def parseRecord(s):
    global paper_cnt, venue_cnt, author_cnt
    a, b, c, d = s.rstrip().split('\t')
    if a == '' or b == '' or c == '' or d == '':
        print('dirty record')
        return
    temp_li = a.split('/')
    if len(temp_li) < 3:
        return
    v_type, v_name, p_name = temp_li
    if (v_type, v_name) not in venue_to_id:
        venue_to_id[(v_type, v_name)] = venue_cnt + 1
        id_to_venue[venue_cnt + 1] = {'name': v_name, 'type': v_type}
        venue_cnt += 1
    id_to_paper[paper_to_id[p_name]]['venue'] = venue_to_id[(v_type, v_name)]
    if c == 'author':
        if d not in author_to_id:
            author_to_id[d] = author_cnt + 1
            id_to_author[author_cnt + 1] = d
            author_cnt += 1
        paper_by_authors.append((paper_to_id[p_name], author_to_id[d]))
    if c == 'cite':
        p2 = d.split('/')[-1]
        if p2 not in paper_to_id:
            print('cited paper not in database')
            return
        citation.append((paper_to_id[p_name], paper_to_id[p2]))
    if c == 'title':
        id_to_paper[paper_to_id[p_name]]['title'] = d
    if c == 'year':
        id_to_paper[paper_to_id[p_name]]['year'] = d


for line in f:

    a, b, c, d = line.rstrip().split('\t')
    if a == '' or b == '' or c == '' or d == '':
        print('dirty record')
        continue
    temp_li = a.split('/')
    if len(temp_li) < 3:
        continue
    v_type, v_name, p_name = temp_li
    if p_name not in paper_to_id:
        paper_to_id[p_name] = paper_cnt + 1
        id_to_paper[paper_cnt + 1] = {}
        paper_cnt += 1
f = open(sys.argv[1])
for line in tqdm(f, ascii=True):
    parseRecord(line)



# print to tsv tables (tab seperated)

# order of attributes is same as in assignment pdf
f = open('Paper.tsv', 'w')
for i in id_to_paper:
    temp_dict = id_to_paper[i]
    if 'title' not in temp_dict or 'year' not in temp_dict or 'venue' not in temp_dict:
        print('Paper missing records')
        continue
    f.write("%d\t%s\t%s\t%d\n" % (i, temp_dict['title'], temp_dict['year'], temp_dict['venue']))
f.close()

f = open('Author.tsv', 'w')
for i in id_to_author:
    f.write("%d\t%s\n" % (i, id_to_author[i]))
f.close()

f = open('PaperByAuthors.tsv', 'w')
for i, j in paper_by_authors:
    f.write("%d\t%d\n" % (i, j))
f.close()

f = open('Citation.tsv', 'w')
for i, j in citation:
    f.write("%d\t%d\n" % (i, j))
f.close()

f = open('Venue.tsv', 'w')
for i in id_to_venue:
    temp_dict = id_to_venue[i]
    f.write("%d\t%s\t%s\n" % (i, temp_dict['name'], temp_dict['type']))
f.close()
