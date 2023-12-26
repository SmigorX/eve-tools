import { app_colors } from "../index.jsx";
import cryptoRandomString from "crypto-random-string";
import { useState } from "react";


export default function TopMenu() {
    const [isDropdownVisible, setDropdownVisible] = useState(false);

    const toggleDropdown = () => {
        setDropdownVisible(!isDropdownVisible);
    };

    return (
        <header style={{position: "sticky"}}>
            <div style={{display: "flex", justifyContent: "center", backgroundColor: app_colors().background}}>
                <div style={{display: "inline-flex", width: "50%", height: "20mm", justifyContent: "space-between", alignItems: "center"}}>
                    <a href={"/"} style={{textDecoration: "none", color: app_colors().text, fontSize:"10mm"}}>eve tools</a>
                    {UserButton(toggleDropdown)}
                </div>
            </div>
            <div style={{position: "absolute", right: "707px"}}>
                {DropdownMenu(isDropdownVisible)}
            </div>
        </header>
    )
}

const DropdownMenu = (isDropdownVisible) => {
    console.log(AuthURL())

    if (isDropdownVisible) {
        return (
            <div style={{position: "inherit", display: "flex", flexDirection: "column", width: "30mm", backgroundColor: "black"}}>
                <button>test</button>
                <button>test</button>
                <button>test</button>
            </div>
        )
    }
}


const UserButton = (toggleDropdown) => {
    return (
        <button onClick={toggleDropdown} style={{height: "20mm", width: "20mm"}}>Open Dropdown</button>
    )
}


export const AuthURL = () => {
    const urlFirstPart = "https://login.eveonline.com/oauth/authorize?code_challenge="
    const urlLastPart = "&response_type=code&client_id=d40c1a23ee8a433ab3e161b46c105e9c&redirect_uri=http%3A%2F%2Flocalhost%3A3000%2Fapi&scope=esi-contracts.read_corporation_contracts.v1+esi-contracts.read_character_contracts.v1";
    const generateUrlSafeToken = () => {
        return cryptoRandomString({length: 128, type: 'url-safe'});
    }
    console.log(urlFirstPart + generateUrlSafeToken() + urlLastPart)
    return (urlFirstPart + generateUrlSafeToken() + urlLastPart)
}