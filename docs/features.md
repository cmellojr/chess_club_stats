# Feature Map

> Auto-maintained index of every user-facing feature and the code path that implements it. Updated alongside the code — not after the fact.

## Club Stats

Display club information (name, description, country, member count, creation date, events count).

**Flow:**

1. `src/chessclub_cli/main.py:450` — `club stats <slug>` CLI command; parses `--output` flag
2. `src/chessclub/services/club_service.py:28` — `ClubService.get_club()` pass-through
3. `src/chessclub/providers/chesscom/client.py:75` or `src/chessclub/providers/lichess/client.py:100` — `get_club()` fetches from API and maps to `Club` model
4. `src/chessclub_cli/main.py:469-538` — Renders `Club` as Rich `Panel`, JSON, or CSV

---

## Club Members

List club members with activity tier (weekly/monthly/inactive), join date, optional title enrichment.

**Flow:**

1. `src/chessclub_cli/main.py:554` — `club members <slug>` CLI command
2. `src/chessclub/services/club_service.py:50` — `ClubService.get_club_members()` pass-through
3. `src/chessclub/providers/chesscom/client.py:103` or `src/chessclub/providers/lichess/client.py:118` — Fetches members, enriches with profile data when `with_details=True`
4. `src/chessclub_cli/main.py:587-623` — Renders as Rich `Table`, JSON, or CSV

---

## Club Tournaments

List tournaments organised by the club. Supports `--details` (per-player standings) and `--games <ref>` (show games for a specific tournament by index, name, or ID).

**Flow:**

1. `src/chessclub_cli/main.py:626` — `club tournaments <slug>` CLI command
2. `src/chessclub/services/club_service.py:65` — `ClubService.get_club_tournaments()` pass-through
3. `src/chessclub/providers/chesscom/client.py:152` or `src/chessclub/providers/lichess/client.py:156` — Paginated tournament fetch from internal/callback APIs
4. `src/chessclub_cli/main.py:803-901` — Renders tournament list with optional standings tables, JSON, or CSV; `--games` branch renders game tables with accuracy stats

---

## Club Games

List tournament games ranked by Stockfish accuracy (best first). Supports `--last-n` and `--min-accuracy` filters.

**Flow:**

1. `src/chessclub_cli/main.py:904` — `club games <slug>` CLI command
2. `src/chessclub/services/club_service.py:148` — `ClubService.get_club_games()` pass-through
3. `src/chessclub/providers/chesscom/client.py:520` or `src/chessclub/providers/lichess/client.py:224` — Fetches tournaments, resolves participants, queries per-player game archives, deduplicates
4. `src/chessclub_cli/main.py:960-1036` — Renders as Rich `Table`, JSON, or CSV with accuracy columns

---

## Club Leaderboard

Aggregate tournament results into a ranked leaderboard by year, month, or all time.

**Flow:**

1. `src/chessclub_cli/main.py:1043` — `club leaderboard <slug>` CLI command
2. `src/chessclub/services/leaderboard_service.py:22` — `LeaderboardService.get_leaderboard()` filters tournaments by date, aggregates scores
3. `src/chessclub/providers/chesscom/client.py:152` or `src/chessclub/providers/lichess/client.py:156` — Tournament list
4. `src/chessclub/providers/chesscom/client.py:207` or `src/chessclub/providers/lichess/client.py:175` — Per-tournament results
5. `src/chessclub_cli/main.py:1099-1141` — Renders ranked `PlayerStats` as Rich `Table`, JSON, or CSV

---

## Club Matchups

Head-to-head records between club members from tournament games.

**Flow:**

1. `src/chessclub_cli/main.py:1149` — `club matchups <slug>` CLI command
2. `src/chessclub/services/matchup_service.py:24` — `MatchupService.get_matchups()` tallies win/loss/draw per player pair
3. `src/chessclub/providers/chesscom/client.py:520` or `src/chessclub/providers/lichess/client.py:224` — Club games
4. `src/chessclub_cli/main.py:1199-1237` — Renders `Matchup` records as Rich `Table`, JSON, or CSV

---

## Club Attendance

Rank players by tournament attendance percentage, current streak, and longest streak.

**Flow:**

