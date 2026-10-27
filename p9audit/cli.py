"""Reproducible offline CLI; it never downloads or submits data."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
from .core import Audit, Particle, Search


def rows(path, expected):
    with path.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != expected:
            raise ValueError(f"{path.name}: expected columns {expected}")
        return list(reader)


def run(directory, selected):
    paths = {name: directory / name for name in ('particles.csv', 'searches.csv', 'detections.csv', 'metadata.json')}
    metadata = json.loads(paths['metadata.json'].read_text())
    for field in ('label', 'synthetic', 'coordinate_epoch', 'probability_definition', 'independent_groups_assumption', 'model_sources'):
        if field not in metadata:
            raise ValueError(f"Missing metadata: {field}")
    if not isinstance(metadata['synthetic'], bool):
        raise ValueError('synthetic must be a JSON boolean')
    if not isinstance(metadata['independent_groups_assumption'], str) or not metadata['independent_groups_assumption'].strip():
        raise ValueError('Document conditional independence assumption explicitly')
    p = [Particle(r['model'], r['particle'], r['weight']) for r in rows(paths['particles.csv'], ['model', 'particle', 'weight'])]
    s = [Search(r['search'], r['dependence_group'], r['source']) for r in rows(paths['searches.csv'], ['search', 'dependence_group', 'source'])]
    d = [(r['model'], r['particle'], r['search'], r['p_detect']) for r in rows(paths['detections.csv'], ['model', 'particle', 'search', 'p_detect'])]
    audit = Audit(p, s, d)
    if not isinstance(metadata['model_sources'], dict) or any(not metadata['model_sources'].get(m) for m in audit.models):
        raise ValueError('Every model needs provenance in metadata.model_sources')
    coverage = audit.coverage(selected)
    return {
        'schema_version': 1,
        'warning': 'SYNTHETIC DEMO. Not actual sky constraints.' if metadata['synthetic'] else 'User-supplied model. Conditional coverage, not existence probability or a measured planet location.',
        'metadata': metadata,
        'inputs_sha256': {n: hashlib.sha256(p.read_bytes()).hexdigest() for n,p in paths.items()},
        'selected_searches': selected,
        'coverage_by_model': coverage,
        'null_likelihood_by_model': {m: {'lower': 1-v['upper'], 'upper': 1-v['lower']} for m,v in coverage.items()},
        'followup_rank': audit.rank(selected),
        'assumptions': [
            'Groups conditionally independent given each particle; within-group dependence unknown.',
            'Null likelihood assumes no accepted detection and a correct input detection model.',
            'Candidate ranking is worst-model lower incremental coverage, not discovery probability.',
            'No inference about whether Planet Nine exists; no automatic new literature ingestion.'
        ]
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--selected', nargs='*', default=[])
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        report = run(args.directory, args.selected)
    except (ValueError, OSError, KeyError, TypeError) as e:
        parser.error(str(e))
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False) + '\n')
    print(f"Wrote {args.output}. {report['warning']}")


if __name__ == '__main__':
    main()
