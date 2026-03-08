import argparse
import sys

from scraper import fetch_post, post_to_json, post_to_markdown
from utils import create_praw


def main():
    parser = argparse.ArgumentParser(
        description="Scrape a Reddit post and all its comments"
    )
    parser.add_argument("url", help="Reddit post URL or post ID")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON instead of markdown",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=32,
        help="Number of comment trees to expand (0=none, None=all). Default: 32",
    )

    args = parser.parse_args()

    try:
        reddit = create_praw()
        post = fetch_post(reddit, args.url, limit=args.limit)

        if args.json:
            output = post_to_json(post)
        else:
            output = post_to_markdown(post)

        print(output)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
