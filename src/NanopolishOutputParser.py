import numpy as np
import os

import nanopolish_pb2

CONTIG = 0
POSITION = 1
REFERENCE_KMER = 2
READ_INDEX = 3
STRAND = 4
EVENT_INDEX = 5
EVENT_LEVEL_MEAN = 6
EVENT_STDV = 7
EVENT_LENGTH = 8
MODEL_KMER = 9
MODEL_MEAN = 10
MODEL_STDV = 11
STANDARDIZED_LEVEL = 12
START_IDX = 13
END_IDX = 14
SAMPLES = 15


class NanopolishOutputParser():
    """
    Nanopolish txt output parser, produces protobuf serialization if 'serialize' method is called.
    """

    COLUMNS = [
        ('contig', str),
        ('position', int),
        ('reference_kmer', str),
        ('read_index', int),
        ('strand', lambda x: x == "t"),
        ('event_index', int),
        ('event_level_mean', float),
        ('event_stdv', float),
        ('event_length', float),
        ('model_kmer', str),
        ('model_mean', float),
        ('model_stdv', float),
        ('standardized_level', float),
        ('start_idx', int),
        ('end_idx', int),
        ('samples', lambda x: [float(i) for i in x.split(',')])
    ]

    def __init__(self, path):
        """

        Parameters
        ----------
        path: string
            Path to file containing nanopolish output data.

        Returns
        -------

        """
        if not os.path.isfile(path):
            raise FileNotFoundError(
                "The file {} could not be found".format(path))

        self.data = nanopolish_pb2.NanopolishData()
        self.path = path
        self._parse()

    def serialize(self, path):
        """
        Writes protobuf serialization string in file.
        Data is sorted by pairs (read_index, position).

        Parameters
        ----------
        path: string
            Path to file where serialized string of data should be written.

        Returns
        -------

        """
        f = open(path, "wb+")
        f.write(self.data.SerializeToString())
        f.close()
        return

    def _parse(self):
        """
        Parses nanopolish txt output and produces protobuf data in self.data.

        Parameters
        ----------

        Returns
        -------

        """
        header_row, *data_rows = self._lines(self.path)

        if not self._valid(header_row):
            raise Exception("Unexpected file format!")

        raw_data = self._parse_data(data_rows)
        self._fill_data(raw_data)

    def _parse_data(self, rows):
        return [self._parse_data_row_tuple(row) for row in rows]

    def _fill_data(self, raw_data):
        data = self.data

        raw_data = list(filter(lambda x: not any(
            ch == 'N' for ch in x[9]), raw_data))

        def extract_id(rd):
            return (rd[READ_INDEX], rd[POSITION])

        # TODO
        # already sorted? probably, check that
        raw_data.sort(key=extract_id)

        if len(raw_data) == 0:
            return

        new_event_align = self.data.event_aligns.add()
        self._fill_event_align(new_event_align, raw_data[0])

        for i in range(1, len(raw_data)):
            if extract_id(raw_data[i - 1]) != extract_id(raw_data[i]):
                new_event_align = self.data.event_aligns.add()
                self._fill_event_align(new_event_align, raw_data[i])
            else:
                self._add_repeated(new_event_align, raw_data[i])

    def _add_repeated(self, new_event_align, raw_data):
        new_event = new_event_align.events.add()
        new_event.index = raw_data[EVENT_INDEX]
        new_event.level_mean = raw_data[EVENT_LEVEL_MEAN]
        new_event.stdv = raw_data[EVENT_STDV]
        new_event.length = raw_data[EVENT_LENGTH]
        new_event.standardized_level = raw_data[STANDARDIZED_LEVEL]
        new_event.start_idx = raw_data[START_IDX]
        new_event.end_idx = raw_data[END_IDX]
        for sample in raw_data[SAMPLES]:
            new_event.samples.append(sample)

    def _fill_event_align(self, event_align, raw_data):
        event_align.contig = raw_data[CONTIG]
        event_align.position = raw_data[POSITION]
        event_align.reference_kmer = raw_data[REFERENCE_KMER]
        event_align.read_index = raw_data[READ_INDEX]
        event_align.strand = raw_data[STRAND]
        event_align.model_kmer = raw_data[MODEL_KMER]
        event_align.model_mean = raw_data[MODEL_MEAN]
        event_align.model_stdv = raw_data[MODEL_STDV]
        self._add_repeated(event_align, raw_data)

    def _valid(self, header_row):
        expected_cols = (c[0] for c in NanopolishOutputParser.COLUMNS)
        actual_cols = header_row.split()
        return all(exp == act for exp, act in zip(expected_cols, actual_cols))

    def _lines(self, file):
        with open(file) as file:
            return (line.strip() for line in file.readlines())

    def _parse_data_row_dict(self, row):
        fields = row.split()
        return {name: parse(val) for (name, parse), val in zip(NanopolishOutputParser.COLUMNS, fields)}

    def _parse_data_row_tuple(self, row):
        fields = row.split()
        return tuple(parse(val) for (name, parse), val in zip(NanopolishOutputParser.COLUMNS, fields))
