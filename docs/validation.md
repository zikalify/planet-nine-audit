# Validation record

Executed locally on 27 October 2026, Python 3.10:

- 26 automated tests passed (`python3 -m unittest discover -s tests -v`).
- Synthetic example output exactly reproduced byte-for-byte.
- Full Caltech v3 reference population downloaded from its record's own CSV link.
- Source MD5 verified against the live published record.
- 100,000 source rows parsed with binary flag and uniqueness checks.
- JSON summary reproduced exactly on a second run.
- Independent set-union implementation matched the 78,260-particle published-flag union.
- No source population redistributed, no credential included, no network actions in library runtime.

Not validated: new selection functions, real follow-up rankings, orbit predictions, scientific novelty, telescope usability, statistical calibration of any new astronomical inference. Unit tests do not certify these.
