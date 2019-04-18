# This depends on hadoop-test-cluster by Jim Crist
# Start a cluster with
# $ hcluster startup --image=cdh6 --config=simple
# Requires libhdfs3 installed with conda
# This creates a hadoop cluster without kerberos autentication that can
# be accessed from the host node (the whole thing runs in containers)

import pyarrow as pa

class HdfsConnection:
    """Small class with utilities to hdfs"""
    def __init__(self,
                 host='127.0.0.1',
                 port=9000,
                 user='testuser',
                 driver='libhdfs3'):
        self.fs = pa.hdfs.connect(host, port, user, driver=driver)

    def open(self, path, mode='rb'):
        return self.fs.open(path, mode)
