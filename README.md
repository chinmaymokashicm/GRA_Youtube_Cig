# Aggregating Youtube Search and Video Data and Metadata
This project is to pull Youtube data, organize and analyze Youtube search data as well as video metadata and comments.

## Modules
* data: Parent Class
* search: Class for search related code
* video: Class for video related code

## Variables
For the code to work, create a variables.yaml file in the root directory.
These variables must be present:
- api_key
- dir_results
- youtube_api_name
- youtube_version
- save_file_results_separator
- save_file_whitespace_substitute
- query_terms (list)
- number_of_search_results
- number_of_comment_threads