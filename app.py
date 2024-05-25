import os
from datetime import datetime
from ai import gpt3_5, gpt3_5_16k, gpt4, gpt4_turbo, gpt4_turbo_16k
from freeGPT.Client import pollinations
from flask import Flask, render_template, request, session, send_from_directory
import secrets


app = Flask(__name__, static_folder=os.getcwd()+'/client', template_folder=os.getcwd()+'/client')
message = ""
stream = True
model = 'gpt-3.5-turbo'
settings = ""
app.secret_key = secrets.token_hex(16)

model_Func = [gpt3_5, gpt3_5_16k, gpt4, gpt4_turbo, gpt4_turbo_16k]
models = ['gpt-3.5-turbo', 'gpt-3.5-turbo-16k', 'gpt-4', "gpt-4-turbo", "gpt-4-turbo-extended"]
model_names = ['GPT 3.5 TURBO', 'GPT 3.5 TURBO 16K', 'GPT 4', "GPT 4-turbo", "GPT 4-turbo Extended"]

@app.route("/robots.txt")
def robots_dot_txt():
    print(app.static_folder)
    return send_from_directory(app.static_folder, "robots.txt")

@app.route('/', methods=['GET', 'POST'])
def main():
    gpt = "url('client/img/gpt.png')"
    pricing_link = "client/html/login/index.html"
    media = ["client/img/gmail.png", "client/img/youtube.png", "client/img/instagram.png"]
    description_list = ["AI Text Companion is ChapGPT powered ai assistant, which can help you to write even diploma",
                        "AI Homework Helper is ChapGPT powered ai assistant, which can help you to write even diploma",
                        "AI Test Maker is ChapGPT powered ai assistant, which can help you to simplify teacher work",
                        "AI Mods Maker is ChapGPT powered ai assistant, which can help you to make your game interesting",
                        "AI Code Generator is ChapGPT powered ai assistant, which can help you to make AI, but you already have it here",
                        "AI Grammar Spelling is ChapGPT powered ai assistant, which can help you enrich your speech",
                        "AI Translator is ChapGPT powered ai assistant, which can help you enrich your vocabulary",
                        "AI Song Writer is ChapGPT powered ai assistant, which can help you make a music party",
                       "AI Image Painter is ChapGPT powered ai assistant, which can help you to draw a picture.",
                       "AI TTS Network is ChapGPT powered ai assistant, which can help you make alive your text",
                       "AI Video Creator is ChapGPT powered ai assistant, which can help you to draw a film.",
                        "AI Service Helper is ChapGPT powered ai assistant, which can help you find path to favourite site",
                        "AI Searcher is ChapGPT powered ai assistant, which can help you find path to favourite AI",
                        "AI Custom Model is ChapGPT powered ai assistant, maybe you were searching for it all your life long",
                       ]
    names_list = ["AI Text Companion", "AI Homework Helper", "AI Test Maker", "AI Mods Maker", "AI Code Generator", "AI Grammar Spelling",
                  "AI Translator", "AI Song Writer", "AI Image Painter", "AI TTS Network", "AI Video Creator",
                  "AI Service Helper", "AI Searcher", "AI Custom Model"]
    picture_list = ["client/img/text.png", "client/img/homework.png", "client/img/test.png", "client/img/mods.png", "client/img/code.png",
                    "client/img/grammar.png", "client/img/translator.png", "client/img/song.png",
                    "client/img/image.png", "client/img/tts.png", "client/img/video.png",
                    "client/img/service.png", "client/img/search.png", "client/img/text.png",]
    app_links = ["/chat", "/homework", "/test", "/mods", "/code", "/grammar",
                 "/translator", "/song", "/image", "/tts", "/video", "/service", "/searcher", "/custom"]
    def create(description, image2, ai_name, link):
        if ai_name == "AI Text Companion":
            div = f"""<div class="ai-container">
                <img src="{image2}" alt="Image of AI">
                <h2><a href="{link}">{ai_name}</a></h2>
                <p>{description}</p></div>"""
            return div
        else:
            div = f"""<div class="ai-container next">
                            <img src="{image2}" alt="Image of AI">
                            <h2><a href="{link}">{ai_name}</a></h2>
                            <p>{description}</p></div>"""
            return div
    html = ""
    for i in range(len(description_list)):
       html += create(description_list[i], picture_list[i], names_list[i], app_links[i])
    return render_template('/html/index/index.html', ai_list=html, gpt=gpt, media=media, pricing_link=pricing_link)

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    from ai.an_ai import list_of_banned
    global models, model_names
    if_selected = ""
    if request.method == 'POST':
        modelsGPT = ""
        modelS = request.form.get('model')
        messageText = request.form.get('message')
        for i in range(len(models)):
            if modelS == models[i]:
                if_selected = "selected"
            modelsGPT += f" <option {if_selected} value='{models[i]}'>{model_names[i]}</option>"
            if_selected = ""
        session['settings'] = f"""
                                    <select name="model" class="select-mod">
                                    {modelsGPT}
                                    </select>
                                """
        answerText = ""
        for i in list_of_banned:
            if i in messageText.lower():
                answerText = "You are banned to ask such questions"
        if answerText != "You are banned to ask such questions":
            answerText = model_Func[models.index(modelS)].Completion().create(messageText)
            answerText = answerText.replace('\n', '')
        session['message'] = session.get('message', '') + f"""
                        <div class="container">
                            <img src="client/img/prof.png" width="30" height="30" alt="Avatar" class="right">
                            <p>{messageText}</p> <span class="time-left">{datetime.now().strftime("%H:%M")}</span>
                        </div>
                        <div class="container darker">
                            <img src="client/img/Atutum.png" width="30" height="30" alt="Avatar" class="right">
                            <p name="current-dialog">{answerText}</p> <span class="time-left">{datetime.now().strftime("%H:%M")}</span>
                        </div> 
                        """
        return render_template('/html/chat/index.html', settings=session['settings'], message=session['message'])
    else:
        global model
        modelsGPT = ""
        for i in range(len(models)):
            if model == models[i]:
                if_selected = "selected"
            modelsGPT += f" <option {if_selected} value='{models[i]}'>{model_names[i]}</option>"
            if_selected = ""
        session['settings'] = f"""
                <select name="model" class="select-mod">
                {modelsGPT}
                </select>
            """
        return render_template('/html/chat/index.html', settings=session['settings'])

