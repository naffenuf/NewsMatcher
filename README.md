# NewsMatcher

NewsMatcher is a set of Python scripts that work in sequence to pull a collection of news articles, index them, and match them by story. The result is a JSON file containing an array of stories, with each story including all related articles.

## Overview

Currently, NewsMatcher uses RSS feeds to gather articles. However, the long-term goal is to implement a more user-controlled method for news gathering.

### Key Features:
- Automated news article collection from RSS feeds
- Article indexing for efficient processing
- Story matching algorithm to group related articles
- JSON output for easy integration with other systems

### How it Works:
1. Fetches articles from configured RSS feeds
2. Indexes the collected articles
3. Applies a matching algorithm to group articles into stories
4. Outputs a JSON file with an array of stories, each containing related articles

## Installation

1. Clone this repository
2. Navigate to the project directory
3. Create and activate a virtual environment
4. Install requirements.txt

## Usage

Run the main pipeline script:
python pipeline.py

## Customization

To add or modify RSS feeds, edit the `rss_feeds.json` file in the project directory.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you have any questions, suggestions, or feedback, please don't hesitate to reach out:

- Email: naffenuf@yahoo.com
- GitHub Issues: [Create an issue](https://github.com/yourusername/NewsMatcher/issues)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

NewsMatcher is provided as-is, without any warranties or guarantees. Users are responsible for complying with all applicable laws and regulations regarding the use and distribution of news content.
