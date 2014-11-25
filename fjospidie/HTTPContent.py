import logging
import hashlib

class HTTPContent(object):
    def __init__(self, content, database):
        self.size = len(content.text)
        self.md5 = hashlib.md5(content.text.encode('utf-8')).hexdigest()
        self.mime_type = content.mime_type
        
        if not database.fs.exists({"md5":self.md5}):
            content_id = database.fs.put(content.text.encode("UTF-8"))
        else:
            grid_file = database.fs.get_version(md5=self.md5)
            content_id = grid_file._id

        self.content_id = content_id
