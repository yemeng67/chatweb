// 初始化加载
document.addEventListener('DOMContentLoaded', () => {
    loadPosts(DEFAULT_PARAMS);
    setupCategoryButtons();
});

// 设置分类按钮事件
function setupCategoryButtons() {
    const categoryButtons = document.querySelectorAll('.category-btn');
    categoryButtons.forEach(button => {
        button.addEventListener('click', () => {
            // 移除所有按钮的active类
            categoryButtons.forEach(btn => btn.classList.remove('active'));
            // 给当前按钮添加active类
            button.classList.add('active');

            // 更新选中分类
            DEFAULT_PARAMS.category = button.dataset.categoryId;
            loadPosts(DEFAULT_PARAMS);
        });
    });
}

// 排序事件监听
document.getElementById('sort-select').addEventListener('change', (e) => {
    DEFAULT_PARAMS.sort = e.target.value;
    loadPosts(DEFAULT_PARAMS);
});

// 加载帖子函数
async function loadPosts(params) {
    try {
        const response = await fetch(`${index_api_url}?sort=${params.sort}&category=${params.category}&page=${params.page}`);
        const data = await response.json();

        // 更新帖子列表
        renderPostList(data.posts);

        // 更新分页
        renderPagination(data.pagination);
    } catch (error) {
        console.error('数据加载失败:', error);
    }
}

// 渲染帖子列表
function renderPostList(posts) {
    const container = document.getElementById('post-list-container');

    if (posts.length === 0) {
        container.innerHTML = '<div class="no-posts">没有找到相关帖子</div>';
        return;
    }

    container.innerHTML = posts.map(post => `
        <div class="post-item" data-post-id="${post.id}">
            <h3>
                <a href="/post_detail/${post.id}" class="post-title">${post.title}</a>
            </h3>
            <div class="meta">
                <a class="author" href="/userspace/index/">
                    <img src="${post.author_avatar}" alt="${post.author_name}" class="avatar">
                    ${post.author_name}
                </a>
                <span class="date">${post.created_at}</span>
                <span class="stats">
                    浏览: ${post.views} | 点赞: ${post.likes}
                </span>
            </div>
            <p class="preview">${post.content}</p>
        </div>
    `).join('');

    // 添加点击事件到每个帖子项目
    document.querySelectorAll('.post-item').forEach(item => {
        item.addEventListener('click', function(e) {
            // 如果点击的不是标题链接，则整个项目可点击
            if (!e.target.closest('.post-title')) {
                const postId = this.dataset.postId;

                window.location.href = `/post_detail/${parseInt(postId)}`;
            }
        });
    });
}

// 渲染分页
function renderPagination(pagination) {
    const container = document.getElementById('pagination-container');
    let html = `
        <div class="pagination">
            <button
                ${pagination.current_page <= 1 ? 'disabled' : ''}
                onclick="loadPosts({sort: '${DEFAULT_PARAMS.sort}', category: '${DEFAULT_PARAMS.category}', page: ${pagination.current_page - 1}})"
            >
                上一页
            </button>

            <span>第 ${pagination.current_page} 页 / 共 ${pagination.total_pages} 页</span>

            <button
                ${pagination.current_page >= pagination.total_pages ? 'disabled' : ''}
                onclick="loadPosts({sort: '${DEFAULT_PARAMS.sort}', category: '${DEFAULT_PARAMS.category}', page: ${pagination.current_page + 1}})"
            >
                下一页
            </button>
        </div>
    `;
    container.innerHTML = html;
}