from argparse import ArgumentParser


def strand_parse(strand_mark):
    return strand_mark == "t"


def parse_data_row_dict(row):
    fields = row.split()
    return {name: parse(val) for (name, parse), val in zip(COLUMNS, fields)}


def parse_data_row_tuple(row):
    fields = row.split()
    return tuple(parse(val) for (name, parse), val in zip(COLUMNS, fields))


def parse_data(rows, method='dict'):
    parse = representation_methods[method]
    return [parse(row) for row in rows]


COLUMNS = [
    ('contig', str),
    ('position', int),
    ('reference_kmer', str),
    ('read_index', int),
    ('strand', strand_parse),
    ('event_index', int),
    ('event_level_mean', float),
    ('event_stdv', float),
    ('event_length', float),
    ('model_kmer', str),
    ('model_mean', float),
    ('model_stdv', float),
    ('standardized_level', float),
]


representation_methods = {
    'dict': parse_data_row_dict,
    'tuple': parse_data_row_tuple,
}


def valid(header_row):
    expected_cols = (c[0] for c in COLUMNS)
    actual_cols = header_row.split()
    return all(exp == act for exp, act in zip(expected_cols, actual_cols))


def get_args():
    parser = ArgumentParser(description="""Convert a symbolic alignment file       
        into a SAM alignemnt file and a corresponding reference.""")

    parser.add_argument(
        "event_alignments_file",
        help="The event alignments file given by the 'nanopolish eventalign' command."
    )

    parser.add_argument(
        "-r",
        "--representation-method",
        default="dict",
        dest="representation_method",
        help=f"How do you want to store the data? {'|'.join(representation_methods.keys())}"
    )

    return parser.parse_args()


def lines(file):
    with open(file) as file:
        return (line.strip() for line in file.readlines())


def main(event_alignments_file, representation_method):
    header_row, *data_rows = lines(event_alignments_file)

    if not valid(header_row):
        print("Unexpected file format")
        return

    data = parse_data(data_rows, representation_method)
    print(data)


if __name__ == '__main__':
    args = get_args()
    main(args.event_alignments_file, args.representation_method)
