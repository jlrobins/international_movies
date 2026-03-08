# Reddit Scraper — International Movie Recommendations

A project to discover and track international movie recommendations scraped from Reddit discussions, with an interactive web interface for browsing and curating your watchlist.

## Overview

This project combines Reddit data collection with a polished single-page application (SPA) to help users explore international cinema recommendations. The workflow is:

1. **Scrape** — Extract movie recommendations and comments from Reddit threads using PRAW
2. **Process** — Round-trip the scraped comment data through Claude to extract and structure movie information (title, country, genre, summary)
3. **Explore** — Browse the curated collection via an interactive web interface with filtering, sorting, and tracking

## Project Structure

### Backend (Python)

- **`utils.py`** — Reddit scraper initialization via PRAW
  - Credentials managed via `.env` (not committed to repo)
  - `create_praw()` returns an authenticated Reddit client

- **`.env`** — Environment variables for Reddit API credentials
  - Not tracked in git for security
  - Required variables: `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `REDDIT_USER_AGENT`, `REDDIT_USERNAME`, `REDDIT_PASSWORD`

### Frontend (JavaScript SPA)

Located in `docs/` for GitHub Pages hosting:

- **`docs/index.html`** — Single-page application with all logic (HTML, CSS, JavaScript)
- **`docs/movies.json`** — Movie data (96 entries: id, title, country, genre, summary)
- **`dev_server.sh`** — Local development server (serves from `docs/` on localhost:8080)

## Features

### Data Model

- **Single enum status per movie**: `undefined | 'want' | 'seen' | 'skip'` (mutually exclusive)
- **localStorage persistence** — User selections saved and restored across sessions
- **Automatic migration** — Converts old multi-key format to single consolidated key

### SPA Capabilities

- **Dual-checkbox + skip tracking** — Mark movies as "Want to see", "Seen", or "Skip"
- **Multi-column sorting** — 9 sort options:
  - Want (↑/↓), Seen (↑/↓), Skip (↑/↓)
  - Title, Country, Genre, Comments Summary (↑/↓ each)
  - Country + Genre (combined sort)
- **Live search** — Case-insensitive substring filtering across Title, Country, Genre
- **Filter select** — View All, Seen only, Wanted only, or Skipped movies
- **IMDB links** — Click any title to search IMDB in a new tab
- **Responsive table** — Clean, accessible layout with hover states

## Setup

### Install Dependencies

```bash
uv sync
```

This installs:

- `praw` — Reddit API wrapper
- `python-dotenv` — Environment variable loading

### Configure Credentials

1. Create a `.env` file in the project root:

   ```
   REDDIT_CLIENT_ID=your_client_id
   REDDIT_CLIENT_SECRET=your_client_secret
   REDDIT_USER_AGENT=your_user_agent
   REDDIT_USERNAME=your_username
   REDDIT_PASSWORD=your_password
   ```

2. Obtain credentials from [Reddit's app registration page](https://www.reddit.com/prefs/apps)

### Run the SPA Locally

```bash
./dev_server.sh
```

Opens `http://localhost:8080/international_movies_table.html` in your browser.

## Data Generation Workflow

The `movies.json` file was created by:

1. **Scraping** Reddit threads with PRAW to extract movie recommendations and associated comment threads
2. **Round-tripping through Claude** — Passing the raw comment data to Claude's API to intelligently extract and structure:
   - Movie titles
   - Countries of origin
   - Genres
   - Natural-language summaries from community comments
3. **Exporting** the processed results as a clean JSON array

This hybrid human-AI approach ensures high-quality, contextually accurate data while leveraging Claude's language understanding for reliable information extraction.

## GitHub Pages Deployment

The `docs/` directory is configured as the GitHub Pages source:

1. Push to your repository
2. In repository Settings → Pages, select "Deploy from a branch" with `/docs` folder
3. Your site will be live at `https://<username>.github.io/reddit_scraper/`

## License

BSD 3-Clause License — see [LICENSE](LICENSE) file for details.
