import streamlit as st
import streamlit.components.v1 as components
import os
import base64

# 1. 设置页面全屏
st.set_page_config(layout="wide", page_title="SONAIR 3D Entry")

# ==========================================
# 配置区域
# ==========================================
TARGET_URL = "https://mingyutang0728.github.io/OMAIB-UoN-UCL/"
LOGO_FILE = "UoN-Nottingham-Blue.png"

# 图片转 Base64
def get_image_base64(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

logo_base64 = get_image_base64(LOGO_FILE)
logo_src = f"data:image/png;base64,{logo_base64}" if logo_base64 else ""

# ==========================================
# 核心代码 (使用纯字符串，避免语法冲突)
# ==========================================
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SONAIR</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        :root { --neon: #00fff2; --alert: #ff3333; --bg: #000205; }
        body { margin: 0; background: var(--bg); overflow: hidden; user-select: none; font-family: 'Orbitron', sans-serif; }
        
        /* Loading / Intro */
        #intro-layer { position: fixed; inset: 0; background: #000; z-index: 10000; display: flex; align-items: center; justify-content: center; pointer-events: none; transition: opacity 1s; }
        #intro-text { font-size: 4rem; font-weight: 900; color: #fff; text-shadow: 0 0 50px var(--neon); }
        body.loaded #intro-layer { opacity: 0; }

        /* HUD & Camera */
        #cam-preview {
            position: absolute; top: 20px; right: 20px; width: 320px; height: 240px;
            border: 1px solid var(--neon); background: rgba(0,0,0,0.8); z-index: 50;
            border-radius: 8px; overflow: hidden;
        }
        #cam-video { width: 100%; height: 100%; object-fit: cover; transform: scaleX(-1); }
        #uon-logo { position: absolute; top: 10px; left: 10px; height: 30px; z-index: 60; filter: drop-shadow(0 0 5px var(--neon)); }

        /* Hand Cursor */
        #hand-cursor {
            position: fixed; top: 0; left: 0; width: 20px; height: 20px;
            border: 2px solid var(--neon); border-radius: 50%;
            transform: translate(-50%, -50%); pointer-events: none; z-index: 9999; display: none;
            box-shadow: 0 0 10px var(--neon);
        }
        #hand-cursor.zoom-in { width: 50px; height: 50px; background: rgba(0, 255, 242, 0.2); }
        #hand-cursor.zoom-out { width: 10px; height: 10px; border-color: var(--alert); background: rgba(255, 50, 50, 0.5); }

        /* Jumping Text */
        #jump-overlay {
            position: fixed; inset: 0; background: black; z-index: 10002; display: flex; align-items: center; justify-content: center;
            opacity: 0; pointer-events: none; transition: opacity 1s;
        }
        #jump-overlay.active { opacity: 1; pointer-events: auto; }
        .jump-text { color: var(--neon); font-size: 3rem; font-weight: bold; letter-spacing: 0.2em; animation: pulse 1s infinite; }
        @keyframes pulse { 0% { opacity: 0.5; } 100% { opacity: 1; } }
    </style>
</head>
<body>

<div id="intro-layer"><h1 id="intro-text">INITIALIZING...</h1></div>
<div id="jump-overlay"><div class="jump-text">WARPING TO UK...</div></div>
<div id="hand-cursor"></div>

<div id="cam-preview">
    <video id="cam-video" autoplay muted playsinline></video>
    <img id="uon-logo" src="__LOGO_SRC__">
    <div class="absolute bottom-0 w-full bg-cyan-900/80 text-[10px] text-center text-cyan-300 font-mono py-1">System Active</div>
</div>

<div id="instructions" class="fixed bottom-10 left-10 p-5 rounded-xl border-l-4 border-cyan-400 bg-gray-900/80 text-cyan-100 space-y-3 backdrop-blur-md z-50">
    <div class="flex items-center gap-3"><div class="text-xl">✋</div><div><span class="font-bold text-cyan-400">OPEN PALM</span><br><span class="text-xs text-gray-400">Zoom In</span></div></div>
    <div class="flex items-center gap-3"><div class="text-xl">✊</div><div><span class="font-bold text-pink-500">FIST</span><br><span class="text-xs text-gray-400">Zoom Out</span></div></div>
    <div class="flex items-center gap-3"><div class="text-xl">👌</div><div><span class="font-bold text-white">PINCH UK</span><br><span class="text-xs text-gray-400">Jump</span></div></div>
</div>

<div id="root"></div>

<script type="importmap">
{
  "imports": {
    "react": "https://esm.sh/react@18.2.0",
    "react-dom/client": "https://esm.sh/react-dom@18.2.0/client",
    "three": "https://esm.sh/three@0.150.1",
    "@react-three/fiber": "https://esm.sh/@react-three/fiber@8.13.0?deps=three@0.150.1,react@18.2.0",
    "@react-three/drei": "https://esm.sh/@react-three/drei@9.70.0?deps=three@0.150.1,react@18.2.0,@react-three/fiber@8.13.0",
    "htm": "https://esm.sh/htm@3.1.1",
    "@mediapipe/tasks-vision": "https://esm.sh/@mediapipe/tasks-vision@0.10.8"
  }
}
</script>

