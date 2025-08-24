// 初始化事件监听
document.addEventListener('DOMContentLoaded', () => {
    setupSearchForm();
    // 设置排序下拉框的初始值
    const sortSelect = document.getElementById('sort-select');
    if (sortSelect) {
        sortSelect.value = currentParams.sort;
    }

    // 只有当有搜索关键词时才加载结果
    if (currentParams.q) {
        loadResults(currentParams);
    } else {
        // 如果没有搜索关键词，隐藏排序控件
        toggleSortControls(false);
    }
});

// 监听返回
document.getElementById('backButton').addEventListener('click', function() {
    // window.history.back();
    window.location.href = "/index"; // 回退到首页
});

// 监听排序
document.getElementById('sort-select').addEventListener('change', (e) => {
    currentParams.sort = e.target.value;
    currentParams.page = 1; // 重置到第一页
    loadResults(currentParams);
});

// 表单提交处理
function setupSearchForm() {
    const form = document.getElementById('searchForm');
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const keyword = document.getElementById('searchInput').value.trim();

        if (!keyword) {
            alert('请输入搜索内容');
            return;
        }

        if (keyword.length > 10) {
            alert('关键词长度不能超过10个字符');
            return;
        }

        currentParams.q = keyword;
        currentParams.page = 1;
        loadResults(currentParams);
    });
}

// 加载搜索结果
async function loadResults(params) {
    try {
        const response = await fetch(`${API_URL}?q=${encodeURIComponent(params.q)}&sort=${params.sort}&page=${params.page}`);
        const data = await response.json();

        // 更新帖子
        renderPosts(data.posts);

        // 渲染分页
        renderPagination(data.pagination);

        // 显示排序控件（只有在有搜索词时才显示）
        toggleSortControls(params.q && data.posts.length > 0);

        // 更新浏览器历史记录
        const newUrl = `?q=${encodeURIComponent(params.q)}&sort=${params.sort}&page=${params.page}`;
        window.history.pushState(params, '', newUrl);
    } catch (error) {
        console.error('加载失败:', error);
    }
}

// 渲染帖子列表
function renderPosts(posts) {
    const container = document.getElementById('postList');

    if (posts.length === 0) {
        container.innerHTML = `
            <div class="no-results alert alert-warning mt-4">
                抱歉，没有您想要的结果
            </div>
        `;
        return;
    }

    container.innerHTML = posts.map(post => `
        <div class="post-item" data-post-id="${post.id}">
            <h3>
                <a href="/post_detail/${post.id}" class="post-title">${post.title}</a>
            </h3>
            <div class="meta">
                <a class="author" href="/userspace/index/">
                    <img src="${post.author_avatar || '/media/default/avatar.jpg'}" onerror="this.src='/media/default/avatar.jpg'" alt="${post.author}" class="avatar">
                    ${post.author}
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

// 显示/隐藏排序控件
function toggleSortControls(hasResults) {
    const sortContainer = document.querySelector('.sort-container');
    if (sortContainer) {
        sortContainer.classList.toggle('d-none', !hasResults);
    }
}

// 渲染分页
function renderPagination(pagination) {
    const container = document.getElementById('pagination-container');
    if (!container) return;

    if (pagination.total_pages <= 1) {
        container.innerHTML = '';
        return;
    }

    let html = `
        <div class="pagination">
            <button
                ${pagination.current_page <= 1 ? 'disabled' : ''}
                onclick="loadResults({q: currentParams.q, sort: currentParams.sort, page: ${pagination.current_page - 1}})"
            >
                上一页
            </button>
            
            <span>第 ${pagination.current_page} 页 / 共 ${pagination.total_pages} 页</span>
            
            <button
                ${pagination.current_page >= pagination.total_pages ? 'disabled' : ''}
                onclick="loadResults({q: currentParams.q, sort: currentParams.sort, page: ${pagination.current_page + 1}})"
            >
                下一页
            </button>
        </div>
    `;
    container.innerHTML = html;
}
