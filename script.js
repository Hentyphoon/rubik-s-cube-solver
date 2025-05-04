import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// --- Configuration ---
const CUBE_SIZE = 3; // 3x3x3 Rubik's Cube
const CUBELET_SIZE = 1;
const CUBELET_SPACING = 0.05; // Small gap between cubelets
const TOTAL_CUBELET_SIZE = CUBELET_SIZE + CUBELET_SPACING;

// Standard Rubik's Colors (Hex) & Mapping to Names
const COLORS = {
    white:  0xffffff,
    yellow: 0xffff00,
    red:    0xff0000,
    orange: 0xffa500,
    blue:   0x0000ff,
    green:  0x008000,
    gray:   0x404040 // Internal faces
};
const COLOR_NAMES = {
    [COLORS.white]: 'W',
    [COLORS.yellow]: 'Y',
    [COLORS.red]: 'R',
    [COLORS.orange]: 'O',
    [COLORS.blue]: 'B',
    [COLORS.green]: 'G',
    [COLORS.gray]: 'X' // Should not appear in final matrix
};
const FACE_COLORS = [
    COLORS.blue,   // Right (+x)
    COLORS.green,  // Left (-x)
    COLORS.white,  // Up (+y)
    COLORS.yellow, // Down (-y)
    COLORS.red,    // Front (+z)
    COLORS.orange  // Back (-z)
];

// Face Name Mapping (used for matrix generation)
const FACE_MAP = {
    RIGHT: 'R', LEFT: 'L', UP: 'U', DOWN: 'D', FRONT: 'F', BACK: 'B'
};

// --- Global Variables ---
let scene, camera, renderer, controls;
let cubeGroup; // Group to hold all cubelets
let cubelets = []; // Array to store individual cubelet meshes
let raycaster, mouse;
let selectedColor = COLORS.white; // Default selected color for painting
let currentCubeState = null; // To store the validated matrix state
let solutionSteps = [];
let currentStepIndex = -1;

// --- DOM Elements ---
const cubeContainer = document.getElementById('cube-container');
const colorPaletteContainer = document.getElementById('color-palette');
const resetButton = document.getElementById('reset-button');
const validateButton = document.getElementById('validate-button');
const solveButton = document.getElementById('solve-button');
const matrixOutput = document.getElementById('matrix-output');
const solutionDisplay = document.getElementById('solution-display');
const solutionCarousel = document.getElementById('solution-carousel');
const prevStepButton = document.getElementById('prev-step');
const nextStepButton = document.getElementById('next-step');
const stepCounter = document.getElementById('step-counter');
const messageBox = document.getElementById('message-box');
const loadingIndicator = document.getElementById('loading-indicator');

// --- Initialization ---
function init() {
    // Scene
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xeeeeee); // Light gray background

    // Camera
    camera = new THREE.PerspectiveCamera(75, cubeContainer.clientWidth / cubeContainer.clientHeight, 0.1, 1000);
    camera.position.set(4, 4, 5); // Adjusted camera position

    // Renderer
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(cubeContainer.clientWidth, cubeContainer.clientHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    cubeContainer.appendChild(renderer.domElement);

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(5, 10, 7.5);
    scene.add(directionalLight);

    // Controls
    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true; // Smooth camera movement
    controls.dampingFactor = 0.05;
    controls.screenSpacePanning = false;
    controls.minDistance = 5;
    controls.maxDistance = 20;

    // Raycaster for clicking
    raycaster = new THREE.Raycaster();
    mouse = new THREE.Vector2();

    // Create the Cube
    cubeGroup = new THREE.Group();
    createRubiksCube();
    scene.add(cubeGroup);

    // Setup UI
    setupColorPalette();
    setupEventListeners();

    // Hide loading indicator
    loadingIndicator.style.display = 'none';

    // Start animation loop
    animate();
}