@app.route('/image', methods=['GET', 'POST'])
def image():
    messageText = request.form.get('prompt')
    if messageText is not None:
        image1 = pollinations.Generation().create(messageText)
        with open("client/img/pic.png", "wb") as file_image:
            file_image.write(image1)
        from PIL import Image
        image1 = Image.open("client/img/pic.png")
        width, height = image1.size
        image1 = image1.crop((0, 0, width, height - 70))
        image1.save("client/img/pic.png")

        return render_template('/html/image/index.html', image="client/img/pic.png")
    else:
        return render_template('/html/image/index.html')

@app.route('/tts', methods=['GET', 'POST'])
def tts():
    messageText = request.form.get('prompt')
    if messageText is not None:
        from TTS.tts import va_speak_save
        va_speak_save(messageText)
        class_contole_audio = "active"
        return render_template('/html/tts/index.html', class_contole_audio=class_contole_audio, audio="client/audio/result_audio.wav")
    else:
        class_contole_audio = "inactive"
        return render_template('/html/tts/index.html', class_contole_audio=class_contole_audio, audio="client/audio/result_audio.wav")

@app.route('/homework', methods=['GET', 'POST'])
def homework():
    from ai.an_ai import list_of_banned
    global models, model_names
    if_selected = ""
    if request.method == 'POST':
        modelsGPT = ""
        modelS = request.form.get('model')
        subjectText = request.form.get('subject')
        messageText = request.form.get('message')
        for i in range(len(models)):
            if modelS == models[i]:
                if_selected = "selected"
            modelsGPT += f" <option {if_selected} value='{models[i]}'>{model_names[i]}</option>"
            if_selected = ""
        session['settings'] = f"""
                                <select name="model" class="select-mod">
                                {modelsGPT}
                                </select>
                            """
        ask = f"You are the best Homework Helper of {subjectText}, please do this task {messageText}"
        answerText = ""
        for i in list_of_banned:
            if i in ask.lower():
                answerText = "You are banned to ask such questions"
        if answerText != "You are banned to ask such questions":
            answerText = model_Func[models.index(modelS)].Completion().create(ask)
            answerText = answerText.replace('\n', '')
        session['message'] = session.get('message', '') + f"""
                    <div class="container">
                        <img src="client/img/prof.png" width="30" height="30" alt="Avatar" class="right">
                        <p>{messageText}</p> <span class="time-left">{datetime.now().strftime("%H:%M")}</span>
                    </div>
                    <div class="container darker">
                        <img src="client/img/Atutum.png" width="30" height="30" alt="Avatar" class="right">
                        <p name="current-dialog">{answerText}</p> <span class="time-left">{datetime.now().strftime("%H:%M")}</span>
                    </div> 
                    """
        return render_template('/html/homework/index.html', settings=session['settings'], message=session['message'])
    else:
        global model
        modelsGPT = ""
        for i in range(len(models)):
            if model == models[i]:
                if_selected = "selected"
            modelsGPT += f" <option {if_selected} value='{models[i]}'>{model_names[i]}</option>"
            if_selected = ""
        session['settings'] = f"""
                <select name="model" class="select-mod">
                {modelsGPT}
                </select>
            """
        return render_template('/html/homework/index.html', settings=session['settings'])

