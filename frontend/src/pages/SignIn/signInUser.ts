import Cookies from "js-cookie";

const csrftoken = Cookies.get("csrftoken");

export default async function signInUser(userData: {
  email: string;
  password: string;
}) {
  const response = await fetch("api/user/token/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(csrftoken && { "X-CSRFToken": csrftoken }),
    },
    body: JSON.stringify(userData),
  });

  if (!response.ok) {
    const errorResponse = await response.json();
    if (errorResponse.email) {
      throw new Error(errorResponse.email[0]);
    }
    if (errorResponse.password) {
      throw new Error(errorResponse.password[0]);
    }
    if (errorResponse.non_field_errors) {
      console.error(errorResponse.non_field_errors);
      throw new Error(errorResponse.non_field_errors[0]);
    }
    throw new Error("An error occurred. Please try again.");
  }

  return response.json();
}
