create_table_if_not_exists = '''
CREATE TABLE IF NOT EXISTS search_results (
	id SERIAL PRIMARY KEY NOT NULL,
	search_request TEXT NOT NULL,
	repository_url TEXT NOT NULL,
	snippet_url TEXT NOT NULL,
	indexed_at TIMESTAMP,
	code_snippet TEXT
)
'''

add_new_record = '''
INSERT INTO search_results (
    search_request,
    repository_url,
    snippet_url,
    indexed_at,
    code_snippet
)
VALUES ($1, $2, $3, $4, $5)
'''