@app.route('/test', methods=['GET', 'POST'])
def test():
    from ai.an_ai import list_of_banned, check_on_false
    global models, model_names
    if_selected = ""
    if request.method == 'POST':
        modelsGPT = ""
        modelS = request.form.get('model')
        subjectText = request.form.get('subject')
        messageText = request.form.get('message')
        for i in range(len(models)):
            if modelS == models[i]:
                if_selected = "selected"
            modelsGPT += f" <option {if_selected} value='{models[i]}'>{model_names[i]}</option>"
            if_selected = ""
        session['settings'] = f"""
                                <select name="model" class="select-mod">
                                {modelsGPT}
                                </select>
                            """
        ask = f"I want to test my knowledge about the {subjectText}. Write me a test paper for ongoing monitoring. " \
              f"Imagine that you are a teacher who knows how to make tests that will simultaneously test the student and help him learn new things. Pay attention to questions in which you can apply knowledge in practice, and not just rewrite memorized material. The test should involve critical thinking." \
              f"Follow examples of the best academic tests used in strong teaching programs. " \
              f"Make sure the work is relevant to the topic."
        if messageText is not None:
            ask += f" Also here is some comments to the test: {messageText}"
        answerText = ""
        for i in list_of_banned:
            if i in ask.lower():
                answerText = "You are banned to ask such questions"
        if answerText != "You are banned to ask such questions":
            answerText = model_Func[models.index(modelS)].Completion().create(ask)
            answerText = answerText.replace('\n', '')
            answerText = gpt4_turbo_16k.Completion().create(f"Write this text in html format(make it look like a test)(write a html code): {answerText}")
        session['message'] = session.get('message', '') + f"""
                    <div class="container">
                        <img src="client/img/prof.png" width="30" height="30" alt="Avatar" class="right">
                        <p>{messageText}</p> <span class="time-left">{datetime.now().strftime("%H:%M")}</span>
                    </div>
                    <div class="container darker">
                        <img src="client/img/Atutum.png" width="30" height="30" alt="Avatar" class="right">
                        <p name="current-dialog">{answerText}</p> <span class="time-left">{datetime.now().strftime("%H:%M")}</span>
                    </div> 
                    """
        return render_template('/html/test/index.html', settings=session['settings'], message=session['message'])
    else:
        global model
        modelsGPT = ""
        for i in range(len(models)):
            if model == models[i]:
                if_selected = "selected"
            modelsGPT += f" <option {if_selected} value='{models[i]}'>{model_names[i]}</option>"
            if_selected = ""
        session['settings'] = f"""
                <select name="model" class="select-mod">
                {modelsGPT}
                </select>
            """
        return render_template('/html/test/index.html', settings=session['settings'])

