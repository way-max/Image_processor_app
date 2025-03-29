import { createElement } from "./utils.js";

// Function to create the main container
export function createCountryFlagLogoContainer() {
    const container = createElement('div', { class: 'flag-logo-container' });

    const header = createElement('h1', {}, 'Generate a Country Flag Logo');
    container.appendChild(header);

    const inputContainer = createInputContainer();
    container.appendChild(inputContainer);

    const loadingMessage = createElement('p', { id: 'loading-message', style: 'display: none;' }, 'Generating logo, please wait...');
    container.appendChild(loadingMessage);

    const logoContainer = createElement('div', { id: 'logo-container' });
    container.appendChild(logoContainer);

    return container;
}

// Function to create the input container
function createInputContainer() {
    const inputContainer = createElement('div', { class: 'input-container' });

    const label = createElement('label', { for: 'prompt-input' }, 'Enter Prompt:');
    const input = createElement('input', { id: 'prompt-input', type: 'text', placeholder: 'Describe the logo theme' });
    const generateButton = createElement('button', { id: 'generate-logo-btn' }, 'Generate Logo');

    inputContainer.appendChild(label);
    inputContainer.appendChild(input);
    inputContainer.appendChild(generateButton);

    generateButton.addEventListener('click', handleGenerateLogo);

    return inputContainer;
}

// Event handler for generating the logo
async function handleGenerateLogo() {
    const loadingMessage = document.getElementById('loading-message');
    const logoContainer = document.getElementById('logo-container');
    const promptInput = document.getElementById('prompt-input').value.trim();

    if (!promptInput) {
        alert('Please enter a prompt.');
        return;
    }

    loadingMessage.style.display = 'block';
    logoContainer.innerHTML = '';

    const requestData = { prompt: promptInput };

    try {
        const response = await fetch('https://image-processor-app.onrender.com/ai_tools/generate-logo/', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });

        if (!response.ok) throw new Error('Logo generation failed.');

        const blob = await response.blob();
        const url = URL.createObjectURL(blob);

        displayGeneratedLogo(url);
    } catch (error) {
        displayErrorMessage();
        console.error('Error:', error);
    } finally {
        loadingMessage.style.display = 'none';
    }
}

// Function to display the generated logo
function displayGeneratedLogo(url) {
    const logoContainer = document.getElementById('logo-container');

    const logoImage = createElement('img', { src: url, alt: 'Generated Logo' });
    const downloadButton = createElement('button', { class: 'download-btn' }, 'Download Logo');
    downloadButton.innerHTML = '<span class="material-icons">download</span> Download Logo';
    downloadButton.addEventListener('click', () => downloadImage(url));

    logoContainer.appendChild(logoImage);
    logoContainer.appendChild(downloadButton);
}

// Function to display an error message
function displayErrorMessage() {
    const logoContainer = document.getElementById('logo-container');
    const errorMessage = createElement('p', { style: 'color: red;' }, 'Error generating logo. Please try again later.');
    logoContainer.appendChild(errorMessage);
}

// Function to download the generated logo
function downloadImage(imageUrl) {
    const a = createElement('a', { href: imageUrl, download: 'generated_logo.png' });
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

