const amenitiesGrid = document.getElementById('amenities-grid');
const form = document.getElementById('tour-request-form');
const successMessage = document.getElementById('form-success');
const menuToggle = document.getElementById('menu-toggle');
const mainMenu = document.getElementById('main-menu');
const currentYear = document.getElementById('current-year');

const AMENITIES_ENDPOINT = 'http://localhost:5000/api/amenities';
const INQUIRIES_ENDPOINT = 'http://localhost:5000/api/inquiries';

function renderAmenities(amenities) {
  if (!amenitiesGrid) return;

  amenitiesGrid.innerHTML = '';

  amenities.forEach((amenity) => {
    const card = document.createElement('article');
    card.className = 'feature-card';
    card.id = `amenity-${amenity.id}`;

    const title = document.createElement('h3');
    title.className = 'feature-card__title';
    title.textContent = amenity.name;

    const description = document.createElement('p');
    description.className = 'feature-card__description';
    description.textContent = amenity.description;

    card.appendChild(title);
    card.appendChild(description);

    amenitiesGrid.appendChild(card);
  });
}

async function fetchAmenities() {
  try {
    const response = await fetch(AMENITIES_ENDPOINT);
    if (!response.ok) {
      throw new Error(`Failed to load amenities: ${response.status}`);
    }

    const data = await response.json();
    renderAmenities(data.amenities || []);
  } catch (error) {
    console.error(error);
  }
}

function toggleMenu() {
  const isOpen = mainMenu.classList.toggle('navigation__menu--open');
  menuToggle.setAttribute('aria-expanded', String(isOpen));
}

function resetFormState() {
  successMessage.textContent = '';
  const errorFields = form.querySelectorAll('.form__error');
  errorFields.forEach((field) => {
    field.textContent = '';
  });
}

function setFieldError(fieldId, message) {
  const errorTarget = document.getElementById(`error-${fieldId}`);
  if (errorTarget) {
    errorTarget.textContent = message;
  }
}

function validateForm(formData) {
  let isValid = true;

  if (!formData.get('name')) {
    setFieldError('name', 'Please provide your name.');
    isValid = false;
  }

  if (!formData.get('email')) {
    setFieldError('email', 'Let us know how to reach you by email.');
    isValid = false;
  }

  if (!formData.get('phone')) {
    setFieldError('phone', 'Please include a phone number.');
    isValid = false;
  }

  if (!formData.get('preferred_date')) {
    setFieldError('preferred-date', 'Select your preferred tour date.');
    isValid = false;
  }

  return isValid;
}

async function submitForm(event) {
  event.preventDefault();
  resetFormState();

  const formData = new FormData(form);
  const payload = Object.fromEntries(formData.entries());

  if (!validateForm(formData)) {
    return;
  }

  try {
    const response = await fetch(INQUIRIES_ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errorPayload = await response.json();
      throw new Error(errorPayload.message || 'Submission failed');
    }

    form.reset();
    successMessage.textContent = 'Thank you! Our concierge will contact you soon.';
  } catch (error) {
    successMessage.textContent = 'We could not submit your request. Please try again.';
    console.error(error);
  }
}

if (currentYear) {
  currentYear.textContent = new Date().getFullYear();
}

if (amenitiesGrid) {
  fetchAmenities();
}

if (form) {
  form.addEventListener('submit', submitForm);
}

if (menuToggle && mainMenu) {
  menuToggle.addEventListener('click', toggleMenu);
}
