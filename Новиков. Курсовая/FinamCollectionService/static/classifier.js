async function classify() {
    let elementTextToClassify = document.getElementById("textForClassify");
    let elementResultOfClassify = document.getElementById("classifyResult");
    let elementErrorOfClassify = document.getElementById("classifyError");

    elementResultOfClassify.textContent = "";
    elementErrorOfClassify.hidden = true;
    elementErrorOfClassify.textContent = "";

    let textToClassify = elementTextToClassify.value;

    if (textToClassify.trim() != "") {
        if (textToClassify.length <= 15000) {
            let jsonForFetch = {
                "text": textToClassify
            };

            let response = await fetch("/api/classify", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(jsonForFetch)
            });

            if (response.ok) {
                let resultOfClassify = await response.json();
                elementResultOfClassify.textContent = resultOfClassify.category;
            } else {
                elementErrorOfClassify.hidden = false;
                elementErrorOfClassify.textContent = "Что-то пошло не так, попробуйте снова";
            }
        } else {
            elementErrorOfClassify.hidden = false;
            elementErrorOfClassify.textContent = "Текст для классификации слишком длинный. Предел 15000 символов";
        }
    } else {
        elementErrorOfClassify.hidden = false;
        elementErrorOfClassify.textContent = "Текст для классификации пуст";
    }
}

async function learnModel() {
    let elementLearnResult = document.getElementById("learnResult");
    let elementLearnError = document.getElementById("learnError");
    let elementLearnLoad = document.getElementById("learnLoad");

    elementLearnLoad.hidden = false;
    elementLearnResult.textContent = "";
    elementLearnError.hidden = true;
    elementLearnError.textContent = "";

    let response = await fetch("/api/model-learn", {
        method: "POST"
    });

    elementLearnLoad.hidden = true;

    if (response.ok) {
        elementLearnResult.textContent = "Переобучение модели классификатора успешно выполнено";
    } else {
        elementLearnError.hidden = false;
        elementLearnError.textContent = "Что-то пошло не так. Попробуйте снова";
    }
}