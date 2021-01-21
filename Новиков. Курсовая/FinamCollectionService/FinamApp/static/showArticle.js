async function showArticleInformation() {
    let pathUrl = document.location.pathname;
    let articleId = parseInt(pathUrl.slice(pathUrl.lastIndexOf('/') + 1));

    let elementArticleTitle = document.getElementById("titleArticle");
    let elementArticleTitleInBody = document.getElementById("titleArticleInBody");
    let elementArticleUrl = document.getElementById("urlArticle");
    let elementArticleCategory = document.getElementById("categoryArticle");
    let elementArticleText = document.getElementById("textArticle");
    let elementArticleLayer = document.getElementById("articleInformationLayer");

    let response = await fetch("/api/articles/" + articleId.toString(), {
        method: "GET"
    });

    if (response.ok) {
        let articleInformation = await response.json();

        elementArticleTitle.textContent = articleInformation.title;
        elementArticleTitleInBody.innerHTML = articleInformation.title;
        elementArticleUrl.innerHTML = "Ссылка на статью: <a href='" + articleInformation.source + "'>" + articleInformation.source + "</a>";
        elementArticleCategory.innerHTML = "Категория: " + articleInformation.category;
        elementArticleText.innerHTML = articleInformation.text;
    } else {
        if (response.status == 404) {
            elementArticleLayer.textContent = "Такой статьи нет (((";
        } else {
            elementArticleLayer.textContent = "Что-то пошло не так. Попробуйте снова загрузить статью";
        }
    }
}