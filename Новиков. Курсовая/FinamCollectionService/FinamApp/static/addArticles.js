async function addArticle() {
    let elementInputUrl = document.getElementById("inputUrl");
    let elementInputCategory = document.getElementById("inputCategory");
    let elementInputTitle = document.getElementById("inputTitle");
    let elementInputText = document.getElementById("inputText");

    let elementUrlError = document.getElementById("urlError");
    let elementCategoryError = document.getElementById("categoryError");
    let elementTitleError = document.getElementById("titleError");
    let elementTextError = document.getElementById("textError");

    let elementAddResult = document.getElementById("resultAdd");
    let elementAddError = document.getElementById("addError");

    elementAddError.hidden = true;
    elementAddError.textContent = "";
    elementAddResult.textContent = "";

    elementUrlError.hidden = true;
    elementCategoryError.hidden = true;
    elementTitleError.hidden = true;
    elementTextError.hidden = true;
    elementUrlError.textContent = "";
    elementCategoryError.textContent = "";
    elementTitleError.textContent = "";
    elementTextError.textContent = "";

    let url = elementInputUrl.value;
    let category = elementInputCategory.value;
    let title = elementInputTitle.value;
    let text = elementInputText.value;

    let signalToAdd = true;

    if (url.trim() != '') {
        if (url.length <= 350) {
            let regExpUrl = /^(?:(?:https?):\/\/(?:[a-z0-9_-]{1,32}(?::[a-z0-9_-]{1,32})?@)?)?(?:(?:[a-z0-9-]{1,128}\.)+(?:com|net|org|mil|edu|arpa|ru|gov|biz|info|aero|inc|name|[a-z]{2})|(?!0)(?:(?!0[^.]|255)[0-9]{1,3}\.){3}(?!0|255)[0-9]{1,3})(?:\/[a-z0-9.,_@%&?+=\~\/-]*)?(?:#[^ \'\"&<>]*)?$/i;
            if (!regExpUrl.test(url)) {
                elementUrlError.hidden = false;
                elementUrlError.textContent = "Ссылка на статью некорректна";
                signalToAdd = false;
            }
        } else {
            elementUrlError.hidden = false;
            elementUrlError.textContent = "Ссылка слишком длинная. Максимальное кол-во символов - 350";
            signalToAdd = false;
        }
    } else {
        elementUrlError.hidden = false;
        elementUrlError.textContent = 'Ссылка на статью не заполнена';
        signalToAdd = false;
    }

    if (title.trim() != '') {
        if (title.length > 300) {
            elementTitleError.hidden = false;
            elementTitleError.textContent = "Заголовок статьи слишком длинный. Максимальное кол-во символов - 300";
            signalToAdd = false;
        }
    } else {
        elementTitleError.hidden = false;
        elementTitleError.textContent = "Заголовок статьи не заполнен";
        signalToAdd = false;
    }

    if (text.trim != '') {
        if (text.length > 15000) {
            elementTextError.hidden = false;
            elementTextError.textContent = "Текст статьи слишком длинный. Максимальное кол-во символов - 15000";
            signalToAdd = false;
        }
    } else {
        elementTextError.hidden = false;
        elementTextError.textContent = "Текст статьи не заполнен";
        signalToAdd = false;
    }

    if (signalToAdd) {
        let jsonForFetch = {
            source: url,
            title: title,
            category: category,
            text: text
        };

        let response = await fetch("api/articles", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(jsonForFetch)
        });

        if (response.ok) {
            elementAddResult.textContent = "Новостная статья была успешно добавлена в коллекцию";
        }
        else {
            elementAddError.hidden = false;
            elementAddError.textContent = "Что-то пошло не так. Повторите запрос";
        }
    }
}