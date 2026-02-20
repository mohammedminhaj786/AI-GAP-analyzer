document.addEventListener('DOMContentLoaded', () => {
    init();
});

async function init() {
    loadRoles();
    setupUploader();
    setupForm();
}

async function loadRoles() {
    try {
        const res = await axios.get('/roles');
        const select = document.getElementById('jobRole');
        res.data.forEach(role => {
            const opt = document.createElement('option');
            opt.value = role;
            opt.textContent = role;
            select.appendChild(opt);
        });
    } catch (err) {
        console.error("Failed to load roles", err);
    }
}

function setupUploader() {
    const dropArea = document.getElementById('dropArea');
    const input = document.getElementById('resumeUpload');
    const fileInfo = document.getElementById('fileInfo');

    dropArea.addEventListener('click', () => input.click());

    input.addEventListener('change', () => {
        if (input.files.length > 0) {
            fileInfo.innerHTML = `
                <p style="color:var(--primary); font-weight:600;">${input.files[0].name}</p>
                <small>File selected successfully</small>
            `;
            dropArea.style.borderColor = "var(--primary)";
            dropArea.style.background = "rgba(99, 102, 241, 0.05)";
        }
    });

    // Drag and drop handlers
    ['dragenter', 'dragover'].forEach(name => {
        dropArea.addEventListener(name, (e) => {
            e.preventDefault();
            dropArea.classList.add('active');
        });
    });

    ['dragleave', 'drop'].forEach(name => {
        dropArea.addEventListener(name, (e) => {
            e.preventDefault();
            dropArea.classList.remove('active');
            if (name === 'drop') {
                input.files = e.dataTransfer.files;
                input.dispatchEvent(new Event('change'));
            }
        });
    });
}

function setupForm() {
    const form = document.getElementById('analysisForm');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // UI Transitions
        document.getElementById('placeholderView').classList.add('hidden');
        document.getElementById('resultsView').classList.add('hidden');
        document.getElementById('loaderView').classList.remove('hidden');

        const btn = document.getElementById('analyzeBtn');
        btn.disabled = true;
        btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> ANALYZING...`;

        const formData = new FormData();
        formData.append('job_role', document.getElementById('jobRole').value);
        formData.append('resume', document.getElementById('resumeUpload').files[0]);

        let githubInput = document.getElementById('githubLink').value;
        if (githubInput) {
            // Extract username from link if it's a full URL
            const username = extractGithubUser(githubInput);
            formData.append('github_username', username);
        }

        try {
            const res = await axios.post('/analyze', formData);
            renderResults(res.data);
        } catch (err) {
            alert("Analysis failed: " + (err.response?.data?.detail || "Connection Error"));
            document.getElementById('loaderView').classList.add('hidden');
            document.getElementById('placeholderView').classList.remove('hidden');
        } finally {
            btn.disabled = false;
            btn.innerHTML = `<i class="fa-solid fa-brain"></i> EVALUATE PROFILE`;
        }
    });
}

function extractGithubUser(input) {
    if (input.includes('github.com/')) {
        const parts = input.split('github.com/');
        return parts[1].split('/')[0].split('?')[0];
    }
    return input; // Assume it's already a username
}

function renderResults(data) {
    document.getElementById('loaderView').classList.add('hidden');
    document.getElementById('resultsView').classList.remove('hidden');

    // 1. Progress Orb
    const score = Math.round(data.readiness_score);
    document.getElementById('readinessVal').textContent = score + '%';
    const circle = document.getElementById('progressCircle');
    const offset = 377 - (377 * score / 100);
    circle.style.strokeDashoffset = offset;

    // 2. Bars
    document.getElementById('resumeScoreText').textContent = Math.round(data.resume_score) + '%';
    document.getElementById('resumeBar').style.width = data.resume_score + '%';
    document.getElementById('githubScoreText').textContent = Math.round(data.github_score) + '%';
    document.getElementById('githubBar').style.width = data.github_score + '%';

    // 3. Tags
    const matchedContainer = document.getElementById('matchedTags');
    matchedContainer.innerHTML = '';
    data.matched_skills.forEach(s => {
        const tag = document.createElement('span');
        tag.className = 'tag matched';
        tag.innerHTML = `<i class="fa-solid fa-check"></i> ${s}`;
        matchedContainer.appendChild(tag);
    });

    const missingContainer = document.getElementById('missingTags');
    missingContainer.innerHTML = '';
    data.missing_skills.forEach(s => {
        const tag = document.createElement('span');
        tag.className = 'tag missing';
        tag.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> ${s}`;
        missingContainer.appendChild(tag);
    });

    // 4. Github
    const ghSection = document.getElementById('ghDataSection');
    if (data.github_data) {
        ghSection.classList.remove('hidden');
        const stats = document.getElementById('githubStats');
        stats.innerHTML = `
            <div class="stat-item"><span class="num">${data.github_data.public_repos}</span><span class="lab">REPOS</span></div>
            <div class="stat-item"><span class="num">${data.github_data.total_stars}</span><span class="lab">STARS</span></div>
            <div class="stat-item"><span class="num">${data.github_data.followers}</span><span class="lab">FOLLOWERS</span></div>
        `;
    } else {
        ghSection.classList.add('hidden');
    }

    // 5. Recommendations
    const road = document.getElementById('roadmapContent');
    road.innerHTML = '';
    data.recommendations.forEach(r => {
        const div = document.createElement('div');
        div.className = 'rec-card';
        div.innerHTML = `
            <div class="rec-icon"><i class="fa-solid fa-arrow-trend-up"></i></div>
            <div class="rec-content"><p>${r}</p></div>
        `;
        road.appendChild(div);
    });

    // 6. Detailed Roadmap (New)
    const detailedRoadmap = document.getElementById('detailedRoadmapView');
    const roadmapContainer = document.getElementById('detailedRoadmapContent');
    roadmapContainer.innerHTML = '';

    if (data.roadmap && data.roadmap.length > 0) {
        detailedRoadmap.classList.remove('hidden');
        data.roadmap.forEach((step, index) => {
            const stepDiv = document.createElement('div');
            stepDiv.className = 'roadmap-step';

            let linksHtml = step.useful_links.map(link =>
                `<a href="${link}" target="_blank" class="link-btn"><i class="fa-solid fa-link"></i> Resource</a>`
            ).join('');

            stepDiv.innerHTML = `
                <div class="roadmap-header">
                    <div class="roadmap-num">${index + 1}</div>
                    <div class="roadmap-skill">${step.skill}</div>
                </div>
                <div class="roadmap-task">
                    <div class="task-item">
                        <i class="fa-solid fa-play"></i>
                        <div class="task-content">
                            <span class="task-label">Where to Start:</span>
                            <span class="task-desc">${step.how_to_start}</span>
                        </div>
                    </div>
                    <div class="task-item">
                        <i class="fa-solid fa-bullseye"></i>
                        <div class="task-content">
                            <span class="task-label">What to Achieve:</span>
                            <span class="task-desc">${step.what_to_achieve}</span>
                        </div>
                    </div>
                </div>
                <div class="roadmap-links">
                    ${linksHtml}
                </div>
            `;
            roadmapContainer.appendChild(stepDiv);
        });
    } else {
        detailedRoadmap.classList.add('hidden');
    }
}
