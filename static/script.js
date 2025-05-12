// 音乐播放控制
const playButton = document.querySelector('.control-button.play');
let isPlaying = false;

playButton.addEventListener('click', () => {
    isPlaying = !isPlaying;
    playButton.innerHTML = isPlaying ? '<i class="fas fa-pause"></i>' : '<i class="fas fa-play"></i>';
});

// 喜欢按钮
const likeButton = document.querySelector('.like-button');
likeButton.addEventListener('click', () => {
    likeButton.classList.toggle('active');
});

// 为所有音乐卡片添加播放覆盖层
document.querySelectorAll('.music-card').forEach(card => {
    const overlay = document.createElement('div');
    overlay.className = 'play-overlay';
    overlay.innerHTML = '<div class="play-button"><i class="fas fa-play"></i></div>';
    
    const imgContainer = card.querySelector('img').parentElement;
    imgContainer.style.position = 'relative';
    imgContainer.appendChild(overlay);

    card.addEventListener('click', () => {
        playButton.innerHTML = '<i class="fas fa-pause"></i>';
        isPlaying = true;
    });
});

// AI卡片点击效果
document.querySelectorAll('.ai-card').forEach(card => {
    card.addEventListener('click', () => {
        playButton.innerHTML = '<i class="fas fa-pause"></i>';
        isPlaying = true;
    });
});

// 模拟DeepSeek API调用
const simulateDeepSeekAPI = async () => {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve({
                analysis: {
                    mood: ['轻松愉悦', '充满活力', '浪漫', '沉思', '梦幻', '激情'],
                    genres: ['流行', '电子', '爵士', '摇滚', '民谣', '古典', '嘻哈', 'R&B'],
                    tempo: '中速',
                    energy: '高',
                    danceability: '中高',
                    valence: '积极',
                    acousticness: '低',
                    instrumentalness: '中',
                    liveness: '低',
                    speechiness: '低',
                    // 新增特征
                    key: 'C大调',
                    mode: '大调',
                    timeSignature: '4/4拍',
                    loudness: '-6.5dB',
                    popularity: '85%',
                    duration: '3分45秒',
                    releaseYear: '2024',
                    bpm: 128,
                    // 新增高级特征
                    harmonicComplexity: '中等',
                    rhythmicStability: '高',
                    timbre: '明亮',
                    dynamicRange: '宽',
                    arrangement: '丰富',
                    productionQuality: '专业级'
                },
                recommendations: [
                    {
                        title: '午后爵士',
                        artist: 'Jazz Ensemble',
                        matchScore: 98,
                        reason: '根据您对轻音乐的偏好推荐',
                        features: {
                            tempo: 120,
                            energy: 0.6,
                            danceability: 0.7,
                            valence: 0.8,
                            acousticness: 0.8,
                            instrumentalness: 0.7,
                            liveness: 0.2,
                            speechiness: 0.1,
                            key: 'C',
                            mode: 'major',
                            timeSignature: 4,
                            loudness: -6.5,
                            popularity: 85,
                            duration: 225,
                            releaseYear: 2024,
                            bpm: 120,
                            harmonicComplexity: 0.7,
                            rhythmicStability: 0.9,
                            timbre: 'warm',
                            dynamicRange: 0.8,
                            arrangement: 'rich',
                            productionQuality: 'professional'
                        }
                    },
                    {
                        title: '电子音乐精选',
                        artist: 'EDM Collective',
                        matchScore: 95,
                        reason: '符合您的节奏偏好',
                        features: {
                            tempo: 128,
                            energy: 0.9,
                            danceability: 0.8,
                            valence: 0.7
                        }
                    },
                    {
                        title: '流行音乐合集',
                        artist: 'Pop Stars',
                        matchScore: 92,
                        reason: '基于您最近的收听记录',
                        features: {
                            tempo: 110,
                            energy: 0.7,
                            danceability: 0.8,
                            valence: 0.9
                        }
                    },
                    {
                        title: '独立民谣',
                        artist: 'Folk Artists',
                        matchScore: 90,
                        reason: '匹配您的音乐风格',
                        features: {
                            tempo: 90,
                            energy: 0.5,
                            danceability: 0.6,
                            valence: 0.7
                        }
                    }
                ]
            });
        }, 2000);
    });
};

// 添加音乐波形动画
const createWaveAnimation = (container) => {
    const waveContainer = document.createElement('div');
    waveContainer.className = 'wave-container';
    
    for (let i = 0; i < 20; i++) {
        const bar = document.createElement('div');
        bar.className = 'wave-bar';
        bar.style.animationDelay = `${i * 0.1}s`;
        waveContainer.appendChild(bar);
    }
    
    container.appendChild(waveContainer);
};

