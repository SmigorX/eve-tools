import ResponsiveAppBar from "./modules/TopMenu.tsx";
import { ThemeProvider, createTheme } from '@mui/material';
import {useState} from "react";


const theme = createTheme({
    palette: {
        primary: {
            main: "#6E0000"
        },
        secondary: {
            main: "#232323"
        },
    },
});

function funny() {(console.log("Hey, where are you looking?! My page is up here!"))}
funny()

function App() {
    const [userData, setUserData] = useState<null | Record<number, string>>(null);

    const handleUserData = (userData: Record<number, string>) => {
        setUserData(userData)
    };

    return (
        <ThemeProvider theme={theme}>
            <ResponsiveAppBar handleUserData={handleUserData} userData={userData}/>
        </ThemeProvider>
        )
}

export default App
