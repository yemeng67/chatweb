document.addEventListener("DOMContentLoaded", function(){
    //帖子点赞
    const likeButton = document.getElementById('post_like_section');
    // const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    async function postLikeButton(is_init=false) {
        try {
            const response = await fetch(`${post_like_api_url}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    // 'X-CSRFToken': csrfToken  // 关键：添加 CSRF Token
                    },
                    body: JSON.stringify({ 'is_init': is_init }),
                })

            const like_data = await response.json();

            likeButton.innerHTML = `
            <button class="like-button" id="post_like_button">
                <span class="like-icon">
                ${like_data.is_liked ? '❤️' : '🤍'}
                ${like_data.is_liked ? '已点赞' : '点赞'}</span>(${like_data.like_count})
            </button>`

            console.log(is_init)

            document.getElementById('post_like_button').addEventListener('click',()=> postLikeButton(false));
        }catch(error) {
            console.log('点赞失败：',error);
            }
    }
    postLikeButton(true);
});