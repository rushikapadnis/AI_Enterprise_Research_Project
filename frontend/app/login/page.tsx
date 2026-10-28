"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

import { apiRequest } from "@/lib/api";


interface LoginResponse {
  access_token: string;
  token_type: string;
}


export default function LoginPage() {

  const router = useRouter();

  const [email, setEmail] =
    useState("");

  const [password, setPassword] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");


  async function handleLogin() {

    if (!email.trim() || !password) {

      setError(
        "Please enter email and password."
      );

      return;
    }


    try {

      setLoading(true);
      setError("");


      const data =
        await apiRequest<LoginResponse>(
          "/users/login",
          {
            method: "POST",

            body: JSON.stringify({
              email: email.trim(),
              password,
            }),
          }
        );


      // Store JWT

      localStorage.setItem(
        "access_token",
        data.access_token
      );


      // Go to dashboard

      router.push("/");


    } catch (err) {

      setError(
        err instanceof Error
          ? err.message
          : "Login failed."
      );

    } finally {

      setLoading(false);

    }
  }


  return (

    <main className="flex min-h-screen items-center justify-center bg-slate-950 px-6 text-white">

      <div className="w-full max-w-md">


        {/* Header */}

        <div className="mb-8 text-center">

          <h1 className="text-3xl font-bold">
            AI Enterprise Research
          </h1>

          <p className="mt-2 text-slate-400">
            Sign in to your research workspace
          </p>

        </div>


        {/* Login Card */}

        <div className="rounded-2xl border border-slate-800 bg-slate-900 p-8">

          <h2 className="text-xl font-semibold">
            Sign in
          </h2>


          <p className="mt-2 text-sm text-slate-400">
            Enter your account credentials.
          </p>


          {/* Email */}

          <div className="mt-6">

            <label
              htmlFor="email"
              className="mb-2 block text-sm font-medium"
            >
              Email
            </label>

            <input
              id="email"
              type="email"
              value={email}
              onChange={(event) =>
                setEmail(event.target.value)
              }
              placeholder="demo@example.com"
              className="w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 outline-none placeholder:text-slate-600 focus:border-blue-500"
            />

          </div>


          {/* Password */}

          <div className="mt-4">

            <label
              htmlFor="password"
              className="mb-2 block text-sm font-medium"
            >
              Password
            </label>

            <input
              id="password"
              type="password"
              value={password}
              onChange={(event) =>
                setPassword(event.target.value)
              }
              onKeyDown={(event) => {

                if (event.key === "Enter") {
                  handleLogin();
                }

              }}
              placeholder="••••••••"
              className="w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 outline-none placeholder:text-slate-600 focus:border-blue-500"
            />

          </div>


          {/* Error */}

          {error && (

            <div className="mt-4 rounded-lg border border-red-900 bg-red-950/40 p-3 text-sm text-red-300">

              {error}

            </div>

          )}


          {/* Login Button */}

          <button
            onClick={handleLogin}
            disabled={loading}
            className="mt-6 w-full rounded-lg bg-blue-600 px-5 py-3 font-medium hover:bg-blue-500 disabled:cursor-not-allowed disabled:bg-slate-700"
          >

            {loading
              ? "Signing in..."
              : "Sign in"}

          </button>

        </div>


        <p className="mt-6 text-center text-xs text-slate-600">
          AI Enterprise Research & Action Agent
        </p>

      </div>

    </main>
  );
}