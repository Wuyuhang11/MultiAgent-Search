const img = document.getElementById('imageDisplay')
const png = document.getElementById('png')
const form = document.getElementById('form')
const loading = document.getElementById('loading')
const ans = document.getElementById('ans')
const mind = document.getElementById('mind')
const nodesParent = document.getElementById('nodes')
const nodes = nodesParent.children
const nodeDesc = document.getElementById('nodeDesc')
png.addEventListener('change', function (event) {
    var file = event.target.files[0];
    var reader = new FileReader();
    reader.onload = function (e) {
        img.src = e.target.result;
    };
    reader.readAsDataURL(file);
});

for (i = 1; i < nodes.length; i++) {
    node = nodes[i]
    node.addEventListener('click', function () {
        for (j = 1; j < nodes.length; j++) {
            nodes[j].className = ''
        }
        this.className = 'active'
        nodeDesc.innerText = this.dataset.desc
    })
}

typed = null
timer = null
form.addEventListener('submit', function (event) {
    event.preventDefault()
    if (png.files.length > 0) {
        clearInterval(timer)
        const file = png.files[0];
        const formData = new FormData();
        formData.append('file', file);
        formData.append('question', '');
        mind.style.display = 'none'
        loading.style.display = 'block'
        img.style.display = 'block'
        if (typed) typed.destroy();
        ans.innerHTML = ''
        nodes[1].click()

        fetch('http://8.138.82.144:8888/upload', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                const main_traits = `
                    <h2 class="title">上传图像的主要特征：</h2>
                    ${marked.parse(data.main_traits)}
                `
                const candidate_big_places = `
                    <h2 class="title">经过外部知识得到的相关地区：</h2>
                    ${data.candidate_big_places.join('<br />')}
                `
                const small_place = `
                    <h2 class="title">候选答案：</h2>
                    ${data.candidate.map(item => '<h3>' + item.small_place + '</h3><div class="traits">' + marked.parse(item.traits) + '</div>').join('<br />')}
                `
                const judge_content = `
                    <h2 class="title">最终判断：</h2>
                    ${marked.parse(data.judge_content)}
                `
                const urls_from_web = `
                    <h2 class="title">参考链接：</h2>
                    ${data.urls_from_web.map(item => {
                    const url = /http[s]?:.*/.exec(item)[0]
                    return '<a target="_blank" href="' + url + '">' + url + '</a>'
                }).join('<br />')}
                `

                const timer = setInterval(() => {
                    if (ans.innerHTML.includes('<h2>最终判断：</h2>')) {
                        return nodes[4].click()
                    } else if (ans.innerHTML.includes('<h2>候选答案：</h2>')) {
                        return nodes[3].click()
                    } else if (ans.innerHTML.includes('<h2>经过外部知识得到的相关地区：</h2>')) {
                        return nodes[2].click()
                    }
                }, 512)
                typed = new Typed('#ans', {
                    strings: [main_traits + candidate_big_places + small_place + judge_content + urls_from_web],
                    typeSpeed: 16,
                    showCursor: false,
                    onStringTyped: () => {
                        clearInterval(timer)
                    }
                });
                loading.style.display = 'none'
                mind.style.display = 'block'
            })
            .catch(error => {
                console.error(error)
                loading.style.display = 'none'
            });
    }
})

if (/Mobi|Android|iPhone/i.test(navigator.userAgent)) {
    alert('检测到当前设备可能为移动端，建议使用电脑访问！');
    window.close();
}