@app.route('/mods', methods=['GET', 'POST'])
def mods():
    from ai.an_ai import list_of_banned, check_on_false
    global models, model_names
    if_selected = ""
    if request.method == 'POST':
        modelsGPT = ""
        modelS = request.form.get('model')
        subjectText = request.form.get('subject')
        messageText = request.form.get('message')
        for i in range(len(models)):
            if modelS == models[i]:
                if_selected = "selected"
            modelsGPT += f" <option {if_selected} value='{models[i]}'>{model_names[i]}</option>"
            if_selected = ""
        session['settings'] = f"""
                                <select name="model" class="select-mod">
                                {modelsGPT}
                                </select>
                            """
        ask = f"I want to create mod for the game: {subjectText}. Write the code for making this {messageText}"
        answerText = ""
        for i in list_of_banned:
            if i in ask.lower():
                answerText = "You are banned to ask such questions"
        if answerText != "You are banned to ask such questions":
            answerText = model_Func[models.index(modelS)].Completion().create(ask)
            answerText = answerText.replace('\n', '')
            answerText = gpt4_turbo_16k.Completion().create(f"Write this text in html format(make it look like a test)(write a html code): {answerText}")
        session['message'] = session.get('message', '') + f"""
                    <div class="container">
                        <img src="client/img/prof.png" width="30" height="30" alt="Avatar" class="right">
                        <p>{messageText}</p> <span class="time-left">{datetime.now().strftime("%H:%M")}</span>
                    </div>
                    <div class="container darker">
                        <img src="client/img/Atutum.png" width="30" height="30" alt="Avatar" class="right">
                        <p name="current-dialog">{answerText}</p> <span class="time-left">{datetime.now().strftime("%H:%M")}</span>
                    </div> 
                    """
        return render_template('/html/mods/index.html', settings=session['settings'], message=session['message'])
    else:
        global model
        modelsGPT = ""
        for i in range(len(models)):
            if model == models[i]:
                if_selected = "selected"
            modelsGPT += f" <option {if_selected} value='{models[i]}'>{model_names[i]}</option>"
            if_selected = ""
        session['settings'] = f"""
                <select name="model" class="select-mod">
                {modelsGPT}
                </select>
            """
        return render_template('/html/mods/index.html', settings=session['settings'])

@app.route('/code', methods=['GET', 'POST'])
def code():
    from ai.an_ai import list_of_banned
    global models, model_names
    if_selected = ""
    if request.method == 'POST':
        modelsGPT = ""
        modelS = request.form.get('model')
        subjectText = request.form.get('subject')
        messageText = request.form.get('message')
        for i in range(len(models)):
            if modelS == models[i]:
                if_selected = "selected"
            modelsGPT += f" <option {if_selected} value='{models[i]}'>{model_names[i]}</option>"
            if_selected = ""
        session['settings'] = f"""
                                <select name="model" class="select-mod">
                                {modelsGPT}
                                </select>
                            """
        ask = f"I want to write code using the programming language of: {subjectText}. Write the code for making this {messageText}"
        answerText = ""
        for i in list_of_banned:
            if i in ask.lower():
                answerText = "You are banned to ask such questions"
        if answerText != "You are banned to ask such questions":
            answerText = model_Func[models.index(modelS)].Completion().create(ask)
            answerText = answerText.replace('\n', '')
            answerText = gpt4_turbo_16k.Completion().create(f"write html code to format this text to make it look like the python code: {answerText}")
        session['message'] = session.get('message', '') + f"""
                    <div class="container">
                        <img src="client/img/prof.png" width="30" height="30" alt="Avatar" class="right">
                        <p>{messageText}</p> <span class="time-left">{datetime.now().strftime("%H:%M")}</span>
                    </div>
                    <div class="container darker">
                        <img src="client/img/Atutum.png" width="30" height="30" alt="Avatar" class="right">
                        <p name="current-dialog"><div>{answerText}</div></p> <span class="time-left">{datetime.now().strftime("%H:%M")}</span>
                    </div> 
                    """
        return render_template('/html/code/index.html', settings=session['settings'], message=session['message'])
    else:
        global model
        modelsGPT = ""
        for i in range(len(models)):
            if model == models[i]:
                if_selected = "selected"
            modelsGPT += f" <option {if_selected} value='{models[i]}'>{model_names[i]}</option>"
            if_selected = ""
        session['settings'] = f"""
                <select name="model" class="select-mod">
                {modelsGPT}
                </select>
            """
        return render_template('/html/code/index.html', settings=session['settings'])

