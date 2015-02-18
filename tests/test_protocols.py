import pickle

import pytest
import mock
import bluefloodserver.protocols


def test_lineReceiver():
    handler = bluefloodserver.protocols.MetricLineReceiver()
    handler.processMetric = mock.MagicMock()
    handler.lineReceived('foo.bar.baz 22.2 124357823')
    handler.processMetric.assert_called_once_with('foo.bar.baz', (124357823.0, 22.2))

def test_pickleReceiver():
    handler = bluefloodserver.protocols.MetricPickleReceiver()
    handler.processMetric = mock.MagicMock()
    timestamp = 12345678.0
    metrics = [('foo.bar.baz', (timestamp, i)) for i in range(5)]
    handler.connectionMade()
    handler.stringReceived(pickle.dumps(metrics))

    assert handler.processMetric.call_count == 5
    handler.processMetric.assert_called_with('foo.bar.baz', (timestamp, 4.0))

def test_datagramReceiver():
    assert False