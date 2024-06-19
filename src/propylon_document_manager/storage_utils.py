# -*- coding: utf-8 -*-

import hashlib
import os

from django.core.files import File
from django.core.files.uploadedfile import UploadedFile


def hash_filename(filename, digestmod=hashlib.sha1,
                  chunk_size=UploadedFile.DEFAULT_CHUNK_SIZE):

    fileobj = File(open(filename))
    try:
        return hash_chunks(fileobj.chunks(chunk_size=chunk_size))
    finally:
        fileobj.close()


def hash_chunks(iterator, digestmod=hashlib.sha1):
    digest = digestmod()
    for chunk in iterator:
        digest.update(chunk)
    return digest.hexdigest()


def shard(string, width, depth, rest_only=False):
    for i in range(depth):
        yield string[(width * i):(width * (i + 1))]

    if rest_only:
        yield string[(width * depth):]
    else:
        yield string


def rm_file_and_empty_parents(filename, root=None):
    if root:
        root_stat = os.stat(root)

    os.unlink(filename)
    directory = os.path.dirname(filename)
    while not (root and os.path.samestat(root_stat, os.stat(directory))):
        if os.listdir(directory):
            break
        os.rmdir(directory)
        directory = os.path.dirname(directory)
