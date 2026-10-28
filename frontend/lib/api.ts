const API_URL =
  process.env.NEXT_PUBLIC_API_URL ||
  "http://localhost:8000";


export async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {

  const token =
    typeof window !== "undefined"
      ? localStorage.getItem("access_token")
      : null;


  const headers = new Headers(
    options.headers
  );


  headers.set(
    "Content-Type",
    "application/json"
  );


  if (token) {

    headers.set(
      "Authorization",
      `Bearer ${token}`
    );

  }


  const response = await fetch(
    `${API_URL}${endpoint}`,
    {
      ...options,
      headers,
    }
  );


  if (!response.ok) {

    let message =
      "Something went wrong.";

    try {

      const data =
        await response.json();

      message =
        data.detail ||
        message;

    } catch {
      // Ignore JSON parsing errors
    }

    throw new Error(message);
  }


  return response.json();
}