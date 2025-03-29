import { createElement } from "./utils.js";
import { createContainer } from "./image-resizer.js";
import { navigation } from "./navigation.js";
import { createCountryFlagLogoContainer } from "./logo_generator.js";


function createServiceCaption(){
	const serviceCaption = createElement("h1", {class: "service-caption"}, 'Welcome to Image Processor App. Select A Service');
	return serviceCaption;
}



function createServiceCards() {
  const cardsArray = [
    {
      icon: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="currentColor">
               <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM5 19V5h14v14H5zm12-6h-5v5h-2v-5H7v-2h3V7h2v4h5v2z"/>
             </svg>`,
      text: "Resize Image",
    },
    {
      icon: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="currentColor">
               <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z"/>
             </svg>`,
      text: "Generate Any Country Logo with AI",
    },
  ];

  // Create a container for the cards
  const cardContainer = document.createElement("div");
  cardContainer.classList.add("card-container");

  // Iterate through the cardsArray and create each card
  cardsArray.forEach((card, index) => {
    const cardElement = document.createElement("div");
    cardElement.classList.add("card");

    const iconElement = document.createElement("div");
    iconElement.classList.add("icon");
    iconElement.innerHTML = card.icon;

    const textElement = document.createElement("p");
    textElement.classList.add("service-text");
    textElement.innerText = card.text;

    cardElement.appendChild(iconElement);
    cardElement.appendChild(textElement);
    cardContainer.appendChild(cardElement);

    // Add a click listener to the card
    cardElement.addEventListener("click", () => {
      switch (index) {
        case 0:
          console.log("Resize Image clicked");
          // Call the function for Resize Image
	  navigation.push("false", createContainer(), "100%", "100%");
          break;
        case 1:
          console.log("Generate Any Country Logo with AI clicked");
          // Call the function for Generate Country Logo
	  navigation.push(false, createCountryFlagLogoContainer(), "100%", "100%");
          break;
        default:
          console.log("Unknown card clicked");
          break;
      }
    });
  });

  return cardContainer;
}




function renderCards(){
	const container = createElement("div", {class: "service-container"});
	container.appendChild(createServiceCaption());
	container.appendChild(createServiceCards());
	return container;
}

//Append to dom
document.body.appendChild(renderCards());