// 添加3D卡片翻转效果
const addCardFlipEffect = (card) => {
    card.addEventListener('click', () => {
        card.classList.toggle('flipped');
    });
};

// 添加进度条动画
const animateProgressBar = (progressBar, duration) => {
    let start = null;
    const animate = (timestamp) => {
        if (!start) start = timestamp;
        const progress = timestamp - start;
        const percentage = Math.min(progress / duration, 1);
        progressBar.style.width = `${percentage * 100}%`;
        
        if (percentage < 1) {
            requestAnimationFrame(animate);
        }
    };
    requestAnimationFrame(animate);
};

// 添加音乐可视化效果
const createMusicVisualizer = (container) => {
    const canvas = document.createElement('canvas');
    canvas.className = 'visualizer-canvas';
    container.appendChild(canvas);
    
    const ctx = canvas.getContext('2d');
    const width = canvas.width = container.offsetWidth;
    const height = canvas.height = container.offsetHeight;
    
    const draw = () => {
        ctx.clearRect(0, 0, width, height);
        
        // 绘制波形
        ctx.beginPath();
        ctx.moveTo(0, height / 2);
        
        for (let i = 0; i < width; i++) {
            const y = height / 2 + Math.sin(i * 0.1 + Date.now() * 0.005) * 50;
            ctx.lineTo(i, y);
        }
        
        ctx.strokeStyle = '#ff5500';
        ctx.lineWidth = 2;
        ctx.stroke();
        
        requestAnimationFrame(draw);
    };
    
    draw();
};

// 修改AI分析动画
const startAnalysis = async () => {
    const aiAnalyzing = document.querySelector('.ai-analyzing');
    const steps = document.querySelectorAll('.analysis-step');
    const recommendationGrid = document.querySelector('.recommendation-grid');
    
    aiAnalyzing.classList.add('active');
    
    // 添加波形动画
    createWaveAnimation(aiAnalyzing.querySelector('.analysis-content'));
    
    // 逐步显示分析步骤
    steps.forEach((step, index) => {
        setTimeout(() => {
            step.classList.add('active');
            // 添加打字机效果
            const text = step.textContent;
            step.textContent = '';
            let i = 0;
            const typeWriter = () => {
                if (i < text.length) {
                    step.textContent += text.charAt(i);
                    i++;
                    setTimeout(typeWriter, 50);
                }
            };
            typeWriter();
        }, (index + 1) * 1000);
    });

    // 模拟API调用
    const deepSeekData = await simulateDeepSeekAPI();
    
    // 完成分析后的操作
    setTimeout(() => {
        aiAnalyzing.classList.remove('active');
        recommendationGrid.classList.add('visible');
        showAnalysisResults(deepSeekData);
        
        // 为所有卡片添加翻转效果
        document.querySelectorAll('.ai-card').forEach(addCardFlipEffect);
        
        // 为进度条添加动画
        const progressBar = document.querySelector('.progress');
        animateProgressBar(progressBar, 3000);
        
        // 为播放器添加可视化效果
        const playerBar = document.querySelector('.player-bar');
        createMusicVisualizer(playerBar);
    }, 5000);
};

