def test_health_route(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_websocket_room_connect_and_message(client):
    with client.websocket_connect("/ws/rooms/python?username=alice") as alice:
        connect_event = alice.receive_json()
        assert connect_event["type"] == "connect"

        with client.websocket_connect("/ws/rooms/python?username=bob") as bob:
            alice_event = alice.receive_json()
            bob_event = bob.receive_json()
            assert alice_event["type"] == "connect"
            assert bob_event["type"] == "connect"

            alice.send_json({"type": "message", "text": "Всем привет"})
            alice_message = alice.receive_json()
            bob_message = bob.receive_json()

            assert alice_message["type"] == "message"
            assert bob_message["type"] == "message"
            assert alice_message["text"] == "Всем привет"
            assert bob_message["text"] == "Всем привет"


def test_websocket_long_message_returns_error(client):
    with client.websocket_connect("/ws/rooms/python?username=alice") as alice:
        alice.receive_json()
        alice.send_json({"type": "message", "text": "x" * 301})
        error_event = alice.receive_json()

        assert error_event["type"] == "error"
        assert error_event["detail"] == "Message is too long"


def test_room_users_endpoint_updates_after_disconnect(client):
    with client.websocket_connect("/ws/rooms/python?username=alice"):
        pass

    response = client.get("/rooms/python/users")
    assert response.status_code == 200
    assert response.json() == {"room_id": "python", "users": []}