// --- Create Rubik's Cube ---
function createRubiksCube(initialState = null) {
    // Clear existing cubelets if any
    cubeGroup.clear();
    cubelets = [];

    const centerOffset = (CUBE_SIZE - 1) / 2 * TOTAL_CUBELET_SIZE;

    for (let x = 0; x < CUBE_SIZE; x++) {
        for (let y = 0; y < CUBE_SIZE; y++) {
            for (let z = 0; z < CUBE_SIZE; z++) {
                // Skip the core cubelet (not visible)
                if (x > 0 && x < CUBE_SIZE - 1 && y > 0 && y < CUBE_SIZE - 1 && z > 0 && z < CUBE_SIZE - 1) {
                    continue;
                }

                const geometry = new THREE.BoxGeometry(CUBELET_SIZE, CUBELET_SIZE, CUBELET_SIZE);
                const materials = [];

                // Determine colors for each face based on position
                for (let i = 0; i < 6; i++) {
                    let color = COLORS.gray; // Default internal color
                    if (x === CUBE_SIZE - 1 && i === 0) color = COLORS.blue;   // Right (+x)
                    if (x === 0 && i === 1) color = COLORS.green;  // Left (-x)
                    if (y === CUBE_SIZE - 1 && i === 2) color = COLORS.white;  // Up (+y)
                    if (y === 0 && i === 3) color = COLORS.yellow; // Down (-y)
                    if (z === CUBE_SIZE - 1 && i === 4) color = COLORS.red;    // Front (+z)
                    if (z === 0 && i === 5) color = COLORS.orange; // Back (-z)

                    materials.push(new THREE.MeshStandardMaterial({
                        color: color,
                        roughness: 0.7,
                        metalness: 0.1
                    }));
                }

                const cubelet = new THREE.Mesh(geometry, materials);

                // Calculate position
                cubelet.position.set(
                    x * TOTAL_CUBELET_SIZE - centerOffset,
                    y * TOTAL_CUBELET_SIZE - centerOffset,
                    z * TOTAL_CUBELET_SIZE - centerOffset
                );

                 // Store position index for later reference (useful for matrix mapping)
                cubelet.userData.positionIndex = { x, y, z };

                cubeGroup.add(cubelet);
                cubelets.push(cubelet);
            }
        }
    }
     // If initialState is provided (e.g., from reset), apply it
     // This part would be more complex if loading a scrambled state initially
     if (initialState) {
         // TODO: Implement logic to apply a given state matrix to the cube colors
         console.log("Applying initial state (not fully implemented yet)");
     }
}

// --- UI Setup ---
function setupColorPalette() {
    // Clear existing swatches first
    colorPaletteContainer.innerHTML = '';
    Object.entries(COLORS).forEach(([name, hex]) => {
        if (name === 'gray') return; // Don't add gray to palette

        const swatch = document.createElement('div');
        // Apply Tailwind classes directly here
        swatch.className = 'color-swatch w-full h-10 rounded cursor-pointer border-2 border-transparent';
        swatch.style.backgroundColor = `#${hex.toString(16).padStart(6, '0')}`;
        swatch.dataset.color = hex;

        if (hex === selectedColor) {
            swatch.classList.add('selected');
        }

        swatch.addEventListener('click', () => {
            selectedColor = parseInt(swatch.dataset.color);
            // Update selection visual feedback
            document.querySelectorAll('.color-swatch').forEach(s => s.classList.remove('selected'));
            swatch.classList.add('selected');
        });

        colorPaletteContainer.appendChild(swatch);
    });
}

function setupEventListeners() {
    window.addEventListener('resize', onWindowResize);
    // Check if cubeContainer exists before adding listener
    if (cubeContainer) {
        cubeContainer.addEventListener('click', onCanvasClick); // Use click instead of mousedown/up
    } else {
        console.error("Could not find cube-container element");
    }
    // Add listeners for other buttons
    if (resetButton) resetButton.addEventListener('click', handleReset);
    if (validateButton) validateButton.addEventListener('click', handleValidate);
    if (solveButton) solveButton.addEventListener('click', handleSolve);
    if (prevStepButton) prevStepButton.addEventListener('click', showPreviousStep);
    if (nextStepButton) nextStepButton.addEventListener('click', showNextStep);
}

