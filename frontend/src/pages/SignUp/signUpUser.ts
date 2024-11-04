import Cookies from "js-cookie";

const csrftoken = Cookies.get("csrftoken");

export default async function signUpUser(userData: {
  name: string;
  email: string;
  password: string;
}) {
  const response = await fetch("api/user/create/", {
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
    if (errorResponse.name) {
      throw new Error(errorResponse.name[0]);
    }
    throw new Error("An error occurred. Please try again.");
  }

  return response.json();
}
