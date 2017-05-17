#!/usr/bin/env python


import sys
import os

import numpy as np
import pandas as pd
import click

@click.command()
@click.option('--inputfile', type=click.Path())
@click.option('--outputfile', type=click.Path())
def main(inputfile, outputfile):
    ## Leemos el archivo
    df = pd.read_csv(inputfile, sep='|')

    ## Hacemos "data science"
    df = df.assign(cuadrados = lambda x: np.square(x.numeros))

    ## Guardamos el resultado en JSON
    df.to_json(outputfile, orient='records', lines=True)

if __name__ == '__main__':
    main()
