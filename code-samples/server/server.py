import eventlet
import socketio
sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

@sio.on('connect')
def connect(sid, env):
    print('connecting ', sid)

@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)

@sio.on('event')
def message(sid, data):
    print('message received :  ', data)
    print('sid: ', sid)
    sio.emit('event', {'text': 'cake', 'url': 'https://www.danskan.se/wp-content/uploads/2019/06/Prinsesst%C3%A5rta.jpg'}, room=sid)

if __name__ == '__main__':
    port = 80
    print('Listening on port ' + str(port) + '...')
    eventlet.wsgi.server(eventlet.listen(('', port)), app)
