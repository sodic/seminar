import nanopolish_pb2
import os
from bisect import bisect_right


class NanopolishOutputData():
    """
    Interface to nanopolish output data. Takes path to protobuf serialized
    nanopolish output data and offers methods for data retrieval.
    """

    def __init__(self, path):
        """

        Parameters
        ----------
        path: string
                Path to protobuf serialization of Nanopolish output.

        Returns
        -------

        """
        if not os.path.isfile(path):
            raise FileNotFoundError(
                "The file {} could not be found".format(path))

        self.data = nanopolish_pb2.NanopolishData()
        self.data.ParseFromString(open(path, 'rb').read())
        self.event_aligns = self.data.event_aligns

        self.position_index = {}
        self.line_search = [0]

        for ea in self.data.event_aligns:
            self.line_search.append(len(ea.events) + self.line_search[-1])
            self.position_index[(ea.position, ea.read_index)] = ea

        self.line_cnt = self.line_search[-1]
        self.iteration_stack = []

    def __iter__(self):
        self.iteration_stack.append((0, 0))
        return self

    def __next__(self):
        """
        For iterating through lines in linear time. Use standard for loop. 

        Parameters
        ----------

        Returns
        -------
        (event_align, event)
            Pair consisting of event_align object (which generally has more events) and specific event on current line.
            Returned event can be also found as element of event_align.events.

        """
        eas = self.data.event_aligns
        ea_ind, event_ind = self.iteration_stack.pop()
        if ea_ind >= len(eas):
            raise StopIteration

        nea, nevent = ea_ind, event_ind + 1
        if nevent >= len(eas[nea].events):
            nea += 1
            nevent = 0
        self.iteration_stack.append((nea, nevent))

        return (eas[ea_ind], eas[ea_ind].events[event_ind])

    def get_line_cnt(self):
        """
        Returns number of lines in original nanopolish txt output.

        Parameters
        ----------

        Returns
        -------

        """
        return self.line_cnt

    def get_line(self, line_number):
        """
        Method works in O(logn) where n is number of event_aligns. If you want to iterate through lines
        in linear time don't use this method. 

        Parameters
        ----------
        line_number: int

        Returns
        -------
        (event_align, event)
            Pair consisting of event_align object (which generally has more events) and specific event on given line.
            Returned event can be also found as element of event_align.events.

        """
        if line_number < 0 or line_number >= self.line_cnt:
            raise ValueError("Line number out of range!")
        ind = bisect_right(self.line_search, line_number)
        ea = self.data.event_aligns[ind - 1]
        event = ea.events[line_number - self.line_search[ind]]
        return (ea, event)

    def get_event_align(self, position, read_index=0):
        """
        Raises key error if (position, read_index) does not exist in data.  
        Read_index default is zero for convenience. E.g. if someone is working with
        only one reference contig read.

        Parameters
        ----------
        position: int
                Position in reference read. 
        read_index: int
                Index of contig, because reference can have more reads.

        Returns
        -------
        event_align object

        """
        return self.position_index[(position, read_index)]

    def get_reference_kmer(self, position, read_index=0):
        return self.get_event_align(position, read_index).reference_kmer

    def get_events(self, position, read_index=0):
        return self.get_event_align(position, read_index).events

    def get_model(self, position, read_index=0):
        """

        Parameters
        ----------
        position: int
            Position in reference read.
        read_index: int
            Index of contig, because reference can have more reads. 

        Returns
        -------
        (model_kmer, model_mean, model_stdv)

        """
        ea = self.get_event_align(position, read_index)
        return (ea.model_kmer, ea.model_mean, ea.model_stdv)