<script type="module">
    import React, { useState, useEffect, useRef, useMemo, Suspense } from 'react';
    import { createRoot } from 'react-dom/client';
    import htm from 'htm';
    import * as THREE from 'three';
    import { Canvas, useFrame, useLoader, useThree } from '@react-three/fiber';
    import { Html, Stars, OrbitControls } from '@react-three/drei';
    import { FilesetResolver, HandLandmarker } from '@mediapipe/tasks-vision';

    const html = htm.bind(React.createElement);
    const TARGET_URL = "__TARGET_URL__";

    // --- Components ---

    const UKMarker = ({ isHovered, pinchProgress }) => {
        const ref = useRef();
        useFrame((state, delta) => { if(ref.current) ref.current.rotation.z -= delta; });
        
        const color = pinchProgress > 0 ? "#ff0055" : "#00fff2";
        
        return html`
            <group position=${[0, 0, 0]}>
                <mesh ref=${ref}>
                    <ringGeometry args=${[0.5, 0.55, 32]} />
                    <meshBasicMaterial color=${color} side=${THREE.DoubleSide} />
                </mesh>
                <${Html} position=${[0, 0.8, 0]} center style=${{pointerEvents:'none'}}>
                    <div class="text-white text-xs font-bold bg-black/50 px-2 rounded border border-cyan-500">
                        ${pinchProgress > 0 ? Math.round(pinchProgress * 100) + '%' : 'UK HUB'}
                    </div>
                <//>
                <mesh name="UK_HITBOX" visible=${false}><sphereGeometry args=${[0.8, 16, 16]} /></mesh>
            </group>
        `;
    };

    const Earth = ({ targetRotation, onHoverUK, pinchProgress, isExploding }) => {
        const earthRef = useRef();
        const [colorMap, normalMap] = useLoader(THREE.TextureLoader, [
            'https://cdn.jsdelivr.net/gh/mrdoob/three.js@master/examples/textures/planets/earth_atmos_2048.jpg',
            'https://cdn.jsdelivr.net/gh/mrdoob/three.js@master/examples/textures/planets/earth_normal_2048.jpg'
        ]);

        useFrame(() => {
            if (earthRef.current && !isExploding) {
                earthRef.current.rotation.y = THREE.MathUtils.lerp(earthRef.current.rotation.y, targetRotation.current.y, 0.1);
                earthRef.current.rotation.x = THREE.MathUtils.lerp(earthRef.current.rotation.x, targetRotation.current.x, 0.1);
            }
            if (isExploding && earthRef.current) {
                earthRef.current.scale.multiplyScalar(1.1);
                earthRef.current.material.opacity -= 0.05;
                earthRef.current.material.transparent = true;
            }
        });

        // UK Coordinates
        const r = 5; 
        const phi = (90 - 53.0) * (Math.PI / 180); 
        const theta = (-1.2 + 180) * (Math.PI / 180);
        const ukPos = [-(r * Math.sin(phi) * Math.cos(theta)), r * Math.cos(phi), r * Math.sin(phi) * Math.sin(theta)];

        return html`
            <mesh ref=${earthRef} rotation=${[0, -1.8, 0]}>
                <sphereGeometry args=${[5, 64, 64]} />
                <meshStandardMaterial map=${colorMap} normalMap=${normalMap} metalness=${0.2} roughness=${0.7} />
                <group position=${ukPos}>
                    <${UKMarker} isHovered=${onHoverUK} pinchProgress=${pinchProgress} />
                </group>
            </mesh>
        `;
    };

    const GestureController = ({ targetRotation, targetZoom, isHoveringUK, setPinchProgress, setExploding }) => {
        const { camera, scene } = useThree();
        const raycaster = useMemo(() => new THREE.Raycaster(), []);

        useEffect(() => {
            const video = document.getElementById('cam-video');
            const cursor = document.getElementById('hand-cursor');
            let landmarker;
            let running = true;
            let pinchStart = 0;

            const setup = async () => {
                const vision = await FilesetResolver.forVisionTasks("https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.8/wasm");
                landmarker = await HandLandmarker.createFromOptions(vision, {
                    baseOptions: { modelAssetPath: "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task", delegate: "GPU" },
                    runningMode: "VIDEO", numHands: 1
                });
                const stream = await navigator.mediaDevices.getUserMedia({ video: { width: 640, height: 480 } });
                video.srcObject = stream;
                video.onloadeddata = () => {
                    document.body.classList.add('loaded');
                    predict();
                };
            };

            const predict = async () => {
                if (!running) return;
                if (landmarker && video.readyState >= 2) {
                    const results = await landmarker.detectForVideo(video, performance.now());
                    
                    if (results.landmarks && results.landmarks.length > 0) {
                        const lm = results.landmarks[0];
                        const index = lm[8]; const thumb = lm[4]; const wrist = lm[0];
                        
                        // Cursor Logic
                        const x = (1 - index.x) * window.innerWidth;
                        const y = index.y * window.innerHeight;
                        cursor.style.display = 'block';
                        cursor.style.left = x + 'px'; cursor.style.top = y + 'px';

                        // Raycasting for UK Hit
                        const ndcX = ((1 - index.x) * 2) - 1;
                        const ndcY = -(index.y * 2) + 1;
                        raycaster.setFromCamera({ x: ndcX, y: ndcY }, camera);
                        const hits = raycaster.intersectObjects(scene.children, true);
                        const hitUK = hits.find(h => h.object.name === 'UK_HITBOX');
                        
                        // State Update
                        if (!!hitUK !== isHoveringUK.current) isHoveringUK.current = !!hitUK;

                        // Gesture Calculations
                        const pinchDist = Math.hypot(index.x - thumb.x, index.y - thumb.y);
                        const isPinching = pinchDist < 0.08; // Threshold for pinch

                        // Calculate "Spread" (Avg distance of fingertips to wrist)
                        const tips = [lm[4], lm[8], lm[12], lm[16], lm[20]];
                        let spread = tips.reduce((acc, t) => acc + Math.hypot(t.x - wrist.x, t.y - wrist.y), 0) / 5;

                        // --- INTERACTION LOGIC ---

                        if (hitUK && isPinching) {
                            // Trigger Jump Logic
                            cursor.className = 'zoom-in'; // Visual feedback
                            if (pinchStart === 0) pinchStart = Date.now();
                            const progress = Math.min((Date.now() - pinchStart) / 2000, 1); // 2 seconds to hold
                            setPinchProgress(progress);

                            if (progress >= 1) {
                                running = false;
                                setExploding(true);
                                document.getElementById('jump-overlay').classList.add('active');
                                setTimeout(() => {
                                    // *** CRITICAL FIX: Open in new tab to bypass Sandbox ***
                                    window.open(TARGET_URL, '_blank'); 
                                }, 1500);
                            }
                        } else {
                            setPinchProgress(0); pinchStart = 0;
                            
                            // Zoom Logic (Adjusted Thresholds)
                            if (spread > 0.35) {
                                cursor.className = 'zoom-in';
                                targetZoom.current = Math.max(targetZoom.current - 0.2, 12);
                            } else if (spread < 0.25) { 
                                cursor.className = 'zoom-out';
                                targetZoom.current = Math.min(targetZoom.current + 0.2, 40);
                            } else if (isPinching) {
                                // Rotate Logic
                                cursor.className = '';
                                targetRotation.current.y += (x - (cursor.lx || x)) * 0.005;
                                targetRotation.current.x += (y - (cursor.ly || y)) * 0.005;
                            } else {
                                cursor.className = '';
                            }
                            cursor.lx = x; cursor.ly = y;
                        }
                    } else {
                        cursor.style.display = 'none';
                    }
                }
                requestAnimationFrame(predict);
            };

            setup();
            return () => { running = false; };
        }, []);
        return null;
    };

    const App = () => {
        const targetRotation = useRef({ x: 0.2, y: -1.6 });
        const targetZoom = useRef(25);
        const isHoveringUK = useRef(false);
        const [pinchProgress, setPinchProgress] = useState(0);
        const [isExploding, setExploding] = useState(false);

        const CameraRig = () => {
            useFrame(({ camera }) => {
                camera.position.z = THREE.MathUtils.lerp(camera.position.z, targetZoom.current, 0.05);
            });
            return null;
        };

        return html`
            <div style=${{width:'100vw', height:'100vh', background:'black'}}>
                <${Canvas} camera=${{position: [0, 0, 25], fov: 45}}>
                    <ambientLight intensity=${0.5} />
                    <pointLight position=${[-10, 10, 10]} intensity=${2} />
                    <${Stars} />
                    <${Suspense} fallback=${null}>
                        <${Earth} 
                            targetRotation=${targetRotation} 
                            onHoverUK=${isHoveringUK} 
                            pinchProgress=${pinchProgress} 
                            isExploding=${isExploding}
                        />
                    </${Suspense}>
                    <${CameraRig} />
                    <${GestureController} 
                        targetRotation=${targetRotation} 
                        targetZoom=${targetZoom} 
                        isHoveringUK=${isHoveringUK} 
                        setPinchProgress=${setPinchProgress}
                        setExploding=${setExploding}
                    />
                    <${OrbitControls} enableZoom=${false} enableRotate=${false} />
                <//>
            </div>
        `;
    };

    createRoot(document.getElementById('root')).render(html`<${App} />`);
</script>
</body>
</html>
"""

# 使用 replace 方法注入变量，这是最安全的做法
html_content = html_template.replace("__TARGET_URL__", TARGET_URL)
html_content = html_content.replace("__LOGO_SRC__", logo_src)

components.html(html_content, height=1000, scrolling=False)