1. `src/chessclub_cli/main.py:1245` — `club attendance <slug>` CLI command
2. `src/chessclub/services/attendance_service.py:17` — `AttendanceService.get_attendance()` builds per-player attendance bitmap
3. `src/chessclub/providers/chesscom/client.py:152` or `src/chessclub/providers/lichess/client.py:156` — Tournament list
4. `src/chessclub/providers/chesscom/client.py:207` or `src/chessclub/providers/lichess/client.py:175` — Per-tournament results
5. `src/chessclub_cli/main.py:1292-1330` — Renders `AttendanceRecord` as Rich `Table`, JSON, or CSV

---

## Club Records

Show notable club highlights: highest tournament score, most tournaments played, most wins, biggest tournament, best game accuracy.

**Flow:**

1. `src/chessclub_cli/main.py:1338` — `club records <slug>` CLI command
2. `src/chessclub/services/records_service.py:19` — `RecordsService.get_records()` computes tournament-based and game-based records
3. `src/chessclub/providers/chesscom/client.py:152` or `src/chessclub/providers/lichess/client.py:156` — Tournament list
4. `src/chessclub/providers/chesscom/client.py:404` or `src/chessclub/providers/lichess/client.py:195` — Per-tournament games for accuracy records
5. `src/chessclub_cli/main.py:1388-1416` — Renders `ClubRecord` as Rich `Table`, JSON, or CSV

---

## Player Rating History

Show a player's rating evolution across club tournaments (rating, position, score per tournament).

**Flow:**

1. `src/chessclub_cli/main.py:1424` — `player rating-history <username> --club <slug>` CLI command
2. `src/chessclub/services/rating_history_service.py:23` — `RatingHistoryService.get_rating_history()` scans tournaments, filters to target player
3. `src/chessclub/providers/chesscom/client.py:152` or `src/chessclub/providers/lichess/client.py:156` — Tournament list
4. `src/chessclub/providers/chesscom/client.py:207` or `src/chessclub/providers/lichess/client.py:175` — Per-tournament results
5. `src/chessclub_cli/main.py:1483-1523` — Renders `RatingSnapshot` list as Rich `Table`, JSON, or CSV

---

## Auth Setup (Cookie)

Save Chess.com session cookies (ACCESS_TOKEN + PHPSESSID) to disk.

**Flow:**

1. `src/chessclub_cli/main.py:262` — `auth setup` CLI command; prompts user for credentials
2. `src/chessclub/providers/chesscom/auth.py:49` — `ChessComCookieAuth` validates credentials against Chess.com
3. `src/chessclub/auth/credentials.py:27` — `save()` writes to `~/.config/chessclub/credentials.json`

---

## Auth Login (OAuth)

Authenticate via OAuth 2.0 PKCE + Loopback Local Server (RFC 8252).

**Flow:**

1. `src/chessclub_cli/main.py:313` — `auth login` CLI command; resolves `client_id`
2. `src/chessclub/providers/chesscom/auth.py:202` — `ChessComOAuth.run_login_flow()` starts loopback server, opens browser, exchanges code for tokens
3. `src/chessclub/auth/credentials.py:89` — `save_oauth_token()` writes to `~/.config/chessclub/oauth_token.json`

---

## Auth Status

Show status of all configured credentials (OAuth token expiry, cookie session path).

**Flow:**

1. `src/chessclub_cli/main.py:350` — `auth status` CLI command
2. `src/chessclub/auth/credentials.py:126,48` — `load_oauth_token()` and `load()` check disk
3. `src/chessclub/providers/chesscom/auth.py:49,202` — `ChessComCookieAuth` and `ChessComOAuth` validate credentials
4. `src/chessclub_cli/main.py:357-428` — Renders status report with expiry, scopes, credential source

---

## Auth Clear

Remove all locally saved credentials.

**Flow:**

1. `src/chessclub_cli/main.py:431` — `auth clear` CLI command
2. `src/chessclub/auth/credentials.py:63,142` — `clear()` and `clear_oauth_token()` remove credential files

---

## Cache Stats

Show SQLite cache statistics (entry count, active/expired, database size).

**Flow:**

1. `src/chessclub_cli/main.py:1531` — `cache stats` CLI command
2. `src/chessclub/providers/cache.py:178` — `SQLiteCache.stats()` queries cache table and file size
3. `src/chessclub_cli/main.py:1537-1547` — Renders stats (entries, location, KB)

---

## Cache Clear

Clear cached API responses (all entries or expired-only).

**Flow:**

1. `src/chessclub_cli/main.py:1550` — `cache clear [--expired]` CLI command
2. `src/chessclub/providers/cache.py:151,163` — `SQLiteCache.clear()` or `purge_expired()`
3. `src/chessclub_cli/main.py:1567-1574` — Reports count of removed entries
