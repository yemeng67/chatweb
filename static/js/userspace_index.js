document.addEventListener('DOMContentLoaded', function () {
    const navButtons = document.querySelectorAll('.nav-btn');
    const contents = document.querySelectorAll('.content');

    navButtons.forEach(button => {
        button.addEventListener('click', function () {
            const targetId = this.dataset.target;

            // 重置所有按钮和内容的层级
            navButtons.forEach(btn => btn.classList.remove('active'));
            contents.forEach(content => {
                content.classList.remove('active');
                content.style.zIndex = 0; // 强制重置 z-index
                content.style.order = 0;   // 重置 CSS Grid/Flex 顺序
                content.style.height = '0'; // 强制收缩

            });

            // 将激活项移动到 DOM 最后（确保覆盖其他内容）
            const activeContent = document.getElementById(targetId);
            activeContent.parentNode.appendChild(activeContent);

            // 设置当前激活项
            this.classList.add('active');
            activeContent.classList.add('active');
            activeContent.style.zIndex = 1;

            // 动态计算高度
            requestAnimationFrame(() => {
              activeContent.style.height = activeContent.scrollHeight + 'px';
              activeContent.style.overflow = 'auto'; // 启用滚动
            });
        });
    });
});

// 头像上传功能
document.querySelector('.avatar').addEventListener('click', function(e) {
    e.stopPropagation();
    document.getElementById('avatarModal').style.display = 'flex';//显示更换界面
});

function submitAvatar() {
    const fileInput = document.getElementById('avatarInput');
    const formData = new FormData();//虽然表单为空，但是会有相应的格式，如请求头之类的
    formData.append('avatar', fileInput.files[0]);//添加数据，命名为avatar，fileInput.files[0]便是input中上传的文件
    formData.append('csrfmiddlewaretoken', '{{ csrf_token }}'); //手动添加csrf_token

    fetch(`${upload_avatar_api_url}`, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // 成功后更新界面
            // const avatar = document.querySelector('.avatar');
            // avatar.src = URL.createObjectURL(avatarInput.files[0]);//更新头像
            // closeModal('avatarModal');  //关闭界面
            alert('头像更换成功！');
            window.location.href = data.redirect_url;
        }
        else {
            alert('上传失败: ' + data.message);
        }
    });
}

//更新头像预览
document.querySelector('#avatarInput').addEventListener('change', function() {
    const avatarInput = document.getElementById('avatarInput');
    const preview = document.getElementById('previewAvatar');
    preview.src = URL.createObjectURL(avatarInput.files[0]);  //获取临时的文件地址，然后赋值给属性src
});


// 简介编辑功能
document.querySelector('.user-info p').addEventListener('click', function() {
        document.getElementById('bioModal').style.display = 'flex';
});

function submitBio() {
    const bioText = document.getElementById('bioInput').value;
    const csrftoken = '{{ csrf_token }}';

    fetch(`${update_bio_api_url}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken
        },
        body: `bio=${encodeURIComponent(bioText)}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // 更新简介显示
            document.querySelector('.user-info p').textContent = bioText || '暂无简介';
            closeModal('bioModal');
        }
        else {
            alert('更新失败: ' + data.message);
        }
    });
}

// 通用关闭函数
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.style.display = 'none';  //关闭更换界面
    // 重置表单
    if (modalId === 'avatarModal') {
        document.getElementById('avatarInput').value = '';
        document.getElementById('previewAvatar').src = `${avatar_url}` ;
    }
}