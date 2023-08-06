import React, { useEffect, useState } from 'react';
import { Button, Menu } from '@mui/material';
import PersonRoundedIcon from '@mui/icons-material/PersonRounded';
import cryptoRandomString from "crypto-random-string";


const DropdownButton = () => {
    const [anchorEl, setAnchorEl] = React.useState(null);
    const [characterPortrait, setCharacterPortrait] = useState<string | null>(null);

    const handleOpenMenu = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleCloseMenu = () => {
        setAnchorEl(null);
    };

    const AuthURL = () => {
        const urlFirstPart = "https://login.eveonline.com/oauth/authorize?code_challenge="
        const urlLastPart = "&response_type=code&client_id=d40c1a23ee8a433ab3e161b46c105e9c&&redirect_uri=http%3A%2F%2Flocalhost%3A5173&scope=esi-contracts.read_corporation_contracts.v1+esi-contracts.read_character_contracts.v1\n"
        const generateUrlSafeToken = () => {
            return cryptoRandomString({length: 128, type: 'url-safe'});
        }
        return (urlFirstPart + generateUrlSafeToken() + urlLastPart)
    }


    const postDataToServer = async () => {
        const getCodeQueryParam = () => {
            const urlParams = new URLSearchParams(window.location.search);
            return urlParams.get('code');
        };
        const queryData = getCodeQueryParam();
        const backendRequestUrl = "http://localhost:5000/dev/token";

        if (queryData != null) {
            if (characterPortrait == null) {
                try {
                    const response = await fetch(backendRequestUrl, {
                        method: "POST",
                        body: JSON.stringify({
                            authToken: queryData
                        }),
                        headers: {
                            "Content-type": "application/json; charset=UTF-8"
                        }
                    });
                    if (response.ok) {
                        return response.json();
                    } else {
                        throw new Error(`Request failed with status: ${response.status} ${response.statusText}`);
                    }
                } catch (error) {
                    throw new Error(`Network request failed: ${error}`);
                }
            } else {
                return null;
            }
        }
    };


    useEffect(() => {
        postDataToServer().then((data) => {
            if (data && data['character_portrait']) {
                setCharacterPortrait(data['character_portrait']);
            }
        }).catch((error) => {
            console.error("Error:", error);
        });
    }, []);


    return (
        <div>
            <Button
                onClick={handleOpenMenu}
                variant="contained"
                color="secondary"
                aria-controls="dropdown-menu"
                aria-haspopup="true"
                style={{ height: '64px', padding: 0 }}
            >
                {characterPortrait ? (
                    <img src={characterPortrait} alt="Character Portrait"
                         style={{ width: '100%', height: '100%', objectFit: 'cover', borderRadius: '5%' }} />
                ) : (
                    <PersonRoundedIcon />
                )}
            </Button>
            <Menu
                id="dropdown-menu"
                anchorEl={anchorEl}
                open={Boolean(anchorEl)}
                onClose={handleCloseMenu}
                anchorOrigin={{
                    vertical: 'bottom',
                    horizontal: 'center',
                }}
                transformOrigin={{
                    vertical: 'top',
                    horizontal: 'center',
                }}
            >
                <Button color={"secondary"} href={AuthURL()}>Log in</Button>
            </Menu>
        </div>
    );
};

export default DropdownButton;