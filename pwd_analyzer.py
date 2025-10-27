#!/usr/bin/env python3
"""
Password Strength Analyzer + Simple Custom Wordlist Generator
Dependencies: pip install zxcvbn-python
Usage:
  python pwd_analyzer.py --check 'P@ssw0rd' --gen --name Swapnil --year 1998
"""

import argparse
from zxcvbn import zxcvbn
import itertools
import sys
from datetime import datetime

def analyze(pw):
    res = zxcvbn(pw)
    score = res.get("score")           # 0-4
    entropy = res.get("entropy")
    crack_time = res.get("crack_times_display", {}).get("offline_slow_hashing_1e4_per_second","unknown")
    feedback = res.get("feedback", {})
    suggestions = feedback.get("suggestions", [])
    warning = feedback.get("warning","")
    return {
        "password": pw,
        "score": score,
        "entropy": entropy,
        "crack_time": crack_time,
        "warning": warning,
        "suggestions": suggestions
    }

def print_analysis(a):
    print(f"\nPassword: {a['password']}")
    print(f"Score (0-4): {a['score']}")
    entropy = a['entropy'] if a['entropy'] is not None else 0
    print(f"Estimated entropy: {entropy:.2f} bits")
    print(f"Estimated crack time (display): {a['crack_time']}")
    if a['warning']:
        print("Warning:", a['warning'])
    if a['suggestions']:
        print("Suggestions:")
        for s in a['suggestions']:
            print(" -", s)


def simple_wordlist(name=None, pet=None, years=None, extra=None, max_items=2000):
    parts = []
    if name:
        parts.append(name)
    if pet:
        parts.append(pet)
    if extra:
        parts += extra.split(",")
    years = years or []
    words = set()
    # combine simple patterns
    for base in parts:
        if not base:
            continue
        base = base.strip()
        words.add(base)
        words.add(base.lower())
        words.add(base.capitalize())
        words.add(base.upper())
        # leet variants (basic)
        words.add(base.replace('a','4').replace('o','0').replace('e','3'))
    for y in years:
        for b in list(words):
            words.add(b + str(y))
            words.add(str(y) + b)
    # add numeric tails
    for i in range(0,100):
        for b in list(words)[:50]:
            words.add(b + str(i))
    # limit size
    wl = list(words)
    return wl[:max_items]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', help='Password to check', default=None)
    parser.add_argument('--gen', help='Generate custom wordlist', action='store_true')
    parser.add_argument('--name', help='User name or target name', default=None)
    parser.add_argument('--pet', help='Pet name', default=None)
    parser.add_argument('--years', help='Comma separated years e.g. 1990,1998', default=None)
    parser.add_argument('--extra', help='Comma separated extra bases', default=None)
    parser.add_argument('--out', help='wordlist output filename', default='wordlist.txt')
    args = parser.parse_args()

    if args.check:
        a = analyze(args.check)
        print_analysis(a)

    if args.gen:
        years = [y.strip() for y in (args.years.split(",") if args.years else []) if y.strip()]
        wl = simple_wordlist(name=args.name, pet=args.pet, years=years, extra=args.extra)
        with open(args.out, 'w', encoding='utf-8') as f:
            for w in wl:
                f.write(w + "\n")
        print(f"\nGenerated wordlist: {args.out} ({len(wl)} items)")

if __name__ == '__main__':
    main()
