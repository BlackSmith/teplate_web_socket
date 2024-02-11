from datetime import datetime

from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, \
    DateTime, JSON

metadata_obj = MetaData()

content_type_table = Table(
    'content_types',
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(32))
)

link_table = Table(
    'source_links',
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("url", String, nullable=False),
    Column("file_id", ForeignKey("files.id", ondelete='CASCADE'), nullable=False)
)

collection_table = Table(
    'collections',
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(32)),
    Column("slug", String(32), index=True, unique=True),
)

file_table = Table(
    'files',
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("path", String(128), index=True, unique=True),
    Column("md5", String(32), index=True, unique=True),
    Column("content_type_id", ForeignKey("content_types.id"), nullable=False),
    Column("size", Integer, nullable=False),
    Column("created_at", DateTime, nullable=False, default=datetime.now),
    Column("width", Integer),
    Column("height", Integer),
    Column("collection_id", ForeignKey("collection.id", ondelete='CASCADE'), nullable=False),
    Column("parameters", JSON, nullable=False, default={}),
)
