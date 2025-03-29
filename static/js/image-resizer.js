import { createElement } from "./utils.js";

// Function to create the main container
export function createContainer() {
  const container = createElement('div', { class: 'container' });

  const header = createElement('h1', {}, 'Image Resizer App');
  container.appendChild(header);

  const form = createForm();
  container.appendChild(form);

  const progressBar = createProgressBar();
  container.appendChild(progressBar);

  const imagePreview = createElement('div', { class: 'image-preview', id: 'image-preview' });
  container.appendChild(imagePreview);

  return container;
}

// Function to create the upload form
function createForm() {
  const form = createElement('form', { id: 'upload-form' });

  const fileGroup = createFormGroup('file', 'Choose an image:', 'file', { accept: 'image/*', required: true });
  form.appendChild(fileGroup);

  const widthGroup = createFormGroup('width', 'Width (px):', 'number', { placeholder: 'Enter width', required: true });
  form.appendChild(widthGroup);

  const heightGroup = createFormGroup('height', 'Height (px):', 'number', { placeholder: 'Enter height', required: true });
  form.appendChild(heightGroup);

  const clientIdGroup = createFormGroup('client_id', 'Client ID:', 'text', { readonly: true });
  form.appendChild(clientIdGroup);

  const submitButton = createElement('button', { type: 'submit' }, 'Upload and Resize');
  const buttonGroup = createElement('div', { class: 'form-group' });
  buttonGroup.appendChild(submitButton);
  form.appendChild(buttonGroup);

  form.addEventListener('submit', handleFormSubmit);

  return form;
}

// Function to create a form group
function createFormGroup(id, labelText, inputType, inputAttributes = {}) {
  const group = createElement('div', { class: 'form-group' });
  const label = createElement('label', { for: id }, labelText);
  const input = createElement('input', { id, type: inputType, ...inputAttributes });
  group.appendChild(label);
  group.appendChild(input);
  return group;
}

// Function to create the progress bar
function createProgressBar() {
  const progressBarContainer = createElement('div', { class: 'progress-bar' });
  const progress = createElement('div', { class: 'progress', id: 'progress' });
  const progressPercent = createElement('div', { class: 'progress-percent', id: 'progress-percent' }, '0%');
  progressBarContainer.appendChild(progress);
  progressBarContainer.appendChild(progressPercent);
  return progressBarContainer;
}

// Event handler for form submission
async function handleFormSubmit(event) {
  event.preventDefault();

  const clientId = Date.now().toString();
  document.getElementById('client_id').value = clientId;

  const fileInput = document.getElementById('file');
  const widthInput = document.getElementById('width');
  const heightInput = document.getElementById('height');

  const file = fileInput.files[0];
  const width = widthInput.value;
  const height = heightInput.value;

  if (!file) return alert('Please select an image.');

  resetProgressBar();
  displayOriginalImageDetails(file);

  try {
    await uploadAndResizeImage(clientId, file, width, height);
  } catch (error) {
    alert('Error uploading image.');
  }
}

// Function to reset progress bar and clear preview
function resetProgressBar() {
  const progressBar = document.getElementById('progress');
  const progressPercent = document.getElementById('progress-percent');
  const imagePreview = document.getElementById('image-preview');

  progressBar.style.width = '0%';
  progressPercent.textContent = '0%';
  imagePreview.innerHTML = '';
}

// Function to display original image details
function displayOriginalImageDetails(file) {
  const fileReader = new FileReader();
  const imagePreview = document.getElementById('image-preview');

  fileReader.onload = (event) => {
    const originalImage = new Image();
    originalImage.src = event.target.result;
    originalImage.onload = () => {
      const detailsContainer = createElement('div');
      detailsContainer.appendChild(createElement('p', {}, 'Original Image:'));
      detailsContainer.appendChild(createElement('p', {}, `Dimensions: ${originalImage.width}x${originalImage.height}px`));
      detailsContainer.appendChild(createElement('p', {}, `File Size: ${(file.size / 1024).toFixed(2)} KB`));
      imagePreview.appendChild(detailsContainer);
    };
  };

  fileReader.readAsDataURL(file);
}

// Function to upload and resize the image
async function uploadAndResizeImage(clientId, file, width, height) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('client_id', clientId);
  formData.append('width', width);
  formData.append('height', height);

  const eventSource = new EventSource(`http://127.0.0.1:8000/image_processing/api/progress/${clientId}`);
  const progressBar = document.getElementById('progress');
  const progressPercent = document.getElementById('progress-percent');

  eventSource.onmessage = (event) => {
    const progress = parseFloat(event.data);
    progressBar.style.width = `${progress}%`;
    progressPercent.textContent = `${progress}%`;

    if (progress === 100 || progress === -1) {
      eventSource.close();
      if (progress === -1) {
        alert('Upload failed.');
      }
    }
  };

  const response = await fetch(`http://127.0.0.1:8000/image_processing/api/upload?client_id=${clientId}&width=${width}&height=${height}`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) throw new Error('Upload failed.');

  const blob = await response.blob();
  displayResizedImageDetails(blob, width, height);
}

// Function to display resized image details
function displayResizedImageDetails(blob, width, height) {
  const url = URL.createObjectURL(blob);
  const imagePreview = document.getElementById('image-preview');

  const detailsContainer = createElement('div');
  detailsContainer.appendChild(createElement('p', {}, 'Resized Image:'));
  detailsContainer.appendChild(createElement('p', {}, `Dimensions: ${width}x${height}px`));
  detailsContainer.appendChild(createElement('p', {}, `File Size: ${(blob.size / 1024).toFixed(2)} KB`));

  const image = createElement('img', { src: url, alt: 'Resized Image' });
  detailsContainer.appendChild(image);

  const downloadButton = createElement('button', { class: 'download-btn' }, 'Download');
  downloadButton.addEventListener('click', () => downloadImage(url));
  detailsContainer.appendChild(downloadButton);

  imagePreview.appendChild(detailsContainer);
}

// Function to download the image
function downloadImage(url) {
  const a = createElement('a', { href: url, download: 'resized-image.png' });
  a.click();
  URL.revokeObjectURL(url);
}

