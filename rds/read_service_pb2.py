# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: read-service.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12read-service.proto\x12\x0breadservice\"B\n\x0bReadRequest\x12\x12\n\ncollection\x18\x01 \x01(\t\x12\x10\n\x08\x64ocument\x18\x02 \x01(\t\x12\r\n\x05\x66ield\x18\x03 \x01(\t\"\xaf\x01\n\x0cReadResponse\x12?\n\x0b\x63ollections\x18\x01 \x03(\x0b\x32*.readservice.ReadResponse.CollectionsEntry\x12\r\n\x05\x65rror\x18\x02 \x01(\t\x1aO\n\x10\x43ollectionsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12*\n\x05value\x18\x02 \x01(\x0b\x32\x1b.readservice.CollectionData:\x02\x38\x01\"\x9c\x01\n\x0e\x43ollectionData\x12=\n\tdocuments\x18\x01 \x03(\x0b\x32*.readservice.CollectionData.DocumentsEntry\x1aK\n\x0e\x44ocumentsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12(\n\x05value\x18\x02 \x01(\x0b\x32\x19.readservice.DocumentData:\x02\x38\x01\"t\n\x0c\x44ocumentData\x12\x35\n\x06\x66ields\x18\x01 \x03(\x0b\x32%.readservice.DocumentData.FieldsEntry\x1a-\n\x0b\x46ieldsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x32P\n\x0bReadService\x12\x41\n\x08ReadData\x12\x18.readservice.ReadRequest\x1a\x19.readservice.ReadResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'read_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_READRESPONSE_COLLECTIONSENTRY']._loaded_options = None
  _globals['_READRESPONSE_COLLECTIONSENTRY']._serialized_options = b'8\001'
  _globals['_COLLECTIONDATA_DOCUMENTSENTRY']._loaded_options = None
  _globals['_COLLECTIONDATA_DOCUMENTSENTRY']._serialized_options = b'8\001'
  _globals['_DOCUMENTDATA_FIELDSENTRY']._loaded_options = None
  _globals['_DOCUMENTDATA_FIELDSENTRY']._serialized_options = b'8\001'
  _globals['_READREQUEST']._serialized_start=35
  _globals['_READREQUEST']._serialized_end=101
  _globals['_READRESPONSE']._serialized_start=104
  _globals['_READRESPONSE']._serialized_end=279
  _globals['_READRESPONSE_COLLECTIONSENTRY']._serialized_start=200
  _globals['_READRESPONSE_COLLECTIONSENTRY']._serialized_end=279
  _globals['_COLLECTIONDATA']._serialized_start=282
  _globals['_COLLECTIONDATA']._serialized_end=438
  _globals['_COLLECTIONDATA_DOCUMENTSENTRY']._serialized_start=363
  _globals['_COLLECTIONDATA_DOCUMENTSENTRY']._serialized_end=438
  _globals['_DOCUMENTDATA']._serialized_start=440
  _globals['_DOCUMENTDATA']._serialized_end=556
  _globals['_DOCUMENTDATA_FIELDSENTRY']._serialized_start=511
  _globals['_DOCUMENTDATA_FIELDSENTRY']._serialized_end=556
  _globals['_READSERVICE']._serialized_start=558
  _globals['_READSERVICE']._serialized_end=638
# @@protoc_insertion_point(module_scope)
