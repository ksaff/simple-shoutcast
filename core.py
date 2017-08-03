"""
Core module
"""
import logging
import re
import struct
import sys
import urllib2


ICY_NAME_RE = re.compile(r'icy-name:(.*)', flags=re.IGNORECASE)
ICY_META_INT_RE = re.compile(r'icy-metaint:(.*)', flags=re.IGNORECASE)
CONTENT_TYPE_RE = re.compile(r'content-type:(.*)', flags=re.IGNORECASE)
META_RE = re.compile(r'StreamTitle\\?=\'(.*?)\';', flags=re.IGNORECASE)
# TODO figure out what the backslash was...


class ReaderWrapper(object):
    """
    Wrap an object with a read method, providing a sanitized read method devoid
    of metadata. Has a logger attribute containing metadata (if metadata is 
    specified). Also provide passthru to reader object via __getattr__.
    """

    def __init__(self, reader, meta_int=None):
        """
        Take in reader, expect metadata if meta_int is specified.

        :param reader: object with read method containing Shoutcast stream
        :param meta_int: icy_metaint; the meta interval
        """
        self.reader = reader
        self.meta_int = meta_int
        self.logger = logging.getLogger(__name__)

    
def read_headers_in_stream(stream, chunk_len=1024):
    """
    Read from stream, looking for icy and content-type headers. Seek stream to
    beginning of audio if metaint found.

    :param stream: open Shoutcast object with read method
    :return: icy-name, icy-metaint, content-type
    """
    chunk = stream.read(chunk_len)

    name_mat = ICY_NAME_RE.search(chunk)
    name = name_mat.group(1).strip() if name_mat else None
    meta_int_mat = ICY_META_INT_RE.search(chunk)
    meta_int = int(meta_int_mat.group(1).strip()) if meta_int_mat else None
    cont_type_mat = CONTENT_TYPE_RE.search(chunk)
    content_type = cont_type_mat.group(1).strip() if cont_type_mat else None

    if meta_int:
        pass
    
    return name, meta_int, content_type
    
    

class ShoutcastCrawler(object):

    # TODO investigate whether auto-finding metadata without metaint is feasible
    
    def __init__(self, in_stream, out_stream, meta_out_stream=None,
                 meta_int=None):
        """
        Read from in_stream, write to out_stream. Write metadata to 
        meta_out_stream if specified, otherwise assume no metadata. If meta_int
        is not given, assume problem for now, maybe auto-find metadata later.

        :param in_stream: open Shoutcast object with read method
        :param out_stream: open object with write method
        :param meta_out_stream: open object with write method
        :param meta_int: icy-metaint
        """
        self.in_stream = in_stream
        self.out_stream = out_stream
        self.meta_out_stream = meta_out_stream
        self.meta_int = meta_int
        if self.meta_out_stream and not self.meta_int:
            raise Exception("Need metaint if writing metadata!")  # TODO make specific
    
    def run(self):
        """
        Just run indefinitely for now
        """
        pass
