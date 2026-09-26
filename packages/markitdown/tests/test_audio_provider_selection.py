import io
import wave
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from markitdown import FileConversionException, MarkItDown, StreamInfo
from markitdown.converters import _audio_converter, _transcribe_audio


def _wav():
    stream = io.BytesIO()
    with wave.open(stream, "wb") as audio:
        audio.setnchannels(1)
        audio.setsampwidth(2)
        audio.setframerate(8000)
        audio.writeframes(b"\x00\x00" * 80)
    stream.seek(0)
    return stream


@pytest.fixture
def google(monkeypatch):
    recognize = Mock(return_value="Google transcript")
    monkeypatch.setattr(_transcribe_audio.sr.Recognizer, "recognize_google", recognize)
    monkeypatch.setattr(_audio_converter, "exiftool_metadata", lambda *a, **kw: {})
    return recognize


@pytest.mark.parametrize(
    "failure", [RuntimeError("service unavailable"), AttributeError("no audio API")]
)
def test_selected_client_failure_does_not_send_audio_to_google(google, failure):
    client = Mock()
    client.audio.transcriptions.create.side_effect = failure
    with pytest.raises(FileConversionException):
        MarkItDown(llm_client=client).convert_stream(
            _wav(), stream_info=StreamInfo(extension=".wav")
        )
    google.assert_not_called()
    client.audio.transcriptions.create.assert_called_once()


def test_supplied_client_does_not_depend_on_openai_import_flag(google, monkeypatch):
    monkeypatch.setattr(_transcribe_audio, "IS_WHISPER_CAPABLE", False)
    client = Mock()
    client.audio.transcriptions.create.return_value = SimpleNamespace(text=" selected ")
    result = MarkItDown(llm_client=client).convert_stream(
        _wav(), stream_info=StreamInfo(extension=".wav")
    )
    assert result.markdown == "### Audio Transcript:\nselected"
    google.assert_not_called()
    upload = client.audio.transcriptions.create.call_args.kwargs["file"]
    assert upload[0] == "audio.wav"
    assert upload[1].startswith(b"RIFF")


def test_no_client_preserves_google_default(google):
    result = MarkItDown().convert_stream(
        _wav(), stream_info=StreamInfo(extension=".wav")
    )
    assert result.markdown == "### Audio Transcript:\nGoogle transcript"
    google.assert_called_once()
