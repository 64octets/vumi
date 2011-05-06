import time
from twisted.trial.unittest import TestCase
from vumi.session import VumiSession, TemplatedDecisionTree, PopulatedDesicionTree, TraversedDecisionTree

class SessionTestCase(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_session_decision_tree(self):
        sess1 = VumiSession()
        sess2 = VumiSession()
        sess3 = VumiSession()
        dt1 = TemplatedDecisionTree()
        dt2 = PopulatedDesicionTree()
        dt3 = TraversedDecisionTree()
        sess1.set_decision_tree(dt1)
        sess2.set_decision_tree(dt2)
        sess3.set_decision_tree(dt3)
        # baby steps
        self.assertEquals(sess1.get_decision_tree(), dt1)
        self.assertEquals(sess2.get_decision_tree(), dt2)
        self.assertEquals(sess3.get_decision_tree(), dt3)
        # the new TraversedDecisionTree should not be completed
        self.assertFalse(dt3.is_completed())

        test_yaml = '''
        __start__:
            next: users

        users:
            question:
                english: "Which user are you ?"
            options: name
            action: select
            next: items

        items:
            question:
                english: "Which item ?"
            options: name
            action: select
            next: stuff

        stuff:
            question:
                english: "How much stuff ?"
            validate: integer
            action: save
            next: things

        things:
            question:
                english: "How many things ?"
            validate: integer
            action: save
            next: timestamp

        timestamp:
            question:
                english: "Which day was it ?"
            options:
                  - display:
                        english: "Today"
                    action: save_today
                    next: __finish__

                  - display:
                        english: "Yesterday"
                    action: save_yesterday
                    next: __finish__

                  - display:
                        english: "Earlier"
                    action: question
                    next:
                        question:
                            english: "Please enter the day [dd/mm/yyyy] ?"
                        validate: date
                        action: save
                        next: __finish__

        __finish__:
            display:
                english: "Thank you"
        '''

        test_json = '''
        {
            "users": [
                {
                    "name": "Simon",
                    "items": [
                        {
                            "name": "alpha",
                            "stuff": 0,
                            "things": 0,
                            "timestamp": 0,
                            "id": "1.1"
                        },
                        {
                            "name": "beta",
                            "stuff": 0,
                            "things": 0,
                            "timestamp": 0,
                            "id": "1.2"
                        }
                    ],
                    "timestamp": "1234567890",
                    "id": "1"
                },
                {
                    "name": "David",
                    "items": [],
                    "timestamp": "1234567890",
                    "id": "2"
                }
            ],
            "msisdn": "12345"
        }
        '''

        # just check the load operations don't blow up
        self.assertEquals(dt1.load_yaml_template(test_yaml), None)
        self.assertEquals(dt2.load_yaml_template(test_yaml), None)
        self.assertEquals(dt2.load_json_data(test_json), None)
        self.assertEquals(dt3.load_yaml_template(test_yaml), None)
        self.assertEquals(dt3.load_json_data(test_json), None)

        before = dt3.dumps()
        dt3.start()
        # simple backtracking test
        dt3.previous()
        self.assertEquals(before, dt3.dumps())
        dt3.start()
        print ""
        #print dt3.dumps()
        print "\n", dt3.question()
        dt3.answer(1)
        print dt3.dumps()
        print "\n", dt3.question()
        dt3.answer(1)
        print dt3.dumps()
        print "\n", dt3.question()
        #dt3.answer(42)
        #print dt3.dumps()






        print "\n\n"
        time.sleep(2)
