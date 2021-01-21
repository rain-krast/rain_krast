async function filterByCategory() {
    let elementCategorySelect = document.getElementById("categorySelect");
    let textCategory = elementCategorySelect.value;

    await showArticlesOnPage(textCategory, 1);
}

function showPages(countArticles, pageLimit, category, page) {
    let elementDivForPages = document.getElementById("pages");
    let lastPage = Math.ceil(countArticles / pageLimit);

    elementDivForPages.innerHTML = "";
    let textPages = "";

    for (let i = 1; i <= lastPage; i++) {
        if (i != page) {
            textPages = textPages + '<button onclick="showArticlesOnPage(' + "'" + category + "'," + i.toString() + ')">' + i.toString() + "</button>";
        } else {
            textPages = textPages + '<button onclick="showArticlesOnPage(' + "'" + category + "'," + i.toString() + ')"><b>' + i.toString() + "</b></button>";
        }
    }

    elementDivForPages.innerHTML = textPages;
}

async function showArticlesOnPage(category, page) {
    let elementErrorFilter = document.getElementById("filterError");
    let elementDivPages = document.getElementById("pages");
    let elementDivArticles = document.getElementById("filteredArticles");
    let elementCountArticles = document.getElementById("countArticles");

    elementErrorFilter.hidden = true;
    elementErrorFilter.textContent = "";
    elementCountArticles.textContent = "";
    elementDivPages.textContent = "";
    elementDivArticles.innerHTML = "<img src='/static/media/load.gif'/>";

    if (category == '') {
        let jsonForFetch = {
            page: page
        };

        let response = await fetch("/api/articles/all", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(jsonForFetch)
        });

        if (response.ok) {
            let dataResult = await response.json();
            showArticlesData(dataResult);
            showPages(dataResult.len, dataResult.pageLimit, category, page);
        } else {
            elementDivArticles.innerHTML = "";
            elementErrorFilter.hidden = false;
            elementErrorFilter.textContent = "Что-то пошло не так. Повторите попытку";
        }
    } else {
        let jsonForFetch = {
            category: category,
            page: page
        };

        let response = await fetch("/api/articles/filter-by-category", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(jsonForFetch)
        });

        if (response.ok) {
            let dataResult = await response.json();
            showArticlesData(dataResult);
            showPages(dataResult.len, dataResult.pageLimit, category, page);
        } else {
            elementDivArticles.innerHTML = "";
            elementErrorFilter.hidden = false;
            elementErrorFilter.textContent = "Что-то пошло не так. Повторите попытку";
        }
    }
}

function showArticlesData(data) {
    let elementDivArticles = document.getElementById("filteredArticles");
    let elementCountArticles = document.getElementById("countArticles");
    let textForDivArticles = "";

    elementCountArticles.textContent = "Количество новостный статей: " + data.len.toString();

    for (let i = 0; i < data.articles.length; i++) {
        textForDivArticles = textForDivArticles + "<div id='article" + data.articles[i].id.toString() + "'><a href='/articles/" + data.articles[i].id.toString() + "'>";
        textForDivArticles = textForDivArticles + data.articles[i].title + "</a>";
        textForDivArticles = textForDivArticles + "<br><p>Категория: " + data.articles[i].category + "</p>";
        textForDivArticles = textForDivArticles + "<img src='/static/media/delete.png' height='25px' weight='25px' onclick='deleteArticle(" + data.articles[i].id.toString() + ")'/>";
        textForDivArticles = textForDivArticles + "<div><p hidden id='deleteErrorArticle" + data.articles[i].id.toString() + "'></p></div></div>";
    }

    elementDivArticles.innerHTML = textForDivArticles;

    if (data.articles.length == 0) {
        elementDivArticles.textContent = "К сожалению таких новостных статей нет";
    }
}

async function deleteArticle(id) {
    let elementArticleLayer = document.getElementById("article" + id.toString());
    let elementArticleDeleteError = document.getElementById("deleteErrorArticle" + id.toString());

    elementArticleDeleteError.hidden = true;
    elementArticleDeleteError.textContent = "";

    let response = await fetch("/api/articles/" + id.toString(), {
        method: "DELETE"
    });

    if (response.ok) {
        elementArticleLayer.textContent = "Новостная статья успешно удалена";
    } else {
        if (response.status == 400) {
            elementArticleDeleteError.hidden = false;
            elementArticleDeleteError.textContent = "Такая новостная статья уже была удалена";
        } else {
            elementArticleDeleteError.hidden = false;
            elementArticleDeleteError.textContent = "Что-то пошло не так. Повторите запрос";
        }
    }
}