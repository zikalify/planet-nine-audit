"""Audit published binary detectability flags, not new calibrated probabilities.

The source population is sampled, so equal weights are used for its rows.
No orbit propagation, simulation or automatic download is performed.
"""
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path

EXPECTED_MD5 = 'a38fa7579b4c9938b3deebecda55a845'
SOURCE = 'https://data.caltech.edu/records/8fjad-x7y61'


def summarize(path):
    data = path.read_bytes()
    md5 = hashlib.md5(data).hexdigest()
    if md5 != EXPECTED_MD5:
        raise ValueError('Not the verified Caltech v3 CSV: MD5 mismatch. Review changed data before use.')
    text = data.decode('utf-8')
    rows = csv.DictReader(io.StringIO('\n'.join(l for l in text.splitlines() if not l.startswith('#'))), skipinitialspace=True)
    expected = ['index','mass','a','e','inc','varpi','Omega','M','ra','dec','R','rad','albedo','V','ZTF','DES','PS1']
    if rows.fieldnames != expected:
        raise ValueError('Unexpected published CSV schema')
    counts = {'ZTF':0,'DES':0,'PS1':0,'any_search':0,'none':0}
    subsets = {f'{a}{b}{c}':0 for a in (0,1) for b in (0,1) for c in (0,1)}
    ids = set()
    for row in rows:
        key = int(row['index'])
        if key in ids:
            raise ValueError('Duplicate source row')
        ids.add(key)
        flags = [int(row[s]) for s in ('ZTF','DES','PS1')]
        if any(f not in (0,1) for f in flags):
            raise ValueError('Nonbinary published detectability flag')
        for s,f in zip(('ZTF','DES','PS1'),flags): counts[s] += f
        counts['any_search'] += int(any(flags))
        counts['none'] += int(not any(flags))
        subsets[''.join(map(str,flags))] += 1
    if len(ids) != 100000:
        raise ValueError('Unexpected reference population size')
    return {
        'source': SOURCE,
        'source_md5': md5,
        'source_sha256': hashlib.sha256(data).hexdigest(),
        'population_size': len(ids),
        'epoch_jd':2458270.0,
        'epoch_label':'1 June 2018; J2000 heliocentric osculating elements',
        'interpretation':'Historical reference-model fraction flagged detectable, NOT a new survey exclusion or discovery probability.',
        'counts':counts,
        'fractions':{k:v/len(ids) for k,v in counts.items()},
        'joint_flag_counts_ZTF_DES_PS1':subsets,
        'warning':'Published binary flags are used jointly exactly as supplied; independence is NOT assumed. This does not incorporate later searches or 2026 model revisions.'
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csv',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    try: result=summarize(args.csv)
    except (ValueError,OSError) as e: parser.error(str(e))
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(f'Wrote {args.output}. Historical model flags only.')


if __name__=='__main__': main()
