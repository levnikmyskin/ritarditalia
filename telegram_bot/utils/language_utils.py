import gettext

italian = gettext.translation('it', './translations', languages=['it'])
# english = gettext.translation('trenitalia', './translations', languages=['en'])
monella = gettext.translation('mn', './translations', languages=['mn'])

italian.install()


def set_language(code: str):
    if code == "it":
        italian.install()
        # return italian
    elif code == "en":
        english.install()
        # return english
    elif code == "mn":
        monella.install()
        # return monella
