# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: duplicatedlog.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13\x64uplicatedlog.proto\x12\rduplicatedlog\"\x1a\n\x07Request\x12\x0f\n\x07message\x18\x01 \x01(\t\"\x1b\n\x08Response\x12\x0f\n\x07message\x18\x01 \x01(\t2\x98\x01\n\x08Protocol\x12L\n\x17register_secondary_node\x12\x16.duplicatedlog.Request\x1a\x17.duplicatedlog.Response\"\x00\x12>\n\treplicate\x12\x16.duplicatedlog.Request\x1a\x17.duplicatedlog.Response\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'duplicatedlog_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _globals['_REQUEST']._serialized_start=38
  _globals['_REQUEST']._serialized_end=64
  _globals['_RESPONSE']._serialized_start=66
  _globals['_RESPONSE']._serialized_end=93
  _globals['_PROTOCOL']._serialized_start=96
  _globals['_PROTOCOL']._serialized_end=248
# @@protoc_insertion_point(module_scope)