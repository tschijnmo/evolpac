`Evolpac`: Evolution of the PacMan genes
========================================

This project contains code to optimize the PacMan genes by an evolution
algorithm.  Note that this code is a Python library rather than a stand-alone
program.  So it can be used in a very flexible way inside any Python script.


Building and Installation
-------------------------

Since this code contains native C modules for efficiency reasons in making a
large number of duels, the code needs building to work.  To build the native C
modules, on the top-level directory of this project, the following command can
be run

```
python3 setup.py build
```

Since there are OpenMP parallelization over the duels in a tournament, the
compiler is required to support the `-fopenmp` compiler flag.  Then by running
`python3 setup.py install`, the code can be installed.  Then a simple Python
code like,

```Py
import evolpac
```

should work.


Organization of the project
---------------------------

All the code are in the `evolpac` package.  Inside it, the subpackage `duel`
contains the core functions for running duels among genes.  The dueling
mechanism is treated as black box outside this package.  Basically it contains
two native modules, `duel.c` contains code to run a duel between two given
genes, and `tournament.c` runs duels among all genes in a pool in parallel and
gets the average score for each gene.  The functions in the native modules are
all forwarded in the `duel` subpackage.  So just importing the subpackage is
sufficient for using the facilities.

In the top-level `evolpac` package, the module `gene_manip` contains some
utility functions for the manipulation of the genes.  `evolve` is the core
module contains the core function for running the evolution.  Note that this
contains a very general function supporting all kinds of tweak of the parameters
in the evolution algorithm.  And we can also output the intermediate results
into JSON files.  The `drivers` module was intended for large high-level driver
functions.  It actually just contains a driver to generate a given number of
genes from repeated short contest among randomly generated genes.  The module
`vizres` is a separate module for the visualization of results.  For instance,
it can be used to visualize the content in `result.json` by

```
python3 -m evolpac.vizres result.json
```

then we can get a sneak peek into the result like

```
Digest                        Gene                        Weight   Score    Eval
327c47 03000000110100003330321121231211221231131131100133      1  17.165  13.278
50f1f7 03000000311100003300321121221211221231132130300131     14  18.780  12.556
d2b2b4 03000300111100003300321121221211221231131131330110      2  11.209  15.111
816a36 03000000110100003330321121211211221231131131123311      1  16.810  11.444
1cf4fd 03000000110100003330321121211211221231131130130131     10  10.891  15.611
89bd06 03000300111100003300321121221211221231131131103131      1  17.596  14.056
193c87 03000000110100003330321121211211221231321133130330      8  16.551  10.778
a49d8f 03000000111100003330321121221211221231131130301131      1  16.140  14.000
d7a5bf 03000000110100003300321121221211221231131133303130      1  15.705  13.167
9f6d8f 03000000100100000333321121231211221231131130130131     20  15.978  17.278
eec437 03000000110100003300321121221211221231101133130130      2  14.275  16.000
c0024f 03000000311100003300321121221211221231131130300131      6  10.825  15.444
```

where the digest are the SHA-1 hash of the gene sequence, which can be used for
easier naming and tracking of the genes.


Example usage
-------------

Due to the low quality of really randomly generated genes, we would first like a
pool of genes with relatively good quality.  Then later random generation of
genes could just pull a random gene from this pool.  This can be achieved by the
following Python code.

```Py
from evolpac.drivers import form_pool

with open('pool.txt', 'w') as out_fp:
    form_pool(3000, out_fp, pop_size=600, evol_steps=100)
```

which will attempt to generate a pool of 3000 genes, each of which are the
winners among a random population 600 genes evolved by 100 steps.  Next, we can
run a real long evolution by the following code,

```Py
from evolpac.duel import run_tournament, eval_w_sample
from evolpac.evolve import evolve
from evolpac.genemanip import gen_random_gene, get_gene_from_str, read_gene_strs


def main():
    """The main driver."""

    with open('../pool.txt', 'r') as fp:
        pool = read_gene_strs(fp)

    good_ones = [
	    get_gene_from_str('03100003010300103333321121121213221121131133132300'),
	    get_gene_from_str('03000001111122201313211212111212212211211311101301'),
	    get_gene_from_str('03000001111122201303211212111212212211211310001331'),
	    get_gene_from_str('00000020111122200300111111211211221221330330310333'),
	    get_gene_from_str('03000000032123203301211232212211212211133131103033'),
	    get_gene_from_str('01310000110020203333131323323322222322323310323310'),
	    get_gene_from_str('01310000110020203330131323323322222322323313023310'),
	    get_gene_from_str('03000001111122201313211212111212212211211311311300'),
	    get_gene_from_str('03000001111122201303211212111212212211211311311300'),
	    get_gene_from_str('03000000111022203333211112212211212211311231021301'),
	    get_gene_from_str('03000000111022203333211112212231212211032123322331'),
	    get_gene_from_str('03000000110100003330321121221211221231131133101131'),
	    get_gene_from_str('03000300011100003330321121221211221231131130221110'),
	    get_gene_from_str('03000000011100003330321121221211221231131133301131'),
	    get_gene_from_str('03000000000100003330321121221211221231131133330131'),
	    get_gene_from_str('03000300000100003330321121221211221231131133301131'),
	    get_gene_from_str('03000300010100003330321121221211221231131133130131'),
	    get_gene_from_str('03000000011100003330321121221111221231131133131131'),
    ]
    eval_sample = good_ones

    evolve(600, 10000, run_tournament, init=good_ones, eval_cb=eval_w_sample(eval_sample),
           gene_db=pool, out_steps=100)


if __name__ == '__main__':
    main()
```

In this script, we start with a few good genes that we have found in previous
evolutions, the rest of the population are all drawn from the pool that we just
generated.  Then this population is evolved by the evolution algorithm.
