const translations = {
  password: {
    title: "Password",
    position: 2,
    placeholder: "Secure Password",
  },
  identifier: {
    title: "E-Mail Address",
    position: 1,
    placeholder: "john.doe@example.com",
  },
  "traits.email": {
    title: "E-Mail Address",
    position: 1,
    placeholder: "john.doe@example.com",
  },
  "traits.first_name": {
    title: "First Name",
    position: 3,
    placeholder: "John",
  },
  "traits.last_name": {
    title: "Last Name",
    position: 4,
    placeholder: "Doe",
  },
};

export const filterFields = (fields) => 
  fields.filter(field => field.attributes.name in translations)

export const getFormFieldTitle = (field) =>
  field.name && field.name in translations
    ? translations[field.name].title
    : field.name;

export const getFormFieldPosition = (field) =>
  field.name && field.name in translations
    ? translations[field.name].position
    : Infinity;

export const getFormPlaceholder = (field) =>
  field.name && field.name in translations
    ? translations[field.name].placeholder
    : "";