// --- Event Handlers ---
function onWindowResize() {
    // Check if camera and renderer are initialized
    if (camera && renderer && cubeContainer) {
        camera.aspect = cubeContainer.clientWidth / cubeContainer.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(cubeContainer.clientWidth, cubeContainer.clientHeight);
    }
}

function onCanvasClick(event) {
    // Check if renderer and raycaster are initialized
    if (!renderer || !raycaster || !camera || !cubelets) return;

    // Calculate mouse position in normalized device coordinates (-1 to +1)
    const rect = renderer.domElement.getBoundingClientRect();
    mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

    // Update the picking ray with the camera and mouse position
    raycaster.setFromCamera(mouse, camera);

    // Calculate objects intersecting the picking ray
    const intersects = raycaster.intersectObjects(cubelets);

    if (intersects.length > 0) {
        const intersection = intersects[0];
        const object = intersection.object; // The cubelet mesh
        const face = intersection.face;

        // Ensure face and material exist
        if (!face || !object.material || !Array.isArray(object.material) || face.materialIndex === undefined) {
            console.error("Intersection data is incomplete.");
            return;
        }
        const faceIndex = face.materialIndex; // Index of the clicked face material

         // Don't allow changing center pieces (assuming standard cube)
        const pos = object.userData.positionIndex;
        // Check if pos exists and has x, y, z
        if (!pos || typeof pos.x === 'undefined' || typeof pos.y === 'undefined' || typeof pos.z === 'undefined') {
            console.error("Cubelet position data missing.");
            return;
        }
        const isCenter = [pos.x, pos.y, pos.z].filter(coord => coord === 1).length === 2;

        // Get the current color of the face
        const currentFaceMaterial = object.material[faceIndex];
        if (!currentFaceMaterial || !currentFaceMaterial.color) {
             console.error("Clicked face material or color missing.");
             return;
        }
        const currentFaceColor = currentFaceMaterial.color.getHex();

        // Only allow changing non-gray faces and non-center faces
        if (currentFaceColor !== COLORS.gray && !isCenter) {
            currentFaceMaterial.color.setHex(selectedColor);
            // Invalidate current state and disable solve button
            currentCubeState = null;
            if (solveButton) solveButton.disabled = true;
            if (matrixOutput) matrixOutput.textContent = 'Cube state changed. Please re-validate.';
            clearSolution();
        } else if (isCenter) {
             showMessage('Center pieces cannot be changed.', 'error');
        }
    }
}

function handleReset() {
    // Recreate the cube in its solved state
    createRubiksCube();
    // Reset UI elements
    currentCubeState = null;
    if (solveButton) solveButton.disabled = true;
    if (matrixOutput) matrixOutput.textContent = 'Cube reset. Validate to get matrix.';
    clearSolution();
    showMessage('Cube reset to solved state.', 'success');
}

function handleValidate() {
    const state = convertToMatrix();
    if (!state) { // Check if matrix conversion failed
        showMessage('Error converting cube state to matrix. Check console.', 'error');
        if (matrixOutput) matrixOutput.textContent = 'Error during matrix conversion.';
        if (solveButton) solveButton.disabled = true;
        return;
    }

    const validationResult = validateCubeState(state);

    if (validationResult.valid) {
        currentCubeState = state; // Store the valid state
        if (matrixOutput) matrixOutput.textContent = JSON.stringify(state, null, 2);
        if (solveButton) solveButton.disabled = false; // Enable solve button
        showMessage('Cube state is valid!', 'success');
        clearSolution(); // Clear previous solution if any
    } else {
        currentCubeState = null;
        if (matrixOutput) matrixOutput.textContent = `Invalid State:\n${validationResult.errors.join('\n')}`;
        if (solveButton) solveButton.disabled = true;
        showMessage(`Invalid Cube State: ${validationResult.errors[0]}`, 'error'); // Show first error
    }
}

