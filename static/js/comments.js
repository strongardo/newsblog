const article = document.querySelector('article');
const slug = article.dataset.slug;

const commentsContainer = document.getElementById('comments-container');
const commentForm = document.getElementById('comment-form');

const successBlock = document.getElementById('comment-success');

function formatDate(dateString) {
    return new Date(dateString)
        .toLocaleString('ru-RU');
}

function getCookie(name) {

    let cookieValue = null;

    if (document.cookie && document.cookie !== '') {

        const cookies = document.cookie.split(';');

        for (let cookie of cookies) {

            cookie = cookie.trim();

            if (cookie.startsWith(name + '=')) {

                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );

                break;
            }

        }

    }

    return cookieValue;
}

function renderComments(comments) {

    if (comments.length === 0) {

        commentsContainer.innerHTML = `
            <p class="text-gray-500">
                Пока нет комментариев.
            </p>
        `;

        return;
    }

    commentsContainer.innerHTML = '';

    comments.forEach(comment => {

        commentsContainer.insertAdjacentHTML(
            'beforeend',
            `
            <div class="border border-gray-200 rounded-lg p-4">

                <div class="flex items-center justify-between mb-2">

                    <span class="font-medium text-gray-900">
                        ${comment.author_name}
                    </span>

                    <span class="text-sm text-gray-500">
                        ${formatDate(comment.created_at)}
                    </span>

                </div>

                <p class="text-gray-700 whitespace-pre-line">
                    ${comment.text}
                </p>

            </div>
            `
        );

    });

}

async function loadComments() {
    try {
        const response = await fetch(
            `/api/articles/${slug}/comments/`
        );

        if (!response.ok) {
            throw new Error('Ошибка загрузки комментариев');
        }

        const comments = await response.json();

        renderComments(comments);

    } catch (error) {
        console.error(error);

        commentsContainer.innerHTML = `
            <p class="text-red-500">
                Не удалось загрузить комментарии.
            </p>
        `;
    }
}

async function createComment(event) {

    event.preventDefault();

    const formData = new FormData(commentForm);
    const csrftoken = getCookie('csrftoken');

    const commentData = {
        author_name: formData.get('author_name'),
        text: formData.get('text'),
    };

    try {

        const response = await fetch(
            `/api/articles/${slug}/comments/`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify(commentData),
            }
        );

        if (!response.ok) {
            throw new Error('Ошибка создания комментария');
        }

        commentForm.reset();

        await loadComments();

        successBlock.classList.remove('hidden');

        setTimeout(() => {
            successBlock.classList.add('hidden');
        }, 3000);

        // commentsContainer.scrollIntoView({
        //     behavior: 'smooth'
        // });

    } catch (error) {

        console.error(error);

        alert('Не удалось добавить комментарий');

    }

}

document.addEventListener(
    'DOMContentLoaded',
    loadComments
);

commentForm.addEventListener(
    'submit',
    createComment
);