// 显示分析结果
const showAnalysisResults = (data) => {
    const analysisSection = document.querySelector('.ai-section');
    
    // 更新音乐风格标签
    const moodTags = document.querySelector('.analysis-card:first-child .mood-tag');
    moodTags.innerHTML = data.analysis.genres.map(genre => 
        `<div class="mood-tag">${genre}</div>`
    ).join('');

    // 更新情绪分析
    const moodAnalysis = document.querySelector('.analysis-card:last-child .mood-tag');
    moodAnalysis.innerHTML = data.analysis.mood.map(mood => 
        `<div class="mood-tag">${mood}</div>`
    ).join('');

    // 创建详细分析结果
    const resultHtml = `
        <div class="analysis-result">
            <h3>您的音乐品味分析</h3>
            <div class="genre-chart">
                ${data.analysis.genres.map((genre, index) => `
                    <div class="genre-bar" 
                         data-genre="${genre}" 
                         data-percentage="${(100 - index * 10)}%"
                         style="height: 0">
                    </div>
                `).join('')}
            </div>
            <div class="detailed-analysis">
                <h4>详细分析</h4>
                <div class="analysis-grid">
                    <div class="analysis-item">
                        <span class="analysis-label">节奏</span>
                        <span class="analysis-value">${data.analysis.tempo} (${data.analysis.bpm} BPM)</span>
                    </div>
                    <div class="analysis-item">
                        <span class="analysis-label">能量</span>
                        <span class="analysis-value">${data.analysis.energy}</span>
                    </div>
                    <div class="analysis-item">
                        <span class="analysis-label">可舞性</span>
                        <span class="analysis-value">${data.analysis.danceability}</span>
                    </div>
                    <div class="analysis-item">
                        <span class="analysis-label">情绪</span>
                        <span class="analysis-value">${data.analysis.valence}</span>
                    </div>
                    <div class="analysis-item">
                        <span class="analysis-label">调性</span>
                        <span class="analysis-value">${data.analysis.key} (${data.analysis.mode})</span>
                    </div>
                    <div class="analysis-item">
                        <span class="analysis-label">节拍</span>
                        <span class="analysis-value">${data.analysis.timeSignature}</span>
                    </div>
                    <div class="analysis-item">
                        <span class="analysis-label">响度</span>
                        <span class="analysis-value">${data.analysis.loudness}</span>
                    </div>
                    <div class="analysis-item">
                        <span class="analysis-label">流行度</span>
                        <span class="analysis-value">${data.analysis.popularity}</span>
                    </div>
                </div>
                <div class="advanced-analysis">
                    <h4>高级特征</h4>
                    <div class="analysis-grid">
                        <div class="analysis-item">
                            <span class="analysis-label">和声复杂度</span>
                            <span class="analysis-value">${data.analysis.harmonicComplexity}</span>
                        </div>
                        <div class="analysis-item">
                            <span class="analysis-label">节奏稳定性</span>
                            <span class="analysis-value">${data.analysis.rhythmicStability}</span>
                        </div>
                        <div class="analysis-item">
                            <span class="analysis-label">音色</span>
                            <span class="analysis-value">${data.analysis.timbre}</span>
                        </div>
                        <div class="analysis-item">
                            <span class="analysis-label">动态范围</span>
                            <span class="analysis-value">${data.analysis.dynamicRange}</span>
                        </div>
                        <div class="analysis-item">
                            <span class="analysis-label">编曲</span>
                            <span class="analysis-value">${data.analysis.arrangement}</span>
                        </div>
                        <div class="analysis-item">
                            <span class="analysis-label">制作质量</span>
                            <span class="analysis-value">${data.analysis.productionQuality}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    analysisSection.insertAdjacentHTML('beforeend', resultHtml);
    
    // 延迟显示图表动画
    setTimeout(() => {
        const result = document.querySelector('.analysis-result');
        result.classList.add('visible');
        
        // 添加新的动画效果
        const bars = document.querySelectorAll('.genre-bar');
        bars.forEach((bar, index) => {
            const heights = ['180px', '160px', '140px', '120px', '100px', '80px', '60px', '40px'];
            setTimeout(() => {
                bar.style.height = heights[index];
                bar.style.animation = 'barGrow 1s ease-out forwards';
            }, index * 200);
        });

        // 添加分析项的动画
        const analysisItems = document.querySelectorAll('.analysis-item');
        analysisItems.forEach((item, index) => {
            setTimeout(() => {
                item.style.animation = 'fadeInUp 0.5s ease-out forwards';
                item.style.opacity = '0';
                item.style.transform = 'translateY(20px)';
            }, index * 100);
        });
    }, 500);
};

// 绑定开始分析按钮
const analyzeButton = document.querySelector('.create-button');
analyzeButton.textContent = '开始AI分析';
analyzeButton.addEventListener('click', startAnalysis);

// 添加鼠标跟随效果
const addMouseFollowEffect = () => {
    const cursor = document.createElement('div');
    cursor.className = 'custom-cursor';
    document.body.appendChild(cursor);
    
    document.addEventListener('mousemove', (e) => {
        cursor.style.left = e.clientX + 'px';
        cursor.style.top = e.clientY + 'px';
    });
    
    document.addEventListener('mousedown', () => {
        cursor.classList.add('click');
    });
    
    document.addEventListener('mouseup', () => {
        cursor.classList.remove('click');
    });
};

// 初始化页面
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        document.querySelector('.recommendation-grid').classList.add('visible');
    }, 500);
    
    // 添加鼠标跟随效果
    addMouseFollowEffect();
    
    // 为所有音乐卡片添加悬停效果
    document.querySelectorAll('.music-card').forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-10px) scale(1.02)';
            card.style.boxShadow = '0 10px 20px rgba(0, 0, 0, 0.3)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0) scale(1)';
            card.style.boxShadow = 'none';
        });
    });
});

// 模拟搜索结果数据
const mockSearchResults = [
    {
        title: '午后爵士',
        artist: 'Jazz Ensemble',
        type: '歌曲',
        image: 'https://picsum.photos/200/200?random=1'
    },
    {
        title: '电子音乐精选',
        artist: 'EDM Collective',
        type: '专辑',
        image: 'https://picsum.photos/200/200?random=2'
    },
    {
        title: '流行音乐合集',
        artist: 'Pop Stars',
        type: '歌单',
        image: 'https://picsum.photos/200/200?random=3'
    },
    {
        title: '独立民谣',
        artist: 'Folk Artists',
        type: '歌手',
        image: 'https://picsum.photos/200/200?random=4'
    }
];

// 搜索功能
const searchInput = document.querySelector('.search-input');
const searchContainer = document.querySelector('.search-container');
let searchTimeout;

// 创建搜索结果容器
const searchResults = document.createElement('div');
searchResults.className = 'search-results';
searchContainer.appendChild(searchResults);

// 模拟搜索API
const simulateSearch = async (query) => {
    return new Promise((resolve) => {
        setTimeout(() => {
            if (!query) {
                resolve([]);
            } else {
                const results = mockSearchResults.filter(item => 
                    item.title.toLowerCase().includes(query.toLowerCase()) ||
                    item.artist.toLowerCase().includes(query.toLowerCase())
                );
                resolve(results);
            }
        }, 500);
    });
};

// 显示搜索结果
const showSearchResults = (results) => {
    if (results.length === 0) {
        searchResults.innerHTML = '<div class="no-results">没有找到相关结果</div>';
    } else {
        searchResults.innerHTML = results.map(result => `
            <div class="search-result-item">
                <img src="${result.image}" alt="${result.title}">
                <div class="search-result-info">
                    <div class="search-result-title">${result.title}</div>
                    <div class="search-result-artist">${result.artist}</div>
                </div>
                <span class="search-result-type">${result.type}</span>
            </div>
        `).join('');
    }
    searchResults.classList.add('visible');
};

// 显示加载状态
const showLoading = () => {
    searchResults.innerHTML = '<div class="search-loading"></div>';
    searchResults.classList.add('visible');
};

// 处理搜索输入
searchInput.addEventListener('input', (e) => {
    const query = e.target.value.trim();
    
    // 清除之前的定时器
    clearTimeout(searchTimeout);
    
    if (query) {
        showLoading();
        
        // 设置新的定时器
        searchTimeout = setTimeout(async () => {
            const results = await simulateSearch(query);
            showSearchResults(results);
        }, 500);
    } else {
        searchResults.classList.remove('visible');
    }
});

// 点击搜索结果项
searchResults.addEventListener('click', (e) => {
    const resultItem = e.target.closest('.search-result-item');
    if (resultItem) {
        const title = resultItem.querySelector('.search-result-title').textContent;
        alert(`你点击了: ${title}`);
        searchResults.classList.remove('visible');
        searchInput.value = '';
    }
});

// 点击其他地方关闭搜索结果
document.addEventListener('click', (e) => {
    if (!searchContainer.contains(e.target)) {
        searchResults.classList.remove('visible');
    }
});

// 搜索框获得焦点时显示最近搜索
searchInput.addEventListener('focus', () => {
    if (searchInput.value.trim()) {
        showLoading();
        setTimeout(() => {
            showSearchResults(mockSearchResults);
        }, 500);
    }
});

// AI 聊天对话框功能
const discoveryLink = document.getElementById('discovery-link');
const aiChatDialog = document.querySelector('.ai-chat-dialog');
const closeButton = document.querySelector('.close-button');
const chatInput = document.querySelector('.ai-chat-input input');
const sendButton = document.querySelector('.send-button');
const chatMessages = document.querySelector('.ai-chat-messages');

// 显示 AI 对话框
discoveryLink.addEventListener('click', (e) => {
    e.preventDefault();
    aiChatDialog.classList.add('visible');
});

// 关闭 AI 对话框
closeButton.addEventListener('click', () => {
    aiChatDialog.classList.remove('visible');
});

// 点击对话框外部关闭
document.addEventListener('click', (e) => {
    if (e.target === aiChatDialog) {
        aiChatDialog.classList.remove('visible');
    }
});

// 预设对话和关键词回复
const presetResponses = {
    '轻松': {
        message: '好的！根据你的听歌历史，我为你推荐以下轻松的音乐：',
        recommendations: [
            {
                title: '稻香',
                artist: '周杰伦',
                image: 'https://picsum.photos/200/200?random=8'
            },
            {
                title: '晴天',
                artist: '周杰伦',
                image: 'https://picsum.photos/200/200?random=9'
            },
            {
                title: '小幸运',
                artist: '田馥甄',
                image: 'https://picsum.photos/200/200?random=10'
            }
        ]
    },
    '伤感': {
        message: '我理解你现在的心情，这些歌曲或许能陪伴你：',
        recommendations: [
            {
                title: '后来',
                artist: '刘若英',
                image: 'https://picsum.photos/200/200?random=11'
            },
            {
                title: '说散就散',
                artist: 'JC',
                image: 'https://picsum.photos/200/200?random=12'
            },
            {
                title: '体面',
                artist: '于文文',
                image: 'https://picsum.photos/200/200?random=13'
            }
        ]
    },
    '励志': {
        message: '这些充满力量的歌曲，希望能给你带来动力：',
        recommendations: [
            {
                title: '倔强',
                artist: '五月天',
                image: 'https://picsum.photos/200/200?random=14'
            },
            {
                title: '追梦赤子心',
                artist: 'GALA',
                image: 'https://picsum.photos/200/200?random=15'
            },
            {
                title: '海阔天空',
                artist: 'Beyond',
                image: 'https://picsum.photos/200/200?random=16'
            }
        ]
    },
    '流行': {
        message: '最近这些热门歌曲很受欢迎：',
        recommendations: [
            {
                title: '起风了',
                artist: '买辣椒也用券',
                image: 'https://picsum.photos/200/200?random=17'
            },
            {
                title: '光年之外',
                artist: '邓紫棋',
                image: 'https://picsum.photos/200/200?random=18'
            },
            {
                title: '年少有为',
                artist: '李荣浩',
                image: 'https://picsum.photos/200/200?random=19'
            }
        ]
    },
    '民谣': {
        message: '这些民谣歌曲很有故事感：',
        recommendations: [
            {
                title: '成都',
                artist: '赵雷',
                image: 'https://picsum.photos/200/200?random=20'
            },
            {
                title: '南山南',
                artist: '马頔',
                image: 'https://picsum.photos/200/200?random=21'
            },
            {
                title: '理想三旬',
                artist: '陈鸿宇',
                image: 'https://picsum.photos/200/200?random=22'
            }
        ]
    },
    '摇滚': {
        message: '这些摇滚歌曲充满力量：',
        recommendations: [
            {
                title: '无地自容',
                artist: '黑豹乐队',
                image: 'https://picsum.photos/200/200?random=23'
            },
            {
                title: '光辉岁月',
                artist: 'Beyond',
                image: 'https://picsum.photos/200/200?random=24'
            },
            {
                title: '梦回唐朝',
                artist: '唐朝乐队',
                image: 'https://picsum.photos/200/200?random=25'
            }
        ]
    },
    '默认': {
        message: '你好！我是你的音乐助手，我可以帮你：',
        recommendations: [
            {
                title: '推荐新音乐',
                artist: '根据你的喜好',
                image: 'https://picsum.photos/200/200?random=26'
            },
            {
                title: '分析音乐风格',
                artist: '了解你的品味',
                image: 'https://picsum.photos/200/200?random=27'
            },
            {
                title: '创建个性化歌单',
                artist: '专属你的音乐',
                image: 'https://picsum.photos/200/200?random=28'
            }
        ]
    }
};

// 修改发送消息函数
function sendMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';
    messageDiv.innerHTML = `
        <div class="message-content">${message}</div>
    `;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    // 查找匹配的关键词
    let response = presetResponses['默认'];
    for (const keyword in presetResponses) {
        if (message.includes(keyword)) {
            response = presetResponses[keyword];
            break;
        }
    }

    // 模拟 AI 回复
    setTimeout(() => {
        const aiResponse = document.createElement('div');
        aiResponse.className = 'message ai-message';
        aiResponse.innerHTML = `
            <div class="message-content">
                ${response.message}
                <div class="recommendation-cards">
                    ${response.recommendations.map(rec => `
                        <div class="recommendation-card">
                            <img src="${rec.image}" alt="${rec.title}">
                            <div class="card-info">
                                <h4>${rec.title}</h4>
                                <p>${rec.artist}</p>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
        chatMessages.appendChild(aiResponse);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 1000);
}

// 处理发送按钮点击
sendButton.addEventListener('click', () => {
    const message = chatInput.value.trim();
    if (message) {
        sendMessage(message);
        chatInput.value = '';
    }
});

// 处理输入框回车
chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        const message = chatInput.value.trim();
        if (message) {
            sendMessage(message);
            chatInput.value = '';
        }
    }
}); 