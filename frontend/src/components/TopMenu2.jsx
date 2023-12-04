import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import MenuIcon from '@mui/icons-material/Menu';
import Container from '@mui/material/Container';
import AdbIcon from '@mui/icons-material/Adb';
import React from "react";
import {Button, Menu} from "@mui/material";
import cryptoRandomString from "crypto-random-string";
import { app_colors } from "../index.jsx";

export default function TopMenu2() {
    return (
        <AppBar position="static">
            <Container maxWidth="xl">
                <Toolbar disableGutters>
                    {/* For larger screens */}
                    <AdbIcon sx={{ display: { xs: 'none', md: 'flex' }, mr: 1 }} />
                    <Typography
                        variant="h6"
                        noWrap
                        component="a"
                        href="/"
                        sx={{
                            mr: 2,
                            display: { xs: 'none', md: 'flex' },
                            fontFamily: 'monospace',
                            fontWeight: 700,
                            letterSpacing: '.3rem',
                            color: app_colors().text,
                            textDecoration: 'none',
                        }}
                    >
                        EVETOOLS
                    </Typography>

                    <Box sx={{ flexGrow: 1 }} />

                    <div       style={{
                        position: 'fixed',
                        left: 0,
                        display: 'flex',
                        alignItems: 'center',
                        padding: '8px',
                    }}>

                        {/* For smaller screens */}
                        <Box sx={{ display: { xs: 'flex', md: 'none' } }}>
                            <IconButton
                                size="large"
                                aria-label="account of current user"
                                aria-controls="menu-appbar"
                                aria-haspopup="true"
                                color= {app_colors().text}
                            >
                                <MenuIcon />
                            </IconButton>
                        </Box>

                        <AdbIcon sx={{ display: { xs: 'flex', md: 'none' }, mr: 1 }} />
                        <Typography
                            variant="h5"
                            noWrap
                            component="a"
                            href=""
                            sx={{
                                mr: 2,
                                display: { xs: 'flex', md: 'none' },
                                fontFamily: 'monospace',
                                fontWeight: 700,
                                letterSpacing: '.3rem',
                                color: 'secondary',
                                textDecoration: 'none',
                            }}
                        >
                            EVETOOLS
                        </Typography>
                    </div>
                    {DropdownButton()}
                </Toolbar>
            </Container>
        </AppBar>
    );
}

//                    <DropdownButton handleUserData={handleUserData} userData={userData}/>

const DropdownButton = () => {
    const [anchorEl, setAnchorEl] = React.useState(null);

    const handleOpenMenu = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleCloseMenu = () => {
        setAnchorEl(null);
    };


    function dropdownMenuElements(userData) {
        if (userData == null) {
            return (
                <Button color="secondary" href={AuthURL()}>
                    Log in
                </Button>
            );
        } else {
            return ( //onClick={() => handleUserData(null)}
                <Button color="secondary">
                    Log out
                </Button>
            );
        }
    }

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
                {dropdownMenuElements()}
            </Menu>
        </div>
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
