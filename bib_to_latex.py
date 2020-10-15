import argparse
from pybtex.database import parse_file


def published_papers():
    bib_data = parse_file('_bibliography/papers.bib')

    strs = []

    accpeted_keys = []
    total_accepted = 0
    for key in bib_data.entries.keys():
        if bib_data.entries[key].fields['abbr'] == 'Preprint':
            continue
        total_accepted += 1
        accpeted_keys.append(key)

    for i, key in enumerate(accpeted_keys):
        if bib_data.entries[key].fields['abbr'] == 'Preprint':
            continue
        
        entry = bib_data.entries[key]
        title = '\\textbf{' + entry.fields['title'] + '}'
        try:
            booktitle = entry.fields['booktitle']
        except:
            booktitle = entry.fields['journal']
        if len(entry.fields['abbr']) < len(booktitle):
            abbr = ', (\\textbf{' + entry.fields['abbr'] + '})'
        else:
            abbr = ''
            
        if len(entry.fields.get('additional', '')) > 0:
            additional = ', \\textit{' + entry.fields.get('additional', '') + '}'
        else:
            additional = ''
        
        author_list = []
        for author in entry.persons['author']:
            if 'Song' in author.last_names[0] and 'Jiaming' in author.first_names[0]:
                author_list.append('\\textbf{' + author.first_names[0] + ' ' + author.last_names[0] + '}')
            else:
                author_list.append(author.first_names[0] + ' ' + author.last_names[0])
        
        author_list = ', '.join(author_list)
        
        strs.append(f'[{total_accepted - i}] & {author_list} \\\\\n & {title} \\\\\n & {booktitle}{abbr}{additional}')
        
    strs = '\\\\\n\\rule{0pt}{3ex}'.join(strs)
    return strs


def arxiv_papers():
    bib_data = parse_file('_bibliography/papers.bib')

    strs = []

    accpeted_keys = []
    total_accepted = 0
    for key in bib_data.entries.keys():
        if not (bib_data.entries[key].fields['abbr'] == 'Preprint'):
            continue
        total_accepted += 1
        accpeted_keys.append(key)

    for i, key in enumerate(accpeted_keys):
        if not (bib_data.entries[key].fields['abbr'] == 'Preprint'):
            continue
        
        entry = bib_data.entries[key]
        title = '\\textbf{' + entry.fields['title'] + '}'
        try:
            booktitle = entry.fields['booktitle']
        except:
            booktitle = entry.fields['journal']
        abbr = ''
            
        if len(entry.fields.get('additional', '')) > 0:
            additional = ', \\textit{' + entry.fields.get('additional', '') + '}'
        else:
            additional = ''
        
        author_list = []
        for author in entry.persons['author']:
            if 'Song' in author.last_names[0] and 'Jiaming' in author.first_names[0]:
                author_list.append('\\textbf{' + author.first_names[0] + ' ' + author.last_names[0] + '}')
            else:
                author_list.append(author.first_names[0] + ' ' + author.last_names[0])
        
        author_list = ', '.join(author_list)
        
        strs.append(f'[{total_accepted - i}] & {author_list} \\\\\n & {title} \\\\\n & {booktitle}{abbr}{additional}')
        
    strs = '\\\\\n\\rule{0pt}{3ex}'.join(strs)
    return strs
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--preprint', action='store_true')
    args = parser.parse_args()
    
    if args.preprint:
        strs = arxiv_papers()
    else:
        strs = published_papers()

    print(strs)