# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: nanopolish.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='nanopolish.proto',
  package='nanopolish',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x10nanopolish.proto\x12\nnanopolish\"\xf0\x02\n\nEventAlign\x12\x0e\n\x06\x63ontig\x18\x01 \x01(\t\x12\x10\n\x08position\x18\x02 \x01(\x04\x12\x16\n\x0ereference_kmer\x18\x03 \x01(\t\x12\x12\n\nread_index\x18\x04 \x01(\r\x12\x0e\n\x06strand\x18\x05 \x01(\x08\x12\x12\n\nmodel_kmer\x18\x06 \x01(\t\x12\x12\n\nmodel_mean\x18\x07 \x01(\x01\x12\x12\n\nmodel_stdv\x18\x08 \x01(\x01\x12,\n\x06\x65vents\x18\n \x03(\x0b\x32\x1c.nanopolish.EventAlign.Event\x1a\x99\x01\n\x05\x45vent\x12\r\n\x05index\x18\x01 \x01(\r\x12\x12\n\nlevel_mean\x18\x02 \x01(\x01\x12\x0c\n\x04stdv\x18\x03 \x01(\x01\x12\x0e\n\x06length\x18\x04 \x01(\x01\x12\x1a\n\x12standardized_level\x18\x05 \x01(\x01\x12\x11\n\tstart_idx\x18\x06 \x01(\r\x12\x0f\n\x07\x65nd_idx\x18\x07 \x01(\r\x12\x0f\n\x07samples\x18\x08 \x03(\x01\">\n\x0eNanopolishData\x12,\n\x0c\x65vent_aligns\x18\x01 \x03(\x0b\x32\x16.nanopolish.EventAlignb\x06proto3')
)




_EVENTALIGN_EVENT = _descriptor.Descriptor(
  name='Event',
  full_name='nanopolish.EventAlign.Event',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='index', full_name='nanopolish.EventAlign.Event.index', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='level_mean', full_name='nanopolish.EventAlign.Event.level_mean', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='stdv', full_name='nanopolish.EventAlign.Event.stdv', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='length', full_name='nanopolish.EventAlign.Event.length', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='standardized_level', full_name='nanopolish.EventAlign.Event.standardized_level', index=4,
      number=5, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='start_idx', full_name='nanopolish.EventAlign.Event.start_idx', index=5,
      number=6, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='end_idx', full_name='nanopolish.EventAlign.Event.end_idx', index=6,
      number=7, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='samples', full_name='nanopolish.EventAlign.Event.samples', index=7,
      number=8, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=248,
  serialized_end=401,
)

_EVENTALIGN = _descriptor.Descriptor(
  name='EventAlign',
  full_name='nanopolish.EventAlign',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='contig', full_name='nanopolish.EventAlign.contig', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='position', full_name='nanopolish.EventAlign.position', index=1,
      number=2, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='reference_kmer', full_name='nanopolish.EventAlign.reference_kmer', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='read_index', full_name='nanopolish.EventAlign.read_index', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='strand', full_name='nanopolish.EventAlign.strand', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='model_kmer', full_name='nanopolish.EventAlign.model_kmer', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='model_mean', full_name='nanopolish.EventAlign.model_mean', index=6,
      number=7, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='model_stdv', full_name='nanopolish.EventAlign.model_stdv', index=7,
      number=8, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='events', full_name='nanopolish.EventAlign.events', index=8,
      number=10, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_EVENTALIGN_EVENT, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=33,
  serialized_end=401,
)


_NANOPOLISHDATA = _descriptor.Descriptor(
  name='NanopolishData',
  full_name='nanopolish.NanopolishData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='event_aligns', full_name='nanopolish.NanopolishData.event_aligns', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=403,
  serialized_end=465,
)

_EVENTALIGN_EVENT.containing_type = _EVENTALIGN
_EVENTALIGN.fields_by_name['events'].message_type = _EVENTALIGN_EVENT
_NANOPOLISHDATA.fields_by_name['event_aligns'].message_type = _EVENTALIGN
DESCRIPTOR.message_types_by_name['EventAlign'] = _EVENTALIGN
DESCRIPTOR.message_types_by_name['NanopolishData'] = _NANOPOLISHDATA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

EventAlign = _reflection.GeneratedProtocolMessageType('EventAlign', (_message.Message,), dict(

  Event = _reflection.GeneratedProtocolMessageType('Event', (_message.Message,), dict(
    DESCRIPTOR = _EVENTALIGN_EVENT,
    __module__ = 'nanopolish_pb2'
    # @@protoc_insertion_point(class_scope:nanopolish.EventAlign.Event)
    ))
  ,
  DESCRIPTOR = _EVENTALIGN,
  __module__ = 'nanopolish_pb2'
  # @@protoc_insertion_point(class_scope:nanopolish.EventAlign)
  ))
_sym_db.RegisterMessage(EventAlign)
_sym_db.RegisterMessage(EventAlign.Event)

NanopolishData = _reflection.GeneratedProtocolMessageType('NanopolishData', (_message.Message,), dict(
  DESCRIPTOR = _NANOPOLISHDATA,
  __module__ = 'nanopolish_pb2'
  # @@protoc_insertion_point(class_scope:nanopolish.NanopolishData)
  ))
_sym_db.RegisterMessage(NanopolishData)


# @@protoc_insertion_point(module_scope)