@app.route('/grammar', methods=['GET', 'POST'])
def grammar():
    from ai.an_ai import list_of_banned
    global models, model_names
    if_selected = ""
    if request.method == 'POST':
        modelsGPT = ""
        modelS = request.form.get('model')
        messageText = request.form.get('message')
        for i in range(len(models)):
            if modelS == models[i]:
                if_selected = "selected"
            modelsGPT += f" <option {if_selected} value='{models[i]}'>{model_names[i]}</option>"
            if_selected = ""
        session['settings'] = f"""
                                <select name="model" class="select-mod">
                                {modelsGPT}
                                </select>
                            """
        ask = f"Find and correct mistakes in following text: {messageText}"
        answerText = ""
        for i in list_of_banned:
            if i in ask.lower():
                answerText = "You are banned to ask such questions"
        if answerText != "You are banned to ask such questions":
            answerText = model_Func[models.index(modelS)].Completion().create(ask)
            answerText = answerText.replace('\n', '')
        session['message'] = session.get('message', '') + f"""
                    <div class="container">
                        <img src="client/img/prof.png" width="30" height="30" alt="Avatar" class="right">
                        <p>{messageText}</p> <span class="time-left">{datetime.now().strftime("%H:%M")}</span>
                    </div>
                    <div class="container darker">
                        <img src="client/img/Atutum.png" width="30" height="30" alt="Avatar" class="right">
                        <p name="current-dialog">{answerText}</p> <span class="time-left">{datetime.now().strftime("%H:%M")}</span>
                    </div> 
                    """
        return render_template('/html/grammar/index.html', settings=session['settings'], message=session['message'])
    else:
        global model
        modelsGPT = ""
        for i in range(len(models)):
            if model == models[i]:
                if_selected = "selected"
            modelsGPT += f" <option {if_selected} value='{models[i]}'>{model_names[i]}</option>"
            if_selected = ""
        session['settings'] = f"""
                <select name="model" class="select-mod">
                {modelsGPT}
                </select>
            """
        return render_template('/html/grammar/index.html', settings=session['settings'])

@app.route('/translator', methods=['GET', 'POST'])
def translator():
    from ai.an_ai import list_of_banned
    global models, model_names
    if_selected = ""
    if request.method == 'POST':
        modelsGPT = ""
        modelS = request.form.get('model')
        inLang = request.form.get('ipt_lng')
        outLang = request.form.get('opt_lng')
        messageText = request.form.get('message')
        for i in range(len(models)):
            if modelS == models[i]:
                if_selected = "selected"
            modelsGPT += f" <option {if_selected} value='{models[i]}'>{model_names[i]}</option>"
            if_selected = ""
        session['settings'] = f"""
                                <select name="model" class="select-mod">
                                {modelsGPT}
                                </select>
                            """
        ask = f"Translate this text: {messageText} from {inLang} to {outLang}"
        answerText = ""
        for i in list_of_banned:
            if i in ask.lower():
                answerText = "You are banned to ask such questions"
        if answerText != "You are banned to ask such questions":
            answerText = model_Func[models.index(modelS)].Completion().create(ask)
            answerText = answerText.replace('\n', '')
        session['message'] = session.get('message', '') + f"""
                    <div class="container">
                        <img src="client/img/prof.png" width="30" height="30" alt="Avatar" class="right">
                        <p>{messageText}</p> <span class="time-left">{datetime.now().strftime("%H:%M")}</span>
                    </div>
                    <div class="container darker">
                        <img src="client/img/Atutum.png" width="30" height="30" alt="Avatar" class="right">
                        <p name="current-dialog">{answerText}</p> <span class="time-left">{datetime.now().strftime("%H:%M")}</span>
                    </div> 
                    """
        return render_template('/html/translator/index.html', settings=session['settings'], message=session['message'])
    else:
        global model
        modelsGPT = ""
        for i in range(len(models)):
            if model == models[i]:
                if_selected = "selected"
            modelsGPT += f" <option {if_selected} value='{models[i]}'>{model_names[i]}</option>"
            if_selected = ""
        session['settings'] = f"""
                <select name="model" class="select-mod">
                {modelsGPT}
                </select>
            """
        return render_template('/html/translator/index.html', settings=session['settings'])

