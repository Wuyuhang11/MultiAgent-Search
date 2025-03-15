new Typed('#typewriter', { strings: ['MultiAgent', '一款基于多智能体的城市图像识别与位置推理系统'], typeSpeed: 60, loop: true, backSpeed: 10, backDelay: 1500 });
if (/Mobi|Android|iPhone/i.test(navigator.userAgent)) {
    alert('检测到当前设备可能为移动端，建议使用电脑访问！');
    window.close();
}

const video = document.getElementById('video');
const videoBtn = document.getElementById('videoBtn');
const videoWrapper = document.getElementById('videoWrapper')
videoBtn.addEventListener('click', function (event) {
    event.preventDefault();
    videoWrapper.style.display = 'block';
});

videoWrapper.addEventListener('click', function (event) {
    if (event.target === this) {
        videoWrapper.style.display = 'none';
        video.pause();
    }
});