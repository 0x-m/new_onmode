def persian_slugify(txt: str):
    slug = ''
    for c in txt:
        if c not in [' ', ' ', '?', '(', ')', '%', '٪']:
            slug += c
        else:
            slug += '-'
    return slug