@app.route('/song', methods=['GET', 'POST'])
def song():
    from ai.an_ai import list_of_banned
    global models, model_names
    if_selected = ""
    if request.method == 'POST':
        modelsGPT = ""
        modelS = request.form.get('model')
        style = request.form.get('theme')
        theme = request.form.get('style')
        messageText = request.form.get('message')
        for i in range(len(models)):
            if modelS == models[i]:
                if_selected = "selected"
            modelsGPT += f" <option {if_selected} value='{models[i]}'>{model_names[i]}</option>"
            if_selected = ""
        session['settings'] = f"""
                                <select name="model" class="select-mod">
                                {modelsGPT}
                                </select>
                            """
        ask = f"write lyrics for a song in {style} style, using metaphors and epitypes on the topic {theme} (on the topic {messageText})"
        answerText = ""
        for i in list_of_banned:
            if i in ask.lower():
                answerText = "You are banned to ask such questions"
        if answerText != "You are banned to ask such questions":
            answerText = model_Func[models.index(modelS)].Completion().create(ask)
            answerText = answerText.replace('\n', '')
        session['message'] = session.get('message', '') + f"""
                    <div class="container">
                        <img src="client/img/prof.png" width="30" height="30" alt="Avatar" class="right">
                        <p>{messageText}</p> <span class="time-left">{datetime.now().strftime("%H:%M")}</span>
                    </div>
                    <div class="container darker">
                        <img src="client/img/Atutum.png" width="30" height="30" alt="Avatar" class="right">
                        <p name="current-dialog">{answerText}</p> <span class="time-left">{datetime.now().strftime("%H:%M")}</span>
                    </div> 
                    """
        return render_template('/html/song/index.html', settings=session['settings'], message=session['message'])
    else:
        global model
        modelsGPT = ""
        for i in range(len(models)):
            if model == models[i]:
                if_selected = "selected"
            modelsGPT += f" <option {if_selected} value='{models[i]}'>{model_names[i]}</option>"
            if_selected = ""
        session['settings'] = f"""
                <select name="model" class="select-mod">
                {modelsGPT}
                </select>
            """
        return render_template('/html/song/index.html', settings=session['settings'])

@app.route('/service', methods=['GET', 'POST'])
def service():
    from ai.an_ai import list_of_banned
    global models, model_names
    if_selected = ""
    if request.method == 'POST':
        modelsGPT = ""
        modelS = request.form.get('model')
        messageText = request.form.get('message')
        for i in range(len(models)):
            if modelS == models[i]:
                if_selected = "selected"
            modelsGPT += f" <option {if_selected} value='{models[i]}'>{model_names[i]}</option>"
            if_selected = ""
        session['settings'] = f"""
                                <select name="model" class="select-mod">
                                {modelsGPT}
                                </select>
                            """
        ask = f"Imagine that you are recommending services and sites, to complete this task {messageText}, recommend services that will help complete this task (provide a link for each service)"
        answerText = ""
        for i in list_of_banned:
            if i in ask.lower():
                answerText = "You are banned to ask such questions"
        if answerText != "You are banned to ask such questions":
            answerText = model_Func[models.index(modelS)].Completion().create(ask)
            answerText = answerText.replace('\n', '')
            answerText = gpt4_turbo_16k.Completion().create(
                f"Write this text in html format(make it look like a test)(write a html code): {answerText}")
        session['message'] = session.get('message', '') + f"""
                    <div class="container">
                        <img src="client/img/prof.png" width="30" height="30" alt="Avatar" class="right">
                        <p>{messageText}</p> <span class="time-left">{datetime.now().strftime("%H:%M")}</span>
                    </div>
                    <div class="container darker">
                        <img src="client/img/Atutum.png" width="30" height="30" alt="Avatar" class="right">
                        <p name="current-dialog">{answerText}</p> <span class="time-left">{datetime.now().strftime("%H:%M")}</span>
                    </div> 
                    """
        return render_template('/html/service/index.html', settings=session['settings'], message=session['message'])
    else:
        global model
        modelsGPT = ""
        for i in range(len(models)):
            if model == models[i]:
                if_selected = "selected"
            modelsGPT += f" <option {if_selected} value='{models[i]}'>{model_names[i]}</option>"
            if_selected = ""
        session['settings'] = f"""
                <select name="model" class="select-mod">
                {modelsGPT}
                </select>
            """
        return render_template('/html/service/index.html', settings=session['settings'])

