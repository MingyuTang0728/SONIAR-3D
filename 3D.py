import streamlit as st
import streamlit.components.v1 as components
import base64
import os

# 设置页面配置
st.set_page_config(layout="wide", page_title="SONAIR 3D Entry")

# ================= 核心修改点 =================
# 这里我们直接指向 GitHub Pages 生成的链接
# 这样无论你的 Streamlit 在哪里运行，都能准确跳过去
TARGET_URL = "https://mingyutang0728.github.io/SONIAR-3D/UoN%20Multimodal%20AI%20Platform.html"
LOGO_FILE = "UoN-Nottingham-Blue.png"
# ============================================

def get_image_base64(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

logo_base64 = get_image_base64(LOGO_FILE)
logo_src = f"data:image/png;base64,{logo_base64}" if logo_base64 else ""

html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SONAIR</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        :root {{ --neon: #00fff2; --bg: #000205; }}
        body {{ margin: 0; background: var(--bg); overflow: hidden; user-select: none; font-family: 'Orbitron', sans-serif; }}
        
        /* 保持原有的 CSS 样式 */
        #intro-layer {{
            position: fixed; inset: 0; background: #000; z-index: 10000;
            display: flex; align-items: center; justify-content: center;
            transition: all 1.5s cubic-bezier(0.16, 1, 0.3, 1); pointer-events: none;
        }}
        #intro-text {{
            font-size: 6rem; font-weight: 900; color: #fff; letter-spacing: 0.2em;
            text-shadow: 0 0 50px var(--neon); transition: all 1.5s; white-space: nowrap;
        }}
        body.intro-active #intro-layer {{ background: transparent; }}
        body.intro-active #intro-text {{
            font-size: 1.5rem; transform: translate(calc(-50vw + 160px), calc(-50vh + 50px)); 
            text-shadow: 0 0 10px var(--neon); letter-spacing: 0.1em;
        }}

        #cam-preview {{
            position: absolute; top: 20px; right: 20px; width: 400px; height: 300px;
            border: 1px solid var(--neon); background: rgba(0,0,0,0.9); z-index: 50; 
            opacity: 0; transition: opacity 1s 2s; box-shadow: 0 0 20px rgba(0, 255, 242, 0.1);
        }}
        body.intro-active #cam-preview {{ opacity: 1; }}
        #cam-video {{ width: 100%; height: 100%; object-fit: cover; transform: scaleX(-1); }}

        #uon-holo-logo {{ position: absolute; top: 10px; left: 10px; z-index: 60; opacity: 0; transition: opacity 1s 2s; }}
        body.intro-active #uon-holo-logo {{ opacity: 1; }}
        #uon-img {{ height: 35px; width: auto; filter: drop-shadow(0 0 5px rgba(0, 255, 242, 0.5)); }}

        #hand-cursor {{
            position: fixed; top: 0; left: 0; width: 30px; height: 30px;
            border: 1px solid rgba(0, 255, 242, 0.5); border-radius: 50%;
            transform: translate(-50%, -50%); pointer-events: none; z-index: 9999;
            box-shadow: 0 0 10px var(--neon); display: none;
        }}
        #hand-cursor.zoom-in {{ border: 2px solid var(--neon); width: 60px; height: 60px; }}
        #hand-cursor.zoom-out {{ border: 2px solid #ff3333; width: 10px; height: 10px; }}
        #hand-cursor.hover-uk {{ border-color: #ffffff; width: 40px; height: 40px; }}

        #access-granted {{
            position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
            color: #fff; font-size: 4rem; font-weight: 900; 
            text-shadow: 0 0 50px var(--neon); opacity: 0; z-index: 10001; 
            transition: opacity 0.2s; letter-spacing: 0.2em;
        }}
        body.access-active #access-granted {{ opacity: 1; }}

        #instructions {{
            position: absolute; bottom: 40px; left: 40px; z-index: 50;
            opacity: 0; transition: opacity 1s 2.5s;
        }}
        body.intro-active #instructions {{ opacity: 1; }}
    </style>
</head>
<body>

<div id="intro-layer"><h1 id="intro-text">SONAIR UK</h1></div>
<div id="access-granted">INITIALIZING...</div>
<div id="hand-cursor"></div>

<div id="cam-preview">
    <video id="cam-video" autoplay muted playsinline></video>
    <div id="uon-holo-logo"><img id="uon-img" src="{logo_src}"></div>
    <div class="absolute bottom-0 w-full bg-cyan-900/80 text-[10px] text-center text-cyan-300 font-mono py-1">UoN X UTC</div>
</div>

