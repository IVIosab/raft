# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: raft.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nraft.proto\")\n\rTermIdMessage\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\n\n\x02id\x18\x02 \x01(\x05\"1\n\x11TermResultMessage\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x0e\n\x06result\x18\x02 \x01(\x08\"\x1f\n\rPeriodMessage\x12\x0e\n\x06period\x18\x01 \x01(\x05\"\x0f\n\rEmptyMessasge\"0\n\rLeaderMessage\x12\x0e\n\x06leader\x18\x01 \x01(\x05\x12\x0f\n\x07\x61\x64\x64ress\x18\x02 \x01(\t2\xc9\x01\n\x07Service\x12\x31\n\x0bRequestVote\x12\x0e.TermIdMessage\x1a\x12.TermResultMessage\x12\x33\n\rAppendEntries\x12\x0e.TermIdMessage\x1a\x12.TermResultMessage\x12)\n\x07Suspend\x12\x0e.PeriodMessage\x1a\x0e.EmptyMessasge\x12+\n\tGetLeader\x12\x0e.EmptyMessasge\x1a\x0e.LeaderMessageb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'raft_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _TERMIDMESSAGE._serialized_start=14
  _TERMIDMESSAGE._serialized_end=55
  _TERMRESULTMESSAGE._serialized_start=57
  _TERMRESULTMESSAGE._serialized_end=106
  _PERIODMESSAGE._serialized_start=108
  _PERIODMESSAGE._serialized_end=139
  _EMPTYMESSASGE._serialized_start=141
  _EMPTYMESSASGE._serialized_end=156
  _LEADERMESSAGE._serialized_start=158
  _LEADERMESSAGE._serialized_end=206
  _SERVICE._serialized_start=209
  _SERVICE._serialized_end=410
# @@protoc_insertion_point(module_scope)
