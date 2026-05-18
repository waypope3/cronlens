# cronlens

> Human-readable cron expression parser and next-run visualizer for the terminal

---

## Installation

```bash
pip install cronlens
```

---

## Usage

Parse a cron expression and visualize upcoming run times:

```bash
cronlens "*/15 9-17 * * 1-5"
```

**Output:**

```
Expression : */15 9-17 * * 1-5
Description: Every 15 minutes, between 09:00 and 17:00, Monday through Friday

Next 5 runs:
  1. Mon, 14 Jul 2025  09:00
  2. Mon, 14 Jul 2025  09:15
  3. Mon, 14 Jul 2025  09:30
  4. Mon, 14 Jul 2025  09:45
  5. Mon, 14 Jul 2025  10:00
```

Show more upcoming runs with the `--count` flag:

```bash
cronlens "0 0 * * *" --count 10
```

Use `--from` to preview runs starting from a specific date:

```bash
cronlens "30 8 1 * *" --from "2025-09-01"
```

---

## Options

| Flag | Description |
|-------------|--------------------------------------|
| `--count N` | Number of next runs to display (default: 5) |
| `--from DATE` | Start date for run preview (ISO format) |
| `--utc` | Display times in UTC |

---

## License

MIT © cronlens contributors