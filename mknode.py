from triples import SimpleGraph
from utils import _version

fs_model = SimpleGraph()

fs_model.add(('root', 'version', _version()))
fs_model.add(('root', 'is', 'bucket'))
fs_model.add(('root', 'contain', 'test'))
fs_model.add(('test', 'is', 'object'))
fs_model.add(('root', 'contain', 'test_bucket'))
fs_model.add(('test_bucket', 'is', 'bucket'))

fs_model.save('model/test.csv')
