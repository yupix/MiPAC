from mipac.actions.note import create_note_body


def test_create_note_body_without_files():
    body = create_note_body(text="hello", reply_id="n1")
    assert body["text"] == "hello"
    assert body["replyId"] == "n1"
    assert "fileIds" not in body


def test_create_note_body_with_file_ids():
    body = create_note_body(text="hello", files=["f1", "f2"])
    assert body["fileIds"] == ["f1", "f2"]
