#install pip install azure-cognitiveservices-speech
import azure.cognitiveservices.speech as speechsdk
from dotenv import dotenv_values

config = dotenv_values('app/credentials.env')

speech_to_text_key = config["speech_to_text_key"]
speech_to_text_region = config["speech_to_text_region"]

def recognize_speech():
    """performs one-shot speech recognition from the default microphone with auto language detection"""
    speech_config = speechsdk.SpeechConfig(subscription=speech_to_text_key, region=speech_to_text_region)

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    # Create the auto detection language configuration with the potential source language candidates
    auto_detect_source_language_config = \
        speechsdk.languageconfig.AutoDetectSourceLanguageConfig(languages=["fr-FR", "en-US","hi-IN","it-IT"])
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, auto_detect_source_language_config=auto_detect_source_language_config)
    result = speech_recognizer.recognize_once()

    # Check the result
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        auto_detect_source_language_result = speechsdk.AutoDetectSourceLanguageResult(result)
        print("Recognized: {} in language {}".format(result.text, auto_detect_source_language_result.language))
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized")
        return ("No speech could be recognized")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
        return ("Speech Recognition canceled: {}".format(cancellation_details.reason))

recognize_speech()