function handleSolve() {
    if (!currentCubeState) {
         showMessage('Please validate the cube state first.', 'error');
        return;
    }

    // --- Backend Simulation ---
    console.log("Sending to backend (simulated):", currentCubeState);
    // In a real app, you would make an API call here:
    // fetch('/api/solve', { method: 'POST', body: JSON.stringify(currentCubeState), headers: {'Content-Type': 'application/json'} })
    //   .then(res => res.json())
    //   .then(data => displaySolution(data.steps))
    //   .catch(error => {
    //      console.error('Error solving cube:', error);
    //      showMessage('Error communicating with solver backend.', 'error');
    //   });

    // Simulate receiving steps after a short delay
    showMessage('Solving... (simulated)', 'success');
    setTimeout(() => {
        // Example solution steps (replace with actual backend response)
        const simulatedSteps = ["F", "R", "U", "R'", "U'", "F'", "D2", "L", "B'", "U2", "R", "D"];
        displaySolution(simulatedSteps);
    }, 500); // Simulate network delay
     // --- End Simulation ---
}

// --- Solution Display & Carousel ---
 function displaySolution(steps) {
    solutionSteps = steps;
    if (steps && steps.length > 0) {
        currentStepIndex = 0;
        updateSolutionDisplay();
        if(solutionCarousel) solutionCarousel.classList.remove('hidden');
        showMessage(`Solution found with ${steps.length} steps.`, 'success');
    } else {
        if(solutionDisplay) solutionDisplay.innerHTML = '<span class="text-gray-500">No solution found or provided.</span>';
        if(solutionCarousel) solutionCarousel.classList.add('hidden');
        currentStepIndex = -1;
    }
}

function clearSolution() {
    solutionSteps = [];
    currentStepIndex = -1;
    if (solutionDisplay) solutionDisplay.innerHTML = '<span class="text-gray-500">No solution yet.</span>';
    if (solutionCarousel) solutionCarousel.classList.add('hidden');
    if (stepCounter) stepCounter.textContent = `Step 0 / 0`;
    if (prevStepButton) prevStepButton.disabled = true;
    if (nextStepButton) nextStepButton.disabled = true;
}

function updateSolutionDisplay() {
    if (currentStepIndex >= 0 && currentStepIndex < solutionSteps.length) {
        if (solutionDisplay) solutionDisplay.innerHTML = `<span class="font-mono text-lg font-bold">${solutionSteps[currentStepIndex]}</span>`;
        if (stepCounter) stepCounter.textContent = `Step ${currentStepIndex + 1} / ${solutionSteps.length}`;
    } else if (solutionSteps.length > 0) { // Handle the "Done!" state only if there were steps
         if (solutionDisplay) solutionDisplay.innerHTML = `<span class="font-mono text-lg font-bold">Done!</span>`;
         if (stepCounter) stepCounter.textContent = `Step ${solutionSteps.length} / ${solutionSteps.length}`; // Show final step count
    } else {
        // If no steps, revert to initial state message
        clearSolution();
    }


    // Update button states
    if (prevStepButton) prevStepButton.disabled = currentStepIndex <= 0;
    if (nextStepButton) nextStepButton.disabled = currentStepIndex >= solutionSteps.length - 1;
}


function showPreviousStep() {
    if (currentStepIndex > 0) {
        currentStepIndex--;
        updateSolutionDisplay();
        // TODO: Optionally, animate the cube backwards (more complex)
    }
}

function showNextStep() {
    if (currentStepIndex < solutionSteps.length - 1) {
        currentStepIndex++;
        updateSolutionDisplay();
        // TODO: Optionally, animate the cube forwards according to the step (more complex)
    }
}


// --- Cube State Logic ---