<div id="instructions" class="px-6 py-5 rounded-tr-2xl border-l-4 border-cyan-400 text-cyan-100 space-y-4" style="background: rgba(0,10,20,0.7); backdrop-filter: blur(10px);">
    <div class="flex items-center gap-4"><div class="text-2xl text-cyan-400 w-8 text-center">✋</div><div><div class="font-bold text-sm">PALM OPEN</div><div class="text-[10px]">Zoom In</div></div></div>
    <div class="flex items-center gap-4"><div class="text-2xl text-pink-400 w-8 text-center">✊</div><div><div class="font-bold text-sm">FIST PINCH</div><div class="text-[10px]">Zoom Out</div></div></div>
    <div class="flex items-center gap-4"><div class="text-2xl text-white w-8 text-center">👌</div><div><div class="font-bold text-sm">TARGET UK</div><div class="text-[10px]">Hold 5s to Warp</div></div></div>
</div>

<div id="root"></div>

<script type="importmap">
{{ "imports": {{ 
    "react": "https://esm.sh/react@18.2.0", 
    "react-dom/client": "https://esm.sh/react-dom@18.2.0/client", 
    "three": "https://esm.sh/three@0.150.1", 
    "@react-three/fiber": "https://esm.sh/@react-three/fiber@8.13.0?deps=three@0.150.1,react@18.2.0", 
    "@react-three/drei": "https://esm.sh/@react-three/drei@9.70.0?deps=three@0.150.1,react@18.2.0,@react-three/fiber@8.13.0", 
    "htm": "https://esm.sh/htm@3.1.1", 
    "@mediapipe/tasks-vision": "https://esm.sh/@mediapipe/tasks-vision@0.10.8" 
}} }}
</script>

