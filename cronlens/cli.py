"""Command-line interface for cronlens."""

import argparse
import sys
from datetime import datetime

from cronlens.parser import CronExpression, ParseError
from cronlens.humanizer import humanize
from cronlens.next_run import next_runs
from cronlens.formatter import print_summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cronlens",
        description="Human-readable cron expression parser and next-run visualizer.",
    )
    parser.add_argument(
        "expression",
        help='Cron expression in quotes, e.g. "*/5 * * * *"',
    )
    parser.add_argument(
        "-n",
        "--count",
        type=int,
        default=5,
        metavar="N",
        help="Number of upcoming runs to display (default: 5)",
    )
    parser.add_argument(
        "--from",
        dest="from_dt",
        metavar="DATETIME",
        help='Start datetime for next-run calculation, e.g. "2024-01-15 08:00"',
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output",
    )
    return parser


def parse_from_dt(value: str) -> datetime:
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    raise ValueError(f"Cannot parse datetime: {value!r}")


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        expr = CronExpression.parse(args.expression)
    except ParseError as exc:
        print(f"cronlens: parse error: {exc}", file=sys.stderr)
        return 1

    from_dt = datetime.now()
    if args.from_dt:
        try:
            from_dt = parse_from_dt(args.from_dt)
        except ValueError as exc:
            print(f"cronlens: {exc}", file=sys.stderr)
            return 1

    description = humanize(expr)
    runs = next_runs(expr, n=args.count, after=from_dt)
    print_summary(
        expression=args.expression,
        description=description,
        runs=runs,
        color=not args.no_color,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
