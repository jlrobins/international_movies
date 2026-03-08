import json
import re
from dataclasses import asdict, dataclass
from typing import Optional

import praw


@dataclass
class Comment:
    author: str
    body: str
    score: int
    depth: int
    replies: list["Comment"]


@dataclass
class Post:
    id: str
    title: str
    author: str
    subreddit: str
    url: str
    selftext: str
    score: int
    num_comments: int
    comments: list[Comment]


def fetch_post(
    reddit: praw.Reddit, url_or_id: str, limit: Optional[int] = 32
) -> Post:
    """
    Fetch a Reddit post and all its comments.

    Args:
        reddit: praw.Reddit instance
        url_or_id: Full Reddit post URL or just the post ID
        limit: How many comment trees to expand (0=none, None=all). Default 32.

    Returns:
        Post object with all comments in a tree structure
    """
    # Handle both full URLs and post IDs
    if url_or_id.startswith("http"):
        submission = reddit.submission(url=url_or_id)
    else:
        submission = reddit.submission(id=url_or_id)

    # Expand "more comments" placeholders
    submission.comments.replace_more(limit=limit)

    # Build the comment tree
    comments = _build_comment_tree(submission.comments, depth=0)

    return Post(
        id=submission.id,
        title=submission.title,
        author=submission.author.name if submission.author else "[deleted]",
        subreddit=submission.subreddit.display_name,
        url=submission.url,
        selftext=submission.selftext,
        score=submission.score,
        num_comments=submission.num_comments,
        comments=comments,
    )


def _build_comment_tree(
    praw_comments: list, depth: int = 0
) -> list[Comment]:
    """
    Recursively build a Comment tree from PRAW comment forest.

    Args:
        praw_comments: List of praw.Comment objects (from submission.comments)
        depth: Current depth in the tree

    Returns:
        List of Comment objects with nested replies
    """
    comments = []
    for praw_comment in praw_comments:
        # Handle deleted/removed comments
        author = (
            praw_comment.author.name
            if praw_comment.author
            else "[deleted]"
        )
        body = praw_comment.body

        # Recursively process replies
        replies = _build_comment_tree(praw_comment.replies, depth=depth + 1)

        comment = Comment(
            author=author,
            body=body,
            score=praw_comment.score,
            depth=depth,
            replies=replies,
        )
        comments.append(comment)

    return comments


def post_to_markdown(post: Post) -> str:
    """
    Format a Post as markdown for LLM consumption.

    Indents comments using blockquote markers for readability.
    """
    lines = []

    # Post header
    lines.append(f"# {post.title}")
    lines.append(f"\n**Author:** {post.author}")
    lines.append(f"**Subreddit:** r/{post.subreddit}")
    lines.append(f"**Score:** {post.score}")
    lines.append(f"**Comments:** {post.num_comments}")
    lines.append(f"**URL:** {post.url}")

    # Post body
    if post.selftext:
        lines.append(f"\n## Post Text\n")
        lines.append(post.selftext)

    # Comments
    if post.comments:
        lines.append(f"\n## Comments\n")
        lines.append(_format_comments_markdown(post.comments))

    return "\n".join(lines)


def _format_comments_markdown(comments: list[Comment], indent: str = "") -> str:
    """Helper to recursively format comments as markdown with indentation."""
    lines = []
    for comment in comments:
        # Use blockquote for indentation
        prefix = "> " * (comment.depth + 1)
        lines.append(f"{prefix}**{comment.author}** ({comment.score} points)")

        # Split comment body into lines and indent each one
        for body_line in comment.body.split("\n"):
            lines.append(f"{prefix}{body_line}")

        lines.append("")  # blank line between comments

        # Recursively add replies
        if comment.replies:
            lines.append(_format_comments_markdown(comment.replies, indent=indent))

    return "\n".join(lines)


def post_to_json(post: Post) -> str:
    """
    Serialize a Post to JSON with full structure and metadata.
    """
    return json.dumps(asdict(post), indent=2)
