"use client";
import { useCookies } from "react-cookie";
import { useSearchParams, useNavigate } from "react-router-dom";
async function keysRequest (sso_token, setCookie, router) {
    const backendRequestUrl = "http://localhost:5000/dev/token";

    try {
        const response = await fetch(backendRequestUrl, {
            method: "POST",
            body: JSON.stringify({SSOCode: sso_token}),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        });
        if (response.ok) {
            const response_content = await response.json()
            await setCookie("session", response_content, {path: "/", SameSite:"None", Secure: true});
        } else {
            console.error(`Network request failed: ${response.status}`)
        }
    } catch (error) {
        console.error("Network request failed: ${error}");
    }
    await router("/");
}

export default function SSOExchange() {
    const [SearchParams, ] = useSearchParams();
    const sso_token = SearchParams.get("code");

    const [, setCookie] = useCookies(["session"]);
    const router = useNavigate();

    keysRequest(sso_token, setCookie, router).then();

    return <div>If you see this for too long your login attempt has probably failed.</div>;
}
