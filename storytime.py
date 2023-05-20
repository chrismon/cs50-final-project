
import os
import openai
import azure.cognitiveservices.speech as speechsdk


def main():
    while True:
        subject = input("Hello, I am story-bot 3000. What subject would you like me to write a story about? ")
        if not subject:
            print("Subject cannot be blank.")
            continue
        break
    while True:
        try:
            words = int(input("How long (in words) should the story be? "))
            if words < 50:
                print("Story should be at least 50 words long.")
                continue
        except:
            print("Please enter a valid integer.")
            continue
        break
    
    story = getStory(subject, words)
    getAudio(story)


def getStory(subject, words):
    print("Getting story from OpenAI...")
    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"Write a {str(words)} word fairy tale about {subject}.",
    temperature=0.4,
    max_tokens=2000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    return response.choices[0]["text"]


def getAudio(text):
    print("Generating audo-book...")
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    speech_config.speech_synthesis_voice_name='en-US-JennyNeural'
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    speech_synthesizer.speak_text_async(text).get()


main()