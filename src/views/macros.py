
def text(request, name, error):

    if request.form.get(name):
        return request.form.get(name)
    else:
        msg = f"{name.capitalize()} muss ausgefüllt sein."
        error.append(msg)
        return None


select = text


def radio(request, name, error, yes='ja', no='nein'):

    if request.form.get(name) == yes:
        return True
    if request.form.get(name) == no:
        return False
    else:
        if len(name) == 5:
            msg = f"{name[:3].capitalize()} {name[-2:].capitalize()} muss ausgefüllt sein."
        else:
            msg = f"{name.capitalize()} muss ausgefüllt sein."
        error.append(msg)
        return None
