# -*- encoding: utf-8 -*-

"""Tests for vumi.blinkenlights.heartbeat.publisher"""

import json

from twisted.trial.unittest import TestCase
from twisted.internet.defer import inlineCallbacks

from vumi.tests.utils import get_stubbed_channel
from vumi.tests.fake_amqp import FakeAMQPBroker
from vumi.blinkenlights.heartbeat import publisher
from vumi.errors import MissingMessageField


class MockHeartBeatPublisher(publisher.HeartBeatPublisher):

    # stub out the LoopingCall task
    def _start_looping_task(self):
        self._task = None


class TestHeartBeatPublisher(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def gen_fake_attrs(self):
        attrs = {
            'version': publisher.HeartBeatMessage.VERSION_20130319,
            'system_id': "system-1",
            'worker_id': "worker-1",
            'hostname': "test-host-1",
            'timestamp': 100,
            'pid': 43,
        }
        return attrs

    @inlineCallbacks
    def test_publish_heartbeat(self):
        self.broker = FakeAMQPBroker()
        channel = yield get_stubbed_channel(self.broker)
        pub = MockHeartBeatPublisher(self.gen_fake_attrs)
        pub.start(channel)
        pub._beat()

        [msg] = self.broker.get_dispatched("vumi.health", "heartbeat.inbound")
        self.assertEqual(json.loads(msg.body), self.gen_fake_attrs())

    def test_message_validation(self):
        attrs = self.gen_fake_attrs()
        attrs.pop("version")
        self.assertRaises(MissingMessageField, publisher.HeartBeatMessage,
                          **attrs)
        attrs = self.gen_fake_attrs()
        attrs.pop("system_id")
        self.assertRaises(MissingMessageField, publisher.HeartBeatMessage,
                          **attrs)
        attrs = self.gen_fake_attrs()
        attrs.pop("worker_id")
        self.assertRaises(MissingMessageField, publisher.HeartBeatMessage,
                          **attrs)
