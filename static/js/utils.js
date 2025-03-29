// Utility function to create elements with attributes
export function createElement(tag, attributes = {}, textContent = "") {
  const element = document.createElement(tag);
  Object.entries(attributes).forEach(([key, value]) => element.setAttribute(key, value));
  if (textContent) element.textContent = textContent;
  return element;
}