function convertToMatrix() {
    const state = { F: [], B: [], U: [], D: [], L: [], R: [] };
    let conversionError = false;
    // Initialize with nulls or placeholders
    for (const face in state) {
        state[face] = Array(9).fill(null);
    }

    cubelets.forEach(cubelet => {
        if (conversionError) return; // Stop processing if an error occurred

        const pos = cubelet.userData.positionIndex; // {x, y, z} from 0 to 2
        if (!pos || typeof pos.x === 'undefined' || typeof pos.y === 'undefined' || typeof pos.z === 'undefined') {
            console.error("Missing position data on cubelet:", cubelet);
            conversionError = true;
            return;
        }

        if (!Array.isArray(cubelet.material)) {
            console.error("Cubelet material is not an array:", cubelet);
            conversionError = true;
            return;
        }


        cubelet.material.forEach((material, faceIndex) => {
             if (conversionError) return;
             if (!material || !material.color) {
                 console.error(`Missing material or color for face ${faceIndex} on cubelet at`, pos);
                 conversionError = true;
                 return;
             }

            const colorHex = material.color.getHex();
            if (colorHex === COLORS.gray) return; // Skip internal faces

            const colorName = COLOR_NAMES[colorHex];
            if (!colorName) {
                 console.error(`Unknown color hex ${colorHex.toString(16)} found on face ${faceIndex} at`, pos);
                 conversionError = true; // Treat unknown colors as an error
                 return;
            }


            // Determine which face (F, B, U, D, L, R) and position (0-8) this sticker belongs to
            let targetFace = null;
            let matrixIndex = -1;

            // Mapping logic (same as before)
            if (faceIndex === 0 && pos.x === 2) { targetFace = FACE_MAP.RIGHT; matrixIndex = (2 - y) * 3 + z; }
            else if (faceIndex === 1 && pos.x === 0) { targetFace = FACE_MAP.LEFT; matrixIndex = (2 - y) * 3 + (2-z); }
            else if (faceIndex === 2 && pos.y === 2) { targetFace = FACE_MAP.UP; matrixIndex = z * 3 + x; } // Original: (2-z)*3 + x; Corrected based on visualization? Let's try z*3+x
            else if (faceIndex === 3 && pos.y === 0) { targetFace = FACE_MAP.DOWN; matrixIndex = (2-z) * 3 + x; } // Original: z * 3 + x; Corrected based on visualization? Let's try (2-z)*3+x
            else if (faceIndex === 4 && pos.z === 2) { targetFace = FACE_MAP.FRONT; matrixIndex = (2-y) * 3 + x; }
            else if (faceIndex === 5 && pos.z === 0) { targetFace = FACE_MAP.BACK; matrixIndex = (2-y) * 3 + (2-x); }


            if (targetFace !== null && matrixIndex >= 0 && matrixIndex < 9) {
                 // Check if the position is already filled
                if (state[targetFace][matrixIndex] !== null) {
                    console.warn(`Overwriting matrix position! Face: ${targetFace}, Index: ${matrixIndex}. Old: ${state[targetFace][matrixIndex]}, New: ${colorName}`);
                    // Allow overwrite but log warning
                }
                state[targetFace][matrixIndex] = colorName;
            } else if (colorHex !== COLORS.gray) {
                 console.error("Error mapping face:", { pos, faceIndex, colorName });
                 conversionError = true;
            }
        });
    });

     // Final check for any nulls after processing all cubelets
    if (!conversionError) {
        for (const face in state) {
            if (state[face].includes(null)) {
                console.error(`Face ${face} has unassigned stickers:`, state[face]);
                conversionError = true; // Mark as error if any face is incomplete
                break; // Exit loop early
            }
        }
    }

    // Return null if there was an error during conversion
    return conversionError ? null : state;
}


