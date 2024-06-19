# -*- coding: utf-8 -*-

import os

from django.core.exceptions import SuspiciousOperation
from django.core.files.storage import FileSystemStorage
from django.utils._os import safe_join
from django.utils.encoding import smart_str

from . import storage_utils


class CAStorage(FileSystemStorage):
    def __init__(self, location=None, base_url=None, keep_extension=True, sharding=(2, 2)):
        if base_url is not None and not base_url.endswith("/"):
            base_url += "/"

        super(CAStorage, self).__init__(location=location, base_url=base_url)

        self.shard_width, self.shard_depth = sharding
        self.keep_extension = keep_extension

    def get_available_name(self, name, n=None):
        return name

    def digest(self, content):
        if hasattr(content, "temporary_file_path"):
            return storage_utils.hash_filename(content.temporary_file_path())
        digest = storage_utils.hash_chunks(content.chunks())
        content.seek(0)
        return digest

    def shard(self, hexdigest):
        return list(storage_utils.shard(hexdigest, self.shard_width, self.shard_depth, rest_only=False))

    def path(self, hexdigest):
        shards = self.shard(hexdigest)

        try:
            path = safe_join(self.location, *shards)
        except ValueError:
            raise SuspiciousOperation("Attempted access to '%s' denied." % ("/".join(shards),))

        return smart_str(os.path.normpath(path))

    def url(self, name):
        return super(CAStorage, self).url("/".join(self.shard(name)))

    def delete(self, name, sure=False):
        if not sure:
            return

        path = name
        if os.path.sep not in path:
            path = self.path(name)
        storage_utils.rm_file_and_empty_parents(path, root=self.location)

    def _save(self, name, content):
        digest = self.digest(content)
        if self.keep_extension:
            digest += os.path.splitext(name)[1]
        path = self.path(digest)
        if os.path.exists(path):
            return digest
        return super(CAStorage, self)._save(digest, content)
