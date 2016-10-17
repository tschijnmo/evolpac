"""Visualization of evolution results."""

import json
import collections
import argparse


LINE_FORMAT = '{gene:^50} {weight:>6} {score:>7} {eval:>7}'


def vizres(fp):
    """Print the results in JSON file prettily."""

    res = json.load(fp)

    uniq = {i['gene_str']: i for i in res}
    weights = collections.Counter(i['gene_str'] for i in res)

    print(LINE_FORMAT.format(
        gene='Gene', weight='Weight', score='Score', eval='Eval'
    ))
    for i, j in uniq.items():
        print(LINE_FORMAT.format(
            gene=i, weight=weights[i], score=j['score'], eval=j['eval']
        ))
    print('')

    return


def main():
    """The main driver function."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'input', type=argparse.FileType('r'),
        metavar='FILE', help='The JSON file from evoluation.'
    )
    args = parser.parse_args()

    return vizres(args.input)


if __name__ == '__main__':
    main()