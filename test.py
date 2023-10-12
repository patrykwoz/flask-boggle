from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle
import json


class FlaskTests(TestCase):
    def test_render_home(self):
        with app.test_client() as client:
            # import pdb
            # pdb.set_trace()
            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Play Boggle</h1>', html)
    
    def test_handle_endgame(self):
        with app.test_client() as client:
            import pdb
            data={'score':25, 'endscore':'0'}
            data_to_send = json.dumps(data)
            res = client.post('/game-finished', data=data_to_send, content_type='application/json')
            
            highest_score = res.json.get('highestscore')

            self.assertEqual(res.status_code, 200)
            self.assertEqual(highest_score, 25)
    
    def test_handle_reset(self):
        with app.test_client() as client:
            res = client.get('/handle-reset')

            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, 'http://localhost/')

    def test_handle_reset_followed(self):
        with app.test_client() as client:
            res = client.get('/handle-reset', follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Play Boggle</h1>', html)
    
    def test_game_finished_session(self):
        with app.test_client() as client:
            data={'score':25, 'endscore':'0'}
            data_to_send = json.dumps(data)
            res = client.post('/game-finished', data=data_to_send, content_type='application/json')

            self.assertEqual(res.status_code, 200)
            self.assertEqual(session['highest_score'], 25)

    def test_changing_session (self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['highest_score'] = 1500
            res = client.get('/')
            self.assertEqual(res.status_code, 200)
            self.assertEqual(session['highest_score'], 1500)