<script type="module">
    import React, {{ useState, useEffect, useRef, useMemo, Suspense }} from 'react';
    import {{ createRoot }} from 'react-dom/client';
    import htm from 'htm';
    import * as THREE from 'three';
    import {{ Canvas, useFrame, useLoader, useThree }} from '@react-three/fiber';
    import {{ Html, Stars, OrbitControls }} from '@react-three/drei';
    import {{ FilesetResolver, HandLandmarker }} from '@mediapipe/tasks-vision';

    const html = htm.bind(React.createElement);
    
    // --- 核心修改：使用 Python 传入的真实 URL ---
    const TARGET_URL = "{TARGET_URL}"; 

    // UK Marker 组件 (简化版)
    const UKMarker = ({{ isHovered, pinchProgress }}) => {{
        // ... (保持之前的 UKMarker 逻辑不变，为了节省长度我这里省略了细节，请确保之前的 UKMarker 代码还在) ...
        const progressColor = pinchProgress > 0.8 ? "#ff0055" : "#00fff2";
        const radius = 28; const circumference = 2 * Math.PI * radius; const offset = circumference - (pinchProgress * circumference);
        return html`
        <group>
             <${{Html}} position=${{[0, 0.6, 0]}} center distanceFactor=${{8}} style=${{{{pointerEvents:'none'}}}}>
                <div className="flex flex-col items-center justify-center filter drop-shadow-[0_0_10px_rgba(0,255,242,0.5)]">
                    <div className="relative w-20 h-20 mb-2">
                        <svg width="80" height="80" viewBox="0 0 80 80" style=${{{{transform: 'rotate(-90deg)'}}}}>
                            <circle cx="40" cy="40" r="28" fill="none" stroke="rgba(0, 170, 255, 0.2)" strokeWidth="2" />
                            <circle cx="40" cy="40" r="28" fill="none" stroke=${{progressColor}} strokeWidth="4" strokeLinecap="round" strokeDasharray=${{circumference}} strokeDashoffset=${{offset}} />
                        </svg>
                        <div className="absolute inset-0 flex items-center justify-center">
                            ${{pinchProgress > 0 && html`<div className="text-white font-bold text-xs">${{Math.round(pinchProgress * 100)}}%</div>`}}
                        </div>
                    </div>
                </div>
            <//>
            <mesh visible=${{false}} name="UK_HITBOX"><sphereGeometry args=${{[0.8, 16, 16]}} /></mesh>
        </group>`;
    }};

    // Earth 组件
    const RealEarth = ({{ targetRotation, onHoverUK, pinchProgress, isExploding }}) => {{
        const earthRef = useRef(); const particlesRef = useRef();
        const [colorMap, normalMap, specMap] = useLoader(THREE.TextureLoader, [
            'https://cdn.jsdelivr.net/gh/mrdoob/three.js@master/examples/textures/planets/earth_atmos_2048.jpg',
            'https://cdn.jsdelivr.net/gh/mrdoob/three.js@master/examples/textures/planets/earth_normal_2048.jpg',
            'https://cdn.jsdelivr.net/gh/mrdoob/three.js@master/examples/textures/planets/earth_specular_2048.jpg'
        ]);

        useFrame((state, delta) => {{
            if (earthRef.current && !isExploding) {{
                earthRef.current.rotation.y = THREE.MathUtils.lerp(earthRef.current.rotation.y, targetRotation.current.y, 0.08);
                earthRef.current.rotation.x = THREE.MathUtils.lerp(earthRef.current.rotation.x, targetRotation.current.x, 0.08);
            }}
            if (isExploding && particlesRef.current) {{
                earthRef.current.visible = false; particlesRef.current.visible = true;
                particlesRef.current.scale.multiplyScalar(1.0 + (3.0 * delta));
                if (particlesRef.current.material.opacity > 0) particlesRef.current.material.opacity -= delta * 1.5;
            }}
        }});
        
        const r = 5; const phi = (90 - 53.0) * (Math.PI / 180); const theta = (-1.2 + 180) * (Math.PI / 180);
        const ukPos = [-(r * Math.sin(phi) * Math.cos(theta)), r * Math.cos(phi), r * Math.sin(phi) * Math.sin(theta)];

        return html`
            <group>
                <mesh ref=${{earthRef}} rotation=${{[0, -1.8, 0]}}>
                    <sphereGeometry args=${{[5, 64, 64]}} />
                    <meshStandardMaterial map=${{colorMap}} normalMap=${{normalMap}} roughnessMap=${{specMap}} metalness=${{0.2}} roughness=${{0.6}} />
                    <group position=${{ukPos}}><${{UKMarker}} isHovered=${{onHoverUK}} pinchProgress=${{pinchProgress}} /></group>
                </mesh>
                <points ref=${{particlesRef}} rotation=${{[0, -1.8, 0]}} visible=${{false}}>
                    <sphereGeometry args=${{[5, 96, 96]}} /> 
                    <pointsMaterial size=${{0.12}} color="#00fff2" transparent sizeAttenuation blending=${{THREE.AdditiveBlending}} />
                </points>
            </group>
        `;
    }};

    // Gesture Manager (跳转逻辑在这里)
    const GestureManager = ({{ targetRotation, targetZoom, isHoveringUK, setPinchProgress, setIsHoveringUK, setExploding }}) => {{
        const {{ camera, scene }} = useThree(); const raycaster = useMemo(() => new THREE.Raycaster(), []);
        useEffect(() => {{
            setTimeout(() => document.body.classList.add('intro-active'), 2500);
            let landmarker, video, cursor, running = true; let pinchStartTime = 0; const REQUIRED_TIME = 5000;
            
            const init = async () => {{
                video = document.getElementById('cam-video'); cursor = document.getElementById('hand-cursor');
                const vision = await FilesetResolver.forVisionTasks("https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.8/wasm");
                landmarker = await HandLandmarker.createFromOptions(vision, {{
                    baseOptions: {{ modelAssetPath: "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task", delegate: "GPU" }},
                    runningMode: "VIDEO", numHands: 1
                }});
                const stream = await navigator.mediaDevices.getUserMedia({{ video: {{ width: 640, height: 480 }} }});
                video.srcObject = stream; video.addEventListener('loadeddata', loop);
            }};

            const loop = async () => {{
                if (!running) return;
                if (landmarker && video.readyState >= 2) {{
                    const results = await landmarker.detectForVideo(video, performance.now());
                    if (results.landmarks && results.landmarks.length > 0) {{
                        const lm = results.landmarks[0]; const index = lm[8]; const thumb = lm[4];
                        const x = (1 - index.x) * window.innerWidth; const y = index.y * window.innerHeight;
                        
                        cursor.style.display = 'block'; cursor.style.left = x + 'px'; cursor.style.top = y + 'px';
                        
                        raycaster.setFromCamera({{ x: ((1 - index.x) * 2) - 1, y: -(index.y * 2) + 1 }}, camera);
                        const hitUK = raycaster.intersectObjects(scene.children, true).find(hit => hit.object.name === 'UK_HITBOX');
                        if (!!hitUK !== isHoveringUK.current) setIsHoveringUK(!!hitUK);

                        const isPinching = Math.hypot(index.x - thumb.x, index.y - thumb.y) < 0.06;

                        if (hitUK && isPinching) {{
                            cursor.className = 'hover-uk';
                            if (pinchStartTime === 0) pinchStartTime = Date.now();
                            const progress = Math.min((Date.now() - pinchStartTime) / REQUIRED_TIME, 1.0);
                            setPinchProgress(progress);
                            
                            if (progress >= 1.0) {{ 
                                running = false; setExploding(true);
                                document.body.classList.add('access-active');
                                setTimeout(() => {{ 
                                    document.body.classList.add('fading-out');
                                    console.log("Jumping to:", TARGET_URL);
                                    // *** 关键修复：使用 window.top 确保跳出 iframe ***
                                    window.top.location.href = TARGET_URL;
                                }}, 1800); 
                            }}
                        }} else {{
                            setPinchProgress(0); pinchStartTime = 0;
                            // 简单的手势缩放逻辑
                            const tips = [lm[4], lm[8], lm[12], lm[16], lm[20]];
                            let avgDist = tips.reduce((sum, t) => sum + Math.hypot(t.x - lm[0].x, t.y - lm[0].y), 0) / 5;
                            if (avgDist > 0.35) {{ targetZoom.current = Math.max(targetZoom.current - 0.08, 12); cursor.className = 'zoom-in'; }}
                            else if (avgDist < 0.15) {{ targetZoom.current = Math.min(targetZoom.current + 0.08, 50); cursor.className = 'zoom-out'; }}
                            else if (isPinching) {{ 
                                cursor.className = ''; 
                                targetRotation.current.y += (x - (cursor.dataset.lx || x)) * 0.003;
                                targetRotation.current.x += (y - (cursor.dataset.ly || y)) * 0.003;
                            }} else {{ cursor.className = ''; }}
                            cursor.dataset.lx = x; cursor.dataset.ly = y;
                        }}
                    }} else {{ cursor.style.display = 'none'; setPinchProgress(0); }}
                }}
                requestAnimationFrame(loop);
            }};
            init(); return () => {{ running = false; }};
        }}, []);
        return null;
    }};

    const App = () => {{
        const targetRotation = useRef({{ x: 0.2, y: -1.6 }}); const targetZoom = useRef(25);
        const [isHoveringUK, setIsHoveringUK] = useState(false); const [isExploding, setExploding] = useState(false);
        const isHoveringUKRef = useRef(false); const [pinchProgress, setPinchProgress] = useState(0);
        const setHoverWrapper = (val) => {{ isHoveringUKRef.current = val; setIsHoveringUK(val); }};

        return html`
            <div className="w-full h-screen bg-black relative">
                <${{Canvas}} gl=${{{{ antialias: true, toneMapping: THREE.ACESFilmicToneMapping }}}} camera=${{{{ position: [0, 0, 25], fov: 45 }}}}>
                    <${{OrbitControls}} enableRotate=${{false}} enableZoom=${{false}} enablePan=${{false}} />
                    <ambientLight intensity=${{0.8}} color="#bbddff" /><directionalLight position=${{[15, 10, 5]}} intensity=${{3.0}} /><pointLight position=${{[-20, 0, -20]}} intensity=${{2.0}} color="#00aaff" />
                    <${{Stars}} radius=${{300}} depth=${{100}} count=${{20000}} factor=${{8}} saturation=${{0}} fade speed=${{1}} />
                    <${{Suspense}} fallimport streamlit as st
import streamlit.components.v1 as components
import os
import base64

# 1. 设置页面全屏
st.set_page_config(layout="wide", page_title="SONAIR 3D Entry")

# ==========================================
# 核心修改：这里填入了你指定的 GitHub Pages 网址
TARGET_URL = "https://mingyutang0728.github.io/OMAIB-UoN-UCL/"
LOGO_FILE = "UoN-Nottingham-Blue.png"
# ==========================================

# 图片转 Base64 辅助函数
def get_image_base64(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

logo_base64 = get_image_base64(LOGO_FILE)
logo_src = f"data:image/png;base64,{logo_base64}" if logo_base64 else ""

# 2. 完整的 HTML/JS 代码
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SONAIR | Holographic Entry</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        :root {{ --neon: #00fff2; --alert: #ff3333; --hud: #00aaff; --bg: #000205; }}
        body {{ 
            margin: 0; background: var(--bg); overflow: hidden; user-select: none; font-family: 'Orbitron', sans-serif;
            opacity: 1; transition: opacity 1.5s cubic-bezier(0.25, 0.1, 0.25, 1);
        }}
        body.fading-out {{ opacity: 0; }}

        /* 欢迎动画 */
        #intro-layer {{
            position: fixed; inset: 0; background: #000; z-index: 10000;
            display: flex; align-items: center; justify-content: center;
            transition: all 1.5s cubic-bezier(0.16, 1, 0.3, 1); pointer-events: none;
        }}
        #intro-text {{
            font-size: 6rem; font-weight: 900; color: #fff; letter-spacing: 0.2em;
            text-shadow: 0 0 50px var(--neon); transition: all 1.5s; white-space: nowrap;
        }}
        body.intro-active #intro-layer {{ background: transparent; }}
        body.intro-active #intro-text {{
            font-size: 1.5rem; transform: translate(calc(-50vw + 160px), calc(-50vh + 50px)); 
            text-shadow: 0 0 10px var(--neon); letter-spacing: 0.1em;
        }}

        /* 摄像头框 */
        #cam-preview {{
            position: absolute; top: 20px; right: 20px; width: 400px; height: 300px;
            border-radius: 4px; overflow: hidden; border: 1px solid var(--neon);
            background: rgba(0,0,0,0.9); z-index: 50; opacity: 0; transition: opacity 1s 2s;
            box-shadow: 0 0 20px rgba(0, 255, 242, 0.1);
        }}
        body.intro-active #cam-preview {{ opacity: 1; }}
        #cam-video {{ width: 100%; height: 100%; object-fit: cover; transform: scaleX(-1); }}

        /* Logo */
        #uon-holo-logo {{ position: absolute; top: 10px; left: 10px; z-index: 60; opacity: 0; transition: opacity 1s 2s; }}
        body.intro-active #uon-holo-logo {{ opacity: 1; }}
        #uon-img {{ height: 35px; width: auto; filter: drop-shadow(0 0 5px rgba(0, 255, 242, 0.5)); }}

        /* 手势光标 */
        #hand-cursor {{
            position: fixed; top: 0; left: 0; width: 30px; height: 30px;
            border: 1px solid rgba(0, 255, 242, 0.5); border-radius: 50%;
            transform: translate(-50%, -50%); pointer-events: none; z-index: 9999;
            box-shadow: 0 0 10px var(--neon); display: none;
            transition: width 0.2s, height 0.2s, border-color 0.2s;
        }}
        #hand-cursor.zoom-in {{ border: 2px solid var(--neon); width: 60px; height: 60px; background: rgba(0, 255, 242, 0.1); box-shadow: 0 0 30px var(--neon); }}
        #hand-cursor.zoom-out {{ border: 2px solid var(--alert); width: 10px; height: 10px; background: rgba(255, 50, 50, 0.5); box-shadow: 0 0 30px var(--alert); }}
        #hand-cursor.hover-uk {{ border-color: #ffffff; box-shadow: 0 0 20px #ffffff; width: 40px; height: 40px; }}

        /* 指引卡片 */
        #instructions {{
            position: absolute; bottom: 40px; left: 40px; z-index: 50;
            opacity: 0; transition: opacity 1s 2.5s;
        }}
        body.intro-active #instructions {{ opacity: 1; }}
        .glass-card {{
            background: rgba(0, 10, 20, 0.7); backdrop-filter: blur(10px);
            border: 1px solid rgba(0, 255, 242, 0.2); box-shadow: 0 0 30px rgba(0,0,0,0.5);
        }}

        /* 跳转文字 */
        #access-granted {{
            position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
            color: #fff; font-size: 4rem; font-weight: 900; 
            text-shadow: 0 0 50px var(--neon), 0 0 20px var(--neon);
            opacity: 0; pointer-events: none; z-index: 10001; letter-spacing: 0.3em;
            transition: opacity 0.2s;
        }}
        body.access-active #access-granted {{ opacity: 1; }}
    </style>
</head>
<body>

<div id="intro-layer"><h1 id="intro-text">SONAIR UK</h1></div>
<div id="access-granted">INITIALIZING...</div>
<div id="hand-cursor"></div>

<div id="cam-preview">
    <video id="cam-video" autoplay muted playsinline></video>
    <div id="uon-holo-logo"><img id="uon-img" src="{logo_src}" alt="UoN Logo"></div>
    <div class="absolute bottom-0 w-full bg-cyan-900/80 text-[10px] text-center text-cyan-300 font-mono py-1 tracking-widest">
        UoN X UTC
    </div>
</div>

<div id="instructions" class="glass-card px-6 py-5 rounded-tr-2xl border-l-4 border-cyan-400 text-cyan-100 space-y-4">
    <div class="flex items-center gap-4">
        <div class="text-2xl text-cyan-400 w-8 text-center">✋</div>
        <div><div class="font-bold text-cyan-400 text-sm tracking-wider">PALM OPEN</div><div class="text-[10px] text-gray-400 font-sans">Zoom In (Enlarge)</div></div>
    </div>
    <div class="flex items-center gap-4">
        <div class="text-2xl text-pink-400 w-8 text-center">✊</div>
        <div><div class="font-bold text-pink-400 text-sm tracking-wider">FIST PINCH</div><div class="text-[10px] text-gray-400 font-sans">Zoom Out (Shrink)</div></div>
    </div>
    <div class="flex items-center gap-4">
        <div class="text-2xl text-white w-8 text-center">👌</div>
        <div><div class="font-bold text-white text-sm tracking-wider">TARGET UK</div><div class="text-[10px] text-gray-400 font-sans">Hold 5s to Warp</div></div>
    </div>
</div>

<div id="root"></div>

<script type="importmap">
{{
  "imports": {{
    "react": "https://esm.sh/react@18.2.0",
    "react-dom/client": "https://esm.sh/react-dom@18.2.0/client",
    "three": "https://esm.sh/three@0.150.1",
    "@react-three/fiber": "https://esm.sh/@react-three/fiber@8.13.0?deps=three@0.150.1,react@18.2.0",
    "@react-three/drei": "https://esm.sh/@react-three/drei@9.70.0?deps=three@0.150.1,react@18.2.0,@react-three/fiber@8.13.0",
    "htm": "https://esm.sh/htm@3.1.1",
    "@mediapipe/tasks-vision": "https://esm.sh/@mediapipe/tasks-vision@0.10.8"
  }}
}}
</script>

<script type="module">
    import React, {{ useState, useEffect, useRef, useMemo, Suspense }} from 'react';
    import {{ createRoot }} from 'react-dom/client';
    import htm from 'htm';
    import * as THREE from 'three';
    import {{ Canvas, useFrame, useLoader, useThree }} from '@react-three/fiber';
    import {{ Html, Stars, OrbitControls }} from '@react-three/drei';
    import {{ FilesetResolver, HandLandmarker }} from '@mediapipe/tasks-vision';

    const html = htm.bind(React.createElement);
    
    // JS 变量接收 Python 传来的 URL
    const TARGET_URL = "{TARGET_URL}";

    // --- UK 光标组件 ---
    const UKMarker = ({{ isHovered, pinchProgress }}) => {{
        const bracketRef = useRef();
        const innerRingRef = useRef();

        useFrame((state, delta) => {{
            if (bracketRef.current) bracketRef.current.rotation.z += delta * 0.5;
            if (innerRingRef.current) innerRingRef.current.rotation.z -= delta * 1.0;
        }});

        const radius = 28;
        const circumference = 2 * Math.PI * radius;
        const offset = circumference - (pinchProgress * circumference);
        const progressColor = pinchProgress > 0.8 ? "#ff0055" : "#00fff2";

        return html`
            <group position=${{[0, 0, 0]}}>
                <group rotation=${{[Math.PI/2, 0, 0]}} ref=${{bracketRef}}>
                    <mesh><ringGeometry args=${{[0.45, 0.48, 4, 1, 0, 1]}} /><meshBasicMaterial color="#00aaff" side=${{THREE.DoubleSide}} transparent opacity=${{0.6}} /></mesh>
                    <mesh rotation=${{[0, 0, Math.PI]}}><ringGeometry args=${{[0.45, 0.48, 4, 1, 0, 1]}} /><meshBasicMaterial color="#00aaff" side=${{THREE.DoubleSide}} transparent opacity=${{0.6}} /></mesh>
                </group>
                <mesh position=${{[0, 0.2, 0]}}><sphereGeometry args=${{[0.08, 16, 16]}} /><meshBasicMaterial color=${{isHovered ? "#ffffff" : "#00aaff"}} /></mesh>
                <${{Html}} position=${{[0, 0.6, 0]}} center distanceFactor=${{8}} style=${{{{pointerEvents:'none'}}}}>
                    <div className="flex flex-col items-center justify-center filter drop-shadow-[0_0_10px_rgba(0,255,242,0.5)]">
                        <div className="relative w-20 h-20 mb-2">
                            <svg width="80" height="80" viewBox="0 0 80 80" style=${{{{transform: 'rotate(-90deg)'}}}}>
                                <circle cx="40" cy="40" r="28" fill="none" stroke="rgba(0, 170, 255, 0.2)" strokeWidth="2" />
                                <circle cx="40" cy="40" r="28" fill="none" 
                                        stroke=${{progressColor}} strokeWidth="4" strokeLinecap="round"
                                        strokeDasharray=${{circumference}} strokeDashoffset=${{offset}}
                                        style=${{{{transition: 'stroke-dashoffset 0.1s linear'}}}} />
                            </svg>
                            <div className="absolute inset-0 flex items-center justify-center">
                                ${{pinchProgress > 0 && html`<div className="text-center"><div className="text-[10px] font-mono text-cyan-200 tracking-tighter">LOAD</div><div className="text-xs font-bold text-white font-mono">${{Math.round(pinchProgress * 100)}}%</div></div>`}}
                            </div>
                        </div>
                        <div className=${{"transition-all duration-300 " + (isHovered ? "opacity-100 translate-y-0" : "opacity-60 translate-y-1")}}>
                            <div className="bg-black/80 backdrop-blur border-x border-cyan-500/80 px-4 py-1 text-cyan-100 font-bold text-[10px] tracking-[0.2em]">UK HUB</div>
                            <div className="h-[1px] w-full bg-cyan-500 mt-0.5 shadow-[0_0_8px_cyan]"></div>
                        </div>
                    </div>
                <//>
                <mesh visible=${{false}} name="UK_HITBOX"><sphereGeometry args=${{[0.8, 16, 16]}} /></mesh>
            </group>
        `;
    }};

    // --- 地球组件 ---
    const RealEarth = ({{ targetRotation, onHoverUK, pinchProgress, isExploding }}) => {{
        const earthRef = useRef();
        const particlesRef = useRef();
        const [colorMap, normalMap, specMap] = useLoader(THREE.TextureLoader, [
            'https://cdn.jsdelivr.net/gh/mrdoob/three.js@master/examples/textures/planets/earth_atmos_2048.jpg',
            'https://cdn.jsdelivr.net/gh/mrdoob/three.js@master/examples/textures/planets/earth_normal_2048.jpg',
            'https://cdn.jsdelivr.net/gh/mrdoob/three.js@master/examples/textures/planets/earth_specular_2048.jpg'
        ]);

        useFrame((state, delta) => {{
            if (earthRef.current && !isExploding) {{
                earthRef.current.rotation.y = THREE.MathUtils.lerp(earthRef.current.rotation.y, targetRotation.current.y, 0.08);
                earthRef.current.rotation.x = THREE.MathUtils.lerp(earthRef.current.rotation.x, targetRotation.current.x, 0.08);
                if (particlesRef.current) {{ particlesRef.current.rotation.copy(earthRef.current.rotation); particlesRef.current.visible = false; }}
            }}
            if (isExploding && particlesRef.current) {{
                earthRef.current.visible = false; particlesRef.current.visible = true; 
                const expansionFactor = 1.0 + (3.0 * delta); particlesRef.current.scale.multiplyScalar(expansionFactor);
                if (particlesRef.current.material.opacity > 0) particlesRef.current.material.opacity -= delta * 1.5; 
            }}
        }});

        const r = 5;
        const phi = (90 - 53.0) * (Math.PI / 180);
        const theta = (-1.2 + 180) * (Math.PI / 180);
        const ukPos = [-(r * Math.sin(phi) * Math.cos(theta)), r * Math.cos(phi), r * Math.sin(phi) * Math.sin(theta)];

        return html`
            <group>
                <group ref=${{earthRef}} rotation=${{[0, -1.8, 0]}}>
                    <mesh>
                        <sphereGeometry args=${{[5, 64, 64]}} />
                        <meshStandardMaterial map=${{colorMap}} normalMap=${{normalMap}} normalScale=${{new THREE.Vector2(1.5, 1.5)}} roughnessMap=${{specMap}} roughness=${{0.6}} metalness=${{0.2}} emissive="#001133" emissiveIntensity=${{0.6}} color="#ffffff"/>
                    </mesh>
                    <group position=${{ukPos}}><${{UKMarker}} isHovered=${{onHoverUK}} pinchProgress=${{pinchProgress}} /></group>
                </group>
                <points ref=${{particlesRef}} rotation=${{[0, -1.8, 0]}} visible=${{false}}>
                    <sphereGeometry args=${{[5, 96, 96]}} /> 
                    <pointsMaterial size=${{0.12}} color="#00fff2" transparent opacity=${{1}} sizeAttenuation=${{true}} blending=${{THREE.AdditiveBlending}} />
                </points>
            </group>
        `;
    }};

    // --- 手势管理 (包含放大缩小逻辑) ---
    const GestureManager = ({{ targetRotation, targetZoom, isHoveringUK, setPinchProgress, setIsHoveringUK, setExploding }}) => {{
        const {{ camera, scene }} = useThree(); 
        const raycaster = useMemo(() => new THREE.Raycaster(), []);

        useEffect(() => {{
            setTimeout(() => document.body.classList.add('intro-active'), 2500);
            let landmarker, video, cursor, running = true;
            let lastHandPos = null;
            let pinchStartTime = 0;
            const REQUIRED_TIME = 5000; 

            const init = async () => {{
                video = document.getElementById('cam-video');
                cursor = document.getElementById('hand-cursor');
                const vision = await FilesetResolver.forVisionTasks("https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.8/wasm");
                landmarker = await HandLandmarker.createFromOptions(vision, {{
                    baseOptions: {{ modelAssetPath: "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task", delegate: "GPU" }},
                    runningMode: "VIDEO", numHands: 1
                }});
                const stream = await navigator.mediaDevices.getUserMedia({{ video: {{ width: 640, height: 480 }} }});
                video.srcObject = stream;
                video.addEventListener('loadeddata', loop);
            }};

            const loop = async () => {{
                if (!running) return;
                if (landmarker && video.readyState >= 2) {{
                    const results = await landmarker.detectForVideo(video, performance.now());
                    if (results.landmarks && results.landmarks.length > 0) {{
                        const lm = results.landmarks[0]; const wrist = lm[0]; const index = lm[8]; const thumb = lm[4];
                        const tips = [lm[4], lm[8], lm[12], lm[16], lm[20]];
                        let avgDist = 0;
                        tips.forEach(t => {{ avgDist += Math.sqrt(Math.pow(t.x - wrist.x, 2) + Math.pow(t.y - wrist.y, 2)); }});
                        avgDist /= 5;

                        const x = (1 - index.x) * window.innerWidth;
                        const y = index.y * window.innerHeight;
                        cursor.style.display = 'block'; cursor.style.left = x + 'px'; cursor.style.top = y + 'px';

                        const ndcX = ((1 - index.x) * 2) - 1; const ndcY = -(index.y * 2) + 1;
                        raycaster.setFromCamera({{ x: ndcX, y: ndcY }}, camera);
                        const intersects = raycaster.intersectObjects(scene.children, true);
                        const hitUK = intersects.find(hit => hit.object.name === 'UK_HITBOX');

                        if (!!hitUK !== isHoveringUK.current) setIsHoveringUK(!!hitUK);
                        const pinchDist = Math.hypot(index.x - thumb.x, index.y - thumb.y);
                        const isPinching = pinchDist < 0.06;

                        if (hitUK && isPinching) {{
                            cursor.className = 'hover-uk';
                            if (pinchStartTime === 0) pinchStartTime = Date.now();
                            const elapsed = Date.now() - pinchStartTime;
                            const progress = Math.min(elapsed / REQUIRED_TIME, 1.0);
                            setPinchProgress(progress);
                            if (progress >= 1.0) {{ 
                                running = false;
                                setExploding(true);
                                document.body.classList.add('access-active');
                                setTimeout(() => {{ 
                                    document.body.classList.add('fading-out');
                                    // *** 这里是跳转逻辑，使用 window.top 确保跳出框架 ***
                                    setTimeout(() => {{ window.top.location.href = TARGET_URL; }}, 1500);
                                }}, 1800); 
                            }}
                        }} else {{
                            setPinchProgress(0); pinchStartTime = 0;
                            // --- 恢复的放大缩小逻辑 ---
                            if (avgDist > 0.35) {{
                                cursor.className = 'zoom-in';
                                targetZoom.current = Math.max(targetZoom.current - 0.08, 12); 
                                lastHandPos = null;
                            }} else if (avgDist < 0.15) {{
                                cursor.className = 'zoom-out';
                                targetZoom.current = Math.min(targetZoom.current + 0.08, 50);
                                lastHandPos = null;
                            }} else if (isPinching) {{
                                cursor.className = ''; cursor.style.borderColor = "#fff"; 
                                if (lastHandPos) {{
                                    const deltaX = x - lastHandPos.x; const deltaY = y - lastHandPos.y;
                                    targetRotation.current.y += deltaX * 0.003; targetRotation.current.x += deltaY * 0.003;
                                }}
                                lastHandPos = {{ x, y }};
                            }} else {{
                                cursor.className = ''; lastHandPos = null;
                            }}
                        }}
                    }} else {{
                        cursor.style.display = 'none'; setPinchProgress(0); lastHandPos = null;
                    }}
                }}
                requestAnimationFrame(loop);
            }};
            init(); return () => {{ running = false; }};
        }}, []);
        return null;
    }};

    const App = () => {{
        const targetRotation = useRef({{ x: 0.2, y: -1.6 }});
        const targetZoom = useRef(25); 
        const [isHoveringUK, setIsHoveringUK] = useState(false);
        const [isExploding, setExploding] = useState(false);
        const isHoveringUKRef = useRef(false); 
        const [pinchProgress, setPinchProgress] = useState(0);

        const setHoverWrapper = (val) => {{ isHoveringUKRef.current = val; setIsHoveringUK(val); }};

        const CameraRig = () => {{
            useFrame(({{ camera }}) => {{
                camera.position.z = THREE.MathUtils.lerp(camera.position.z, targetZoom.current, 0.04);
            }});
            return null;
        }};

        return html`
            <div className="w-full h-screen bg-black relative">
                <${{Canvas}} gl=${{{{ antialias: true, toneMapping: THREE.ACESFilmicToneMapping }}}} camera=${{{{ position: [0, 0, 25], fov: 45 }}}}>
                    <${{OrbitControls}} enableRotate=${{false}} enableZoom=${{false}} enablePan=${{false}} />
                    <ambientLight intensity=${{0.8}} color="#bbddff" />
                    <directionalLight position=${{[15, 10, 5]}} intensity=${{3.0}} color="#ffffff" />
                    <pointLight position=${{[-20, 0, -20]}} intensity=${{2.0}} color="#00aaff" />
                    <${{Stars}} radius=${{300}} depth=${{100}} count=${{20000}} factor=${{8}} saturation=${{0}} fade speed=${{1}} />
                    <${{Suspense}} fallback=${{null}}>
                        <${{RealEarth}} targetRotation=${{targetRotation}} onHoverUK=${{isHoveringUK}} pinchProgress=${{pinchProgress}} isExploding=${{isExploding}} />
                    </${{Suspense}}>
                    <${{CameraRig}} />
                    <${{GestureManager}} 
                        targetRotation=${{targetRotation}} targetZoom=${{targetZoom}} 
                        isHoveringUK=${{isHoveringUKRef}} setIsHoveringUK=${{setHoverWrapper}}
                        setPinchProgress=${{setPinchProgress}} setExploding=${{setExploding}}
                    />
                </${{Canvas}}>
            </div>
        `;
    }};

    createRoot(document.getElementById('root')).render(html`<${{App}} />`);
</script>
</body>
</html>
"""

# 渲染 HTML
components.html(html_content, height=1000, scrolling=False)back=${{null}}>
                        <${{RealEarth}} targetRotation=${{targetRotation}} onHoverUK=${{isHoveringUK}} pinchProgress=${{pinchProgress}} isExploding=${{isExploding}} />
                    </${{Suspense}}>
                    <${{GestureManager}} targetRotation=${{targetRotation}} targetZoom=${{targetZoom}} isHoveringUK=${{isHoveringUKRef}} setIsHoveringUK=${{setHoverWrapper}} setPinchProgress=${{setPinchProgress}} setExploding=${{setExploding}} />
                </${{Canvas}}>
            </div>
        `;
    }};
    createRoot(document.getElementById('root')).render(html`<${{App}} />`);
</script>
</body>
</html>
"""

components.html(html_content, height=1000, scrolling=False)
