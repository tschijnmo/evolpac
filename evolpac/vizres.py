"""Visualization of evolution results."""

import json
import collections
import argparse
import hashlib


LINE_FORMAT = '{digest:6} {gene:^50} {weight:>6} {score:>7} {eval:>7}'


def vizres(fps):
    """Print the results in JSON files prettily."""

    uniq = {}
    weights = collections.Counter()

    for fp in fps:
        res = json.load(fp)
        uniq.update((i['gene_str'], i) for i in res)
        weights.update(i['gene_str'] for i in res)
        continue

    print(LINE_FORMAT.format(
        digest='Digest', gene='Gene', weight='Weight',
        score='Score', eval='Eval'
    ))
    for i, j in uniq.items():
        print(LINE_FORMAT.format(
            digest=_hash_gene(j['gene']),
            gene=i, weight=weights[i],
            score='{:.3f}'.format(j['score']),
            eval='{:.3f}'.format(j['eval'])
        ))
    print('')

    return


def _hash_gene(gene, length=6):
    """Get the first letters of the SHA-1 digest of the gene."""

    encoded = sum(
        v * 4 ** i for i, v in enumerate(gene)
    ).to_bytes(13, byteorder='big')
    digest = hashlib.sha1(encoded).hexdigest()
    return digest[0:length]


def main():
    """The main driver function."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'input', type=argparse.FileType('r'), nargs='+',
        metavar='FILEs', help='The JSON files from evoluation.'
    )
    args = parser.parse_args()

    return vizres(args.input)


if __name__ == '__main__':
    main()