function validateCubeState(state) {
    // Check if state is null or not an object (could happen if convertToMatrix failed)
    if (!state || typeof state !== 'object') {
        return { valid: false, errors: ["Invalid state object provided."] };
    }

    const errors = [];
    const colorCounts = {};
    let totalStickers = 0;
    const expectedFaces = ['F', 'B', 'U', 'D', 'L', 'R'];
    const expectedColors = ['W', 'Y', 'R', 'O', 'B', 'G'];

    // Check if all expected faces exist
    expectedFaces.forEach(faceName => {
        if (!state[faceName]) {
            errors.push(`State is missing face: ${faceName}.`);
        }
    });

    // If faces are missing, return early as further checks are pointless
    if (errors.length > 0) {
        return { valid: false, errors };
    }


    // 1. Count colors on each face and total counts
    for (const faceName in state) {
         // Check if it's an expected face (might be redundant now but safe)
         if (!expectedFaces.includes(faceName)) {
             errors.push(`Unexpected face "${faceName}" found in state.`);
             continue;
         }

        const faceColors = state[faceName];
        if (!Array.isArray(faceColors) || faceColors.length !== 9) {
            errors.push(`Face ${faceName} is not an array of 9 stickers.`);
            continue; // Skip this face if format is wrong
        }

        faceColors.forEach((color, index) => {
            if (color && expectedColors.includes(color)) {
                colorCounts[color] = (colorCounts[color] || 0) + 1;
                totalStickers++;
            } else if (!color) {
                 errors.push(`Face ${faceName} has a missing sticker (null) at index ${index}.`);
            } else if (color !== 'X') { // Allow 'X' but flag other unexpected values
                errors.push(`Unexpected value "${color}" found on face ${faceName} at index ${index}.`);
            }
        });
    }

    // 2. Check total sticker count
    const expectedTotal = 9 * 6; // 9 stickers per face * 6 faces
    if (totalStickers !== expectedTotal && errors.length === 0) { // Only add this error if others haven't masked it
        errors.push(`Expected ${expectedTotal} stickers, but found ${totalStickers}.`);
    }

    // 3. Check if there are exactly 9 of each standard color
    expectedColors.forEach(color => {
        if ((colorCounts[color] || 0) !== 9) {
            errors.push(`Expected 9 stickers of color ${color}, but found ${colorCounts[color] || 0}.`);
        }
    });

    // 4. Check for unexpected colors (already partially covered in step 1, but this catches counts of unexpected colors)
    Object.keys(colorCounts).forEach(color => {
        if (!expectedColors.includes(color)) {
            // This case should ideally be caught earlier, but serves as a fallback.
            errors.push(`Unexpected color "${color}" was counted ${colorCounts[color]} times.`);
        }
    });

     // 5. Check Center Pieces (assuming standard color scheme)
     const centerMappings = { F: 'R', B: 'O', U: 'W', D: 'Y', L: 'G', R: 'B' };
     for (const faceName in centerMappings) {
         // Ensure the face and its center sticker exist before checking
         if (state[faceName] && state[faceName].length === 9) {
             const expectedCenterColor = centerMappings[faceName];
             const actualCenterColor = state[faceName][4]; // Center sticker is index 4
             if (actualCenterColor !== expectedCenterColor) {
                 errors.push(`Center piece of face ${faceName} should be ${expectedCenterColor} but is ${actualCenterColor}.`);
             }
         } else if (state[faceName]) {
            // Error already logged about face length
         } else {
            // Error already logged about missing face
         }
     }

    // More advanced checks (edge/corner piece validity) could be added here,
    // but require more complex graph theory or algorithms.

    return {
        valid: errors.length === 0,
        errors: errors
    };
}


// --- Utility Functions ---
let messageTimeout;
function showMessage(text, type = 'success', duration = 3000) {
    if (!messageBox) return; // Don't try to show if element doesn't exist

    messageBox.textContent = text;
    // Use classList for better class management
    messageBox.classList.remove('success', 'error'); // Remove previous types
    messageBox.classList.add(type); // Add current type
    messageBox.style.display = 'block';

    clearTimeout(messageTimeout); // Clear previous timeout if any
    messageTimeout = setTimeout(() => {
        if (messageBox) messageBox.style.display = 'none';
    }, duration);
}


// --- Animation Loop ---
function animate() {
    requestAnimationFrame(animate);
    // Check if controls and renderer are initialized
    if (controls) controls.update();
    if (renderer && scene && camera) renderer.render(scene, camera);
}

// --- Start ---
// Ensure the DOM is fully loaded before initializing
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init(); // DOMContentLoaded has already fired
}
