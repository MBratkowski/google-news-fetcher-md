# News Fetcher

This is a Python script that fetches news articles from Google News based on a user-specified keyword and time period.
The news articles are saved in Markdown format.

## Requirements

- Python 3.6 or higher
- `requests` library

## Usage

1. Run the `news.py` script.
2. When prompted, enter the keyword for the news articles you want to fetch.
3. Enter the number of months you want to go back in time for the news articles.

The script will fetch the news articles and save them in the `result` directory. Each month's news articles are saved in
a separate Markdown file. A summary of all the news articles is saved in `output.md` in the `result` directory.

## Example

Here's an example of how to use the script:

```bash
python news.py
Enter the keyword: python
Enter the number of months: 3
```

This will fetch news articles related to "python" from the last 3 months.

## Note

The script uses the Google News RSS feed to fetch the news articles. The number of articles and the time period covered
may vary based on the keyword and Google's RSS feed.