@app.route('/searcher', methods=['GET', 'POST'])
def searcher():
    from ai.an_ai import list_of_banned
    global models, model_names
    if_selected = ""
    if request.method == 'POST':
        modelsGPT = ""
        modelS = request.form.get('model')
        messageText = request.form.get('message')
        for i in range(len(models)):
            if modelS == models[i]:
                if_selected = "selected"
            modelsGPT += f" <option {if_selected} value='{models[i]}'>{model_names[i]}</option>"
            if_selected = ""
        session['settings'] = f"""
                                <select name="model" class="select-mod">
                                {modelsGPT}
                                </select>
                            """
        ask = f"Imagine that you are recommending services and sites, to complete this task {messageText}, recommend services that will help complete this task (provide a link for each service)"
        answerText = ""
        for i in list_of_banned:
            if i in ask.lower():
                answerText = "You are banned to ask such questions"
        if answerText != "You are banned to ask such questions":
            answerText = model_Func[models.index(modelS)].Completion().create(ask)
            answerText = answerText.replace('\n', '')
            answerText = gpt4_turbo_16k.Completion().create(
                f"Write this text in html format(make it look like a test)(write a html code): {answerText}")
        session['message'] = session.get('message', '') + f"""
                    <div class="container">
                        <img src="client/img/prof.png" width="30" height="30" alt="Avatar" class="right">
                        <p>{messageText}</p> <span class="time-left">{datetime.now().strftime("%H:%M")}</span>
                    </div>
                    <div class="container darker">
                        <img src="client/img/Atutum.png" width="30" height="30" alt="Avatar" class="right">
                        <p name="current-dialog">{answerText}</p> <span class="time-left">{datetime.now().strftime("%H:%M")}</span>
                    </div> 
                    """
        return render_template('/html/searcher/index.html', settings=session['settings'], message=session['message'])
    else:
        global model
        modelsGPT = ""
        for i in range(len(models)):
            if model == models[i]:
                if_selected = "selected"
            modelsGPT += f" <option {if_selected} value='{models[i]}'>{model_names[i]}</option>"
            if_selected = ""
        session['settings'] = f"""
                <select name="model" class="select-mod">
                {modelsGPT}
                </select>
            """
        return render_template('/html/searcher/index.html', settings=session['settings'])

@app.route('/custom', methods=['GET', 'POST'])
def custom():
    from ai.an_ai import list_of_banned
    global models, model_names
    if_selected = ""
    if request.method == 'POST':
        modelsGPT = ""
        modelS = request.form.get('model')
        object1 = request.form.get('object')
        orient1 = request.form.get('orient')
        messageText = request.form.get('message')
        for i in range(len(models)):
            if modelS == models[i]:
                if_selected = "selected"
            modelsGPT += f" <option {if_selected} value='{models[i]}'>{model_names[i]}</option>"
            if_selected = ""
        session['settings'] = f"""
                                <select name="model" class="select-mod">
                                {modelsGPT}
                                </select>
                            """
        ask = f"Imagine you have a custom language AI model specialized on {object1} and thinks in a similar way to the neural network {orient1} and you need to complete the task: {messageText}"
        answerText = ""
        for i in list_of_banned:
            if i in ask.lower():
                answerText = "You are banned to ask such questions"
        if answerText != "You are banned to ask such questions":
            answerText = model_Func[models.index(modelS)].Completion().create(ask)
            answerText = answerText.replace('\n', '')
            answerText = gpt4_turbo_16k.Completion().create(
                f"Write this text in html format(make it look like a test)(write a html code): {answerText}")
        session['message'] = session.get('message', '') + f"""
                    <div class="container">
                        <img src="client/img/prof.png" width="30" height="30" alt="Avatar" class="right">
                        <p>{messageText}</p> <span class="time-left">{datetime.now().strftime("%H:%M")}</span>
                    </div>
                    <div class="container darker">
                        <img src="client/img/Atutum.png" width="30" height="30" alt="Avatar" class="right">
                        <p name="current-dialog">{answerText}</p> <span class="time-left">{datetime.now().strftime("%H:%M")}</span>
                    </div> 
                    """
        return render_template('/html/custom/index.html', settings=session['settings'], message=session['message'])
    else:
        global model
        modelsGPT = ""
        for i in range(len(models)):
            if model == models[i]:
                if_selected = "selected"
            modelsGPT += f" <option {if_selected} value='{models[i]}'>{model_names[i]}</option>"
            if_selected = ""
        session['settings'] = f"""
                <select name="model" class="select-mod">
                {modelsGPT}
                </select>
            """
        return render_template('/html/custom/index.html', settings=session['settings'])
if __name__ == "__main__":
    app.run(debug=True, port="8000")