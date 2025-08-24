document.addEventListener("DOMContentLoaded", function() {
    //等待页面加载完成
    //下面的window是将函数声明为全局函数，原因如下：
            // 当 loadComments 函数被包裹在 DOMContentLoaded 事件监听器的回调函数中时，该函数会被限制在局部作用域内。这意味着：
            // 在外部 JS 文件中，loadComments 仅在该回调函数内部可见
            // HTML 中通过 onclick 属性直接调用的方式（如 onclick="loadComments(2)"）无法找到该函数
            // 分页按钮的事件绑定会失效，表现为点击无响应
    window.loadComments = async function(page = 1) {
        const response = await fetch(`${comment_api_url}?comment_page=${page}`);
        const data = await response.json();   //将得到的回应转换为json

        //更新评论列表
        const comments_container = document.querySelector('#post-comments-content');
        comments_container.innerHTML = data.comments.map(comment =>
            `<div class="comment">
                <div class="comment-user">
                    <img src="/media/${comment.user__avatar}" class="comment-user-avatar">
                    <span>${comment.user__username}:</span>
                </div>
                ${comment.content}
            </div>`
        ).join('');
        /*map循环遍历，返回的是数组（如["<div>...</div>", "<div>...</div>"]），
        直接赋值给innerHTML会显示逗号。join('')去除逗号，合并为连续HTML。*/

        //更新分页控件
        const commentsContainer = document.querySelector('#post-comments-pagination');
        commentsContainer.innerHTML = `
                    <button onclick="loadComments(1)">首页</button>
                    ${data.has_previous ? `<button onclick="loadComments(${Number(data.comment_page) - 1})"><-前一页</button>` : ''}
                    ${data.has_previous ? `<button onclick="loadComments(${Number(data.comment_page) - 1})">${data.comment_page - 1}</button>` : ''}
                    <span>${data.comment_page}</span>
                    ${data.has_next ? `<button onclick="loadComments(${Number(data.comment_page) + 1})">${Number(data.comment_page) + 1}</button>` : ''}
                    ${data.has_next ? `<button onclick="loadComments(${Number(data.comment_page) + 1})">下一页-></button>` : ''}
                    <button onclick="loadComments(${data.total_pages})">末页</button>
                    <span>总页数:${data.total_pages}</span>
                    `;
    }

    //初始化加载第一页
    loadComments();
})

document.addEventListener("DOMContentLoaded", function() {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    document.querySelector("#add_comment").addEventListener("submit", async (event) => {
        event.preventDefault();//阻止表单的提交的行为
        const formData = new FormData(event.target);//event.target获取当前对象，FormData自动处理获取表单
        try {
            const response = await fetch(`${add_comment_api_url}`, {
                method: 'POST',
                body: formData,// 直接发送FormData对象
                headers: {
                    'X-CSRFToken': csrftoken  // 添加CSRF令牌头
                }
                // 注意：无需手动设置Content-Type，FormData会自动处理
            });
            if (!response.ok) throw new Error('请求失败');
            const result = await response.json();
            loadComments();
            alert(result.message);//成功
            event.target.reset(); //清空输入框中的内容
        } catch (error) {
            alert(error.message);//失败
        }
    })
})