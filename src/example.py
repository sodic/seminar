import NanopolishOutputParser as nop
import NanopolishOutputData as nod
import sys

if __name__ == '__main__':
    # parse nanopolish txt file and serialize it
    parser = nop.NanopolishOutputParser(sys.argv[1])
    parser.serialize(sys.argv[2])


    # read data from protobuf serialization
    data = nod.NanopolishOutputData(sys.argv[2])

    # iterate through lines
    for ea, event in data:
        if ea.position == 3:
            print(event)

    print()
    print()
    # iterate through event_aligns
    # Should give same output as previous for loop.
    # Every event_align is unique by (position, read_index)
    for ea in data.event_aligns:
        if ea.position == 3:
            for event in ea.events:
                print(event)

    # data retrieval


    # retrieve specific line
    # log time
    # Prints pair, first element is event align,
    # second is specific event on that line.
    print(data.get_line(3))

    # retrieve specific event_align
    # constant time
    print(data.event_aligns[1])


    print(data.event_aligns[1].events[0].samples)


    try:
        print(data.get_reference_kmer(7, 0))
        kmer, mean, stdv = data.get_model(7, 0)
    except KeyError:
        print("There is no event align with read_index = 0 && position = 7")

    # print all events on event_align with read_index = 0 && position = 9
    # raises KeyError if there is no such
    print(data